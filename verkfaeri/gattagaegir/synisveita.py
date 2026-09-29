"""Sýnisveita — OAI-PMH 2.0 þjónn fyrir gullið DC á ListRecords-formi.

Til hvers: gagnaeigandi sem á ekki OAI-þjón (RÚV, Listasafn) sendir skrá; við
umbreytum henni í gullna DC-sniðið og þá er hægt að sýna honum strax hvernig
hans eigin gögn líta út sem OAI-veita — og prófa hana í Gáttagægi. Sama skrá
fer í `Upload File/s` í Alma.

Fylgir staðlinum orðrétt (openarchives.org/OAI/openarchivesprotocol.html):
sex aðgerðir, sett, from/until, resumptionToken með completeListSize og
cursor, villur sem OAI-kóðar (§3.6), GET og POST. Færslurnar eru hafðar í
sqlite í minni — lítil skrá, en sömu fyrirspurnir og stór gagnagrunnur.

Engin ytri söfn. Kallað úr thjonn.py á /veitur/<nafn>/oai.
"""
import base64
import datetime
import html
import json
import re
import sqlite3
import xml.etree.ElementTree as ET

OAI_NS = "http://www.openarchives.org/OAI/2.0/"
_O = "{%s}" % OAI_NS
OAI_DC = ("oai_dc", "http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
          "http://www.openarchives.org/OAI/2.0/oai_dc/")
ROK = {  # leyfð rök hverrar aðgerðar (staðall §4); None = frjálst/valfrjálst
    "Identify": {"required": set(), "optional": set()},
    "ListMetadataFormats": {"required": set(), "optional": {"identifier"}},
    "ListSets": {"required": set(), "optional": {"resumptionToken"}},
    "GetRecord": {"required": {"identifier", "metadataPrefix"}, "optional": set()},
    "ListIdentifiers": {"required": {"metadataPrefix"},
                        "optional": {"from", "until", "set", "resumptionToken"}},
    "ListRecords": {"required": {"metadataPrefix"},
                    "optional": {"from", "until", "set", "resumptionToken"}},
}
_DAGS = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_SEK = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def _x(s):
    return html.escape(str(s), quote=True)


class Synisveita:
    def __init__(self, nafn, xml_texti, heiti=None, netfang="einar@kann.is",
                 sidustaerd=5, lysing="", audkennisforskeyti="", adgangur=None, uppruni=""):
        self.nafn = nafn
        # færslusíður: /<nafn>/<stutt> ↔ <audkennisforskeyti><stutt>
        self.audkennisforskeyti = audkennisforskeyti
        self.adgangur = adgangur or {}      # {"texti": …, "slod": …} — hvar efnið sjálft fæst
        self.uppruni = uppruni
        self.heiti = heiti or ("Sýnisveita: " + nafn)
        self.netfang = netfang
        self.sidustaerd = sidustaerd
        self.lysing = lysing
        self.db = sqlite3.connect(":memory:", check_same_thread=False)
        self.db.execute("CREATE TABLE f (rod INTEGER PRIMARY KEY, id TEXT UNIQUE, "
                        "datestamp TEXT, sett TEXT, metadata TEXT)")
        self._hlada(xml_texti)

    # ---------------------------------------------------------- innlestur
    def _hlada(self, xml_texti):
        rot = ET.fromstring(xml_texti.encode("utf-8"))
        # skráin má vera ber <ListRecords> (Alma-upphleðsla) eða heilt OAI-svar
        records = [r for r in rot.iter() if r.tag.split("}")[-1] == "record"]
        for r in records:
            h = next(c for c in r if c.tag.split("}")[-1] == "header")
            finna = lambda nafn: [c.text.strip() for c in h
                                  if c.tag.split("}")[-1] == nafn and c.text]
            aud = finna("identifier")[0]
            ds = (finna("datestamp") or ["2026-01-01T00:00:00Z"])[0]
            if _DAGS.match(ds):
                ds += "T00:00:00Z"
            md = next((c for c in r if c.tag.split("}")[-1] == "metadata"), None)
            innra = ""
            if md is not None and len(md):
                innra = ET.tostring(md[0], encoding="unicode")
            self.db.execute("INSERT INTO f (id, datestamp, sett, metadata) VALUES (?,?,?,?)",
                            (aud, ds, json.dumps(finna("setSpec")), innra))
        self.db.commit()

    def fjoldi(self):
        return self.db.execute("SELECT COUNT(*) FROM f").fetchone()[0]

    # ---------------------------------------------------------- svar
    def svara(self, rok, base_url):
        """rok: {nafn: [gildi, …]} (eins og parse_qs skilar). Skilar (200, xml)."""
        einfold = {k: v[0] for k, v in rok.items()}
        verb = einfold.get("verb")
        beidni_at = "".join(' %s="%s"' % (k, _x(v)) for k, v in sorted(einfold.items()))
        if any(len(v) != 1 for v in rok.values()):
            return self._villa(base_url, "", "badArgument", "Rök mega ekki koma oftar en einu sinni.")
        if verb not in ROK:
            return self._villa(base_url, "", "badVerb",
                               "Óþekkt eða vantandi verb." if verb else "verb vantar.")
        hin = {k: v for k, v in einfold.items() if k != "verb"}
        leyft = ROK[verb]
        if "resumptionToken" in hin and verb in ("ListIdentifiers", "ListRecords", "ListSets"):
            if len(hin) > 1:
                return self._villa(base_url, beidni_at, "badArgument",
                                   "resumptionToken er einkarök.")
        else:
            vantar = leyft["required"] - set(hin)
            ofaukid = set(hin) - leyft["required"] - leyft["optional"]
            if vantar or ofaukid:
                return self._villa(base_url, beidni_at, "badArgument",
                                   "Vantar: %s. Óleyfð: %s." % (", ".join(sorted(vantar)) or "—",
                                                               ", ".join(sorted(ofaukid)) or "—"))
        fall = getattr(self, "_" + verb)
        return fall(hin, base_url, beidni_at)

    # ---------------------------------------------------------- aðgerðir
    def _Identify(self, rok, base, at):
        elst = self.db.execute("SELECT MIN(datestamp) FROM f").fetchone()[0] or "2026-01-01T00:00:00Z"
        lys = ("<description><![CDATA[%s]]></description>" % self.lysing.replace("]]>", "]] >")
               if self.lysing else "")
        return self._umslag(base, at, "<Identify><repositoryName>%s</repositoryName>"
                            "<baseURL>%s</baseURL><protocolVersion>2.0</protocolVersion>"
                            "<adminEmail>%s</adminEmail><earliestDatestamp>%s</earliestDatestamp>"
                            # kyrr skrá: engu er eytt, svo „persistent“ stenst orðrétt
                            "<deletedRecord>persistent</deletedRecord>"
                            "<granularity>YYYY-MM-DDThh:mm:ssZ</granularity>%s</Identify>"
                            % (_x(self.heiti), _x(base), _x(self.netfang), elst, lys))

    def _ListMetadataFormats(self, rok, base, at):
        if "identifier" in rok and not self._til(rok["identifier"]):
            return self._villa(base, at, "idDoesNotExist", "Auðkennið er ekki til.")
        p, s, n = OAI_DC
        return self._umslag(base, at, "<ListMetadataFormats><metadataFormat>"
                            "<metadataPrefix>%s</metadataPrefix><schema>%s</schema>"
                            "<metadataNamespace>%s</metadataNamespace></metadataFormat>"
                            "</ListMetadataFormats>" % (p, s, n))

    def _ListSets(self, rok, base, at):
        if "resumptionToken" in rok:
            return self._villa(base, at, "badResumptionToken", "Settin koma á einni síðu.")
        sett = set()
        for (s,) in self.db.execute("SELECT sett FROM f"):
            sett.update(json.loads(s))
        inn = "".join("<set><setSpec>%s</setSpec><setName>%s</setName></set>"
                      % (_x(s), _x(self._setheiti(s))) for s in sorted(sett))
        return self._umslag(base, at, "<ListSets>%s</ListSets>" % inn)

    def _GetRecord(self, rok, base, at):
        if rok["metadataPrefix"] != "oai_dc":
            return self._villa(base, at, "cannotDisseminateFormat", "Aðeins oai_dc.")
        r = self.db.execute("SELECT id, datestamp, sett, metadata FROM f WHERE id=?",
                            (rok["identifier"],)).fetchone()
        if not r:
            return self._villa(base, at, "idDoesNotExist", "Auðkennið er ekki til.")
        return self._umslag(base, at, "<GetRecord>%s</GetRecord>" % self._record(r, True))

    def _ListIdentifiers(self, rok, base, at):
        return self._listi(rok, base, at, "ListIdentifiers", False)

    def _ListRecords(self, rok, base, at):
        return self._listi(rok, base, at, "ListRecords", True)

    # ---------------------------------------------------------- listi + token
    def _listi(self, rok, base, at, verb, med_metadata):
        if "resumptionToken" in rok:
            try:
                st = json.loads(base64.urlsafe_b64decode(rok["resumptionToken"].encode()).decode())
                prefix, sett, fra, til, byrja = (st["p"], st.get("s"), st.get("f"),
                                                st.get("u"), int(st["o"]))
            except Exception:
                return self._villa(base, at, "badResumptionToken", "Ógilt eða útrunnið token.")
        else:
            prefix, sett = rok["metadataPrefix"], rok.get("set")
            fra, til, byrja = rok.get("from"), rok.get("until"), 0
            if prefix != "oai_dc":
                return self._villa(base, at, "cannotDisseminateFormat", "Aðeins oai_dc.")
            for d in (fra, til):
                if d and not (_DAGS.match(d) or _SEK.match(d)):
                    return self._villa(base, at, "badArgument", "Dagsetning á rangu formi: %s" % d)
            if fra and til and (bool(_DAGS.match(fra)) != bool(_DAGS.match(til))):
                return self._villa(base, at, "badArgument",
                                   "from og until verða að hafa sama nákvæmnisstig.")
        rows = self._sia(sett, fra, til)
        if not rows:
            return self._villa(base, at, "noRecordsMatch", "Engin færsla passar.")
        alls = len(rows)
        sida = rows[byrja:byrja + self.sidustaerd]
        inn = "".join(self._record(r, med_metadata) for r in sida)
        naesta = byrja + self.sidustaerd
        if "resumptionToken" in rok or naesta < alls:
            tok = ""
            if naesta < alls:
                tok = base64.urlsafe_b64encode(json.dumps(
                    {"p": prefix, "s": sett, "f": fra, "u": til, "o": naesta},
                    separators=(",", ":")).encode()).decode()
            inn += '<resumptionToken completeListSize="%d" cursor="%d">%s</resumptionToken>' % (
                alls, byrja, tok)
        return self._umslag(base, at, "<%s>%s</%s>" % (verb, inn, verb))

    def _sia(self, sett, fra, til):
        """Sett og dagsetningabil. Dagur (YYYY-MM-DD) ber saman fyrstu 10 stafi
        datestamp; sekúndur (…Z) bera saman allan strenginn — ISO raðast rétt."""
        n = lambda d: 10 if _DAGS.match(d) else 20
        ut = []
        for r in self.db.execute("SELECT id, datestamp, sett, metadata FROM f ORDER BY rod"):
            if sett and sett not in json.loads(r[2]):
                continue
            if fra and r[1][:n(fra)] < fra:
                continue
            if til and r[1][:n(til)] > til:
                continue
            ut.append(r)
        return ut

    # ---------------------------------------------------------- færslusíða
    _DC = "{http://purl.org/dc/elements/1.1/}"
    _DCT = "{http://purl.org/dc/terms/}"
    _ROLE = "{https://mshl.is/terms#}role"

    def faersla(self, stutt):
        """Ein færsla sem orðabók fyrir færslusíðu, eða None. `stutt` er
        auðkennið án forskeytis (t.d. 6170EA10)."""
        aud = self.audkennisforskeyti + stutt
        r = self.db.execute("SELECT id, datestamp, sett, metadata FROM f WHERE id=?", (aud,)).fetchone()
        if not r or not r[3]:
            return None
        dc = ET.fromstring(r[3])
        allt = lambda tag: [" ".join((e.text or "").split()) if tag != "description" else (e.text or "").strip()
                            for e in dc if e.tag.split("}")[-1] == tag and (e.text or "").strip()]
        folk = [{"nafn": (e.text or "").strip(), "hlutverk": e.get(self._ROLE, ""),
                 "reitur": e.tag.split("}")[-1]}
                for e in dc if e.tag.split("}")[-1] in ("creator", "contributor") and (e.text or "").strip()]
        foreldri = None
        hlutar = [e for e in dc if e.tag == self._DCT + "isPartOf"]
        fid = next((e.text.strip() for e in hlutar if (e.text or "").startswith(self.audkennisforskeyti)
                    and self.audkennisforskeyti), None)
        if fid:
            ftitill = next((e.text.strip() for e in hlutar if not (e.text or "").startswith(self.audkennisforskeyti)), "")
            foreldri = {"stutt": fid[len(self.audkennisforskeyti):], "titill": ftitill}
        born = []
        for bid, bmd in self.db.execute("SELECT id, metadata FROM f WHERE metadata LIKE ? ORDER BY rod",
                                        ("%>" + aud + "<%",)):
            if bid == aud:
                continue
            t = ET.fromstring(bmd).find(self._DC + "title")
            born.append({"stutt": bid[len(self.audkennisforskeyti):],
                         "titill": " ".join((t.text or "").split()) if t is not None else bid})
        return {
            "audkenni": aud, "stutt": stutt, "titill": (allt("title") or [stutt])[0],
            "tegund": [e.text.strip() for e in dc if e.tag == self._DC + "type"
                       and e.get("{http://www.w3.org/XML/1998/namespace}lang") == "is"],
            "dags": (allt("date") or [""])[0], "tekid_upp": (allt("created") or [""])[0],
            "utsent": allt("issued"), "lysing": (allt("description") or [""])[0],
            "efnisord": [e.text.strip() for e in dc if e.tag == self._DC + "subject" and (e.text or "").strip()
                         and not e.get("{http://www.w3.org/2001/XMLSchema-instance}type")],
            "flokkar": [e.text.strip() for e in dc if e.tag == self._DC + "subject" and (e.text or "").strip()
                        and e.get("{http://www.w3.org/2001/XMLSchema-instance}type")],
            "folk": folk, "foreldri": foreldri, "born": born,
            "frumeintak": (allt("source") or [""])[0], "midill": (allt("format") or [""])[0],
            "lengd": (allt("extent") or [""])[0], "utgefandi": allt("publisher"),
            "safnnumer": [i for i in allt("identifier") if not i.startswith(("http", "oai:"))],
            "rettindi": (allt("rights") or [""])[0],
            "tilvisanir": self._tilvisanir(dc),
            # smámynd: bein myndslóð í dc:identifier (gullna sniðið, LinkingParameter2)
            "mynd": next((i for i in allt("identifier") if i.startswith(("http://", "https://"))
                          and re.search(r"\.(jpe?g|png|webp)$", i, re.I)), ""),
        }

    def _tilvisanir(self, dc):
        """dcterms:isReferencedBy í pörum, eins og isPartOf: texti + slóð."""
        tv = [(e.text or "").strip() for e in dc if e.tag == self._DCT + "isReferencedBy" and (e.text or "").strip()]
        slodir = [t for t in tv if t.startswith(("http://", "https://"))]
        textar = [t for t in tv if not t.startswith(("http://", "https://"))]
        return [{"titill": textar[i] if i < len(textar) else s, "slod": s} for i, s in enumerate(slodir)]

    def yfirlit(self):
        """Allar færslur í röð skrárinnar: efsta stig, börn undir foreldri sínu."""
        rod, eftir_id = [], {}
        for aud, md in self.db.execute("SELECT id, metadata FROM f ORDER BY rod"):
            if not md:
                continue
            dc = ET.fromstring(md)
            texti = lambda tag, lang=None: next(
                (" ".join((e.text or "").split()) for e in dc if e.tag == self._DC + tag and (e.text or "").strip()
                 and (lang is None or e.get("{http://www.w3.org/XML/1998/namespace}lang") == lang)), "")
            foreldri = next((e.text.strip()[len(self.audkennisforskeyti):] for e in dc
                             if e.tag == self._DCT + "isPartOf" and self.audkennisforskeyti
                             and (e.text or "").strip().startswith(self.audkennisforskeyti)), None)
            stutt = aud[len(self.audkennisforskeyti):] if aud.startswith(self.audkennisforskeyti) else aud
            t = {"stutt": stutt, "titill": texti("title") or stutt, "tegund": texti("type", "is"),
                 "dags": texti("date"), "foreldri": foreldri, "born": []}
            eftir_id[stutt] = t
            rod.append(t)
        efst = []
        for t in rod:
            if t["foreldri"] and t["foreldri"] in eftir_id:
                eftir_id[t["foreldri"]]["born"].append(t)
            else:
                efst.append(t)
        return efst

    # ---------------------------------------------------------- smáföll
    def _til(self, aud):
        return self.db.execute("SELECT 1 FROM f WHERE id=?", (aud,)).fetchone() is not None

    @staticmethod
    def _setheiti(s):
        if s.startswith("source:"):
            return "Allt safnið (%s)" % s.split(":", 1)[1]
        if s.startswith("type:"):
            return "Tegund: " + s.split(":", 1)[1]
        return s

    @staticmethod
    def _record(r, med_metadata):
        aud, ds, sett, md = r
        haus = "<header><identifier>%s</identifier><datestamp>%s</datestamp>%s</header>" % (
            _x(aud), ds, "".join("<setSpec>%s</setSpec>" % _x(s) for s in json.loads(sett)))
        if not med_metadata:
            return haus
        return "<record>%s<metadata>%s</metadata></record>" % (haus, md)

    def _umslag(self, base, at, inni):
        nu = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return 200, ('<?xml version="1.0" encoding="UTF-8"?>\n'
                     '<OAI-PMH xmlns="%s" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                     'xsi:schemaLocation="%s http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">'
                     "<responseDate>%s</responseDate><request%s>%s</request>%s</OAI-PMH>\n"
                     % (OAI_NS, OAI_NS, nu, at, _x(base), inni))

    def _villa(self, base, at, kodi, texti):
        # staðall §3.6: við badVerb og badArgument ber request aðeins baseURL
        if kodi in ("badVerb", "badArgument"):
            at = ""
        return self._umslag(base, at, '<error code="%s">%s</error>' % (kodi, _x(texti)))

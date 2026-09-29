#!/usr/bin/env python3
"""byggja_timarit_dc.py — Tímarit.is (OAI-PMH, oai_dc) → gullið Dublin Core.

Tímarit.is (Landsbókasafn Íslands – Háskólabókasafn) á opna OAI-PMH gagnaveitu
á https://timarit.is/oai. Hver færsla þar er TITILL blaðs eða tímarits — ekki
tölublað og ekki grein. Forritið sækir alla gagnaveituna (eða les vistað svar),
færir hana í gullna sniðið (snidmat/GULLNA-SNIDID.md), sannprófar og skrifar:

    gagnaveitur/timarit/TIMARIT-tryA.xml            í git; fer í Upload File/s í Alma
    verkfaeri/gattagaegir/synisveitur/timarit.xml   sama skrá; sýnisveita (utan git)

Sniðið sem Alma tekur við: ber <ListRecords> án xmlns og án <?xml …?>-línu;
nafnrýmin eru á hverju <oai_dc:dc>. Kortlagningin og rökin fyrir henni eru í
README.md hér við hliðina. Ekkert er skrifað ef sannprófunin bregst.

Keyrsla (Python 3.9+, engin ytri söfn):
    python3 byggja_timarit_dc.py                     # sækir gagnaveituna
    python3 byggja_timarit_dc.py --vista hratt.xml   # sækir og vistar hráa svarið
    python3 byggja_timarit_dc.py hratt.xml           # les vistað svar (eða fleiri, í röð)
"""
import argparse
import collections
import html
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HER = os.path.dirname(os.path.abspath(__file__))
ROT = os.path.abspath(os.path.join(HER, "..", ".."))
UT = os.path.join(HER, "TIMARIT-tryA.xml")
SYNISVEITA = os.path.join(ROT, "verkfaeri", "gattagaegir", "synisveitur", "timarit.xml")

# Án skástriks. Identify auglýsir http://timarit.is/oai, sem fer í 301 hingað.
BASEURL = "https://timarit.is/oai"
UA = "MSHL-Sagnatrog harvest (einar@kann.is)"
SETT = "source:timarit"
# Slóð á titil (mælt 29.9.2026): https svarar 302 á fyrstu síðu titilsins;
# http svarar 301 á https og svo 302. https sparar eitt stökk.
SLOD_TITILS = "https://timarit.is/publication/"

OAI = "{http://www.openarchives.org/OAI/2.0/}"
OAI_DC = "{http://www.openarchives.org/OAI/2.0/oai_dc/}"
DC = "{http://purl.org/dc/elements/1.1/}"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

TEGUND_IS = "Tímarit"
TEGUND_EN = "Text"
EFNI_IS = "Tímarit og blöð"
EFNI_EN_THEKKT = {"Serials"}          # efnisorð Tímarit.is, á ensku
RETTINDI = "Lýsigögnin eru frá Tímarit.is, vef Landsbókasafns Íslands – Háskólabókasafns."

# ISO 639-2 (B- og T-kóðar) → ISO 639-1. Gullna sniðið: „ISO-kóði, `is`“.
MAL = {"isl": "is", "ice": "is", "fao": "fo", "dan": "da", "kal": "kl",
       "eng": "en", "deu": "de", "ger": "de", "nor": "no", "nob": "nb",
       "nno": "nn", "swe": "sv", "fra": "fr", "fre": "fr", "lat": "la",
       "fin": "fi", "epo": "eo", "pol": "pl", "spa": "es", "ita": "it"}

# lýsingar sem segja ekkert — sleppt eins og tómum reit
TOMT = {"lýsingu vantar", "lýsing vantar", "none", "null", "n/a", "-", "?"}
_NONE = {"none", "null", "n/a", "na", "-", "–", "—", "?", "undefined", "nan"}

_SLOD = re.compile(r"^https?://(?:www\.)?timarit\.is/publication/(\d+)$")
_UTGEFANDI = re.compile(r"^(?P<nafn>.*?)[\s,]*,\s*\d{4}\s*-\s*(?:\d{4}|present)$")
_MARC = re.compile(r"\|[a-z0-9]\s+")            # MARC-deilisviðsmerki: „|b “, „|c “
_STYRITAKN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_HTML = re.compile(r"<[A-Za-z/!]|&[A-Za-z]+;|&#\d+;")
_EDTF = re.compile(r"^(\d{4})(?:/(\d{4}|\.\.))?$")
_DAGSTIMPILL = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


# ------------------------------------------------------------- smáföll
def hreinsa(s):
    """Allt bil (líka \\r, tab og \\xa0) verður eitt bil; endabil fara."""
    return " ".join((s or "").split())


def mynstur(s):
    """Ártöl út, svo óþekkt mynstur teljist saman: 'Published c. ÁÁÁÁ'."""
    return re.sub(r"\d{4}", "ÁÁÁÁ", hreinsa(s))


def tulka_utgafuar(enska):
    """Enska lýsingin → (EDTF, íslensk setning), eða None ef mynstrið er óþekkt.

    'Published from 1933 to 1948'     → ('1933/1948', 'Kom út 1933–1948.')
    'Published from 1949 to  present' → ('1949/..',   'Hefur komið út frá árinu 1949.')
    'Published in 1852 '              → ('1852',      'Kom út árið 1852.')
    """
    t = hreinsa(enska)
    m = re.match(r"^Published from (\d{4}) to (\d{4})$", t)
    if m:
        fra, til = m.group(1), m.group(2)
        if fra == til:
            return fra, "Kom út árið %s." % fra
        if fra < til:
            return "%s/%s" % (fra, til), "Kom út %s–%s." % (fra, til)
        return None                                  # öfugt bil: látið vita
    m = re.match(r"^Published from (\d{4}) to present$", t)
    if m:
        return "%s/.." % m.group(1), "Hefur komið út frá árinu %s." % m.group(1)
    m = re.match(r"^Published in (\d{4})$", t)
    if m:
        return m.group(1), "Kom út árið %s." % m.group(1)
    return None


def hreinsa_utgefanda(s):
    """'Niels Winther, 1852-1852' → 'Niels Winther'.

    Árin aftan við nafnið eru útgáfutími útgefandans hjá titlinum; þau falla
    niður (sjá README). Nafn án ártala helst óbreytt að öðru en bilum.
    """
    t = hreinsa(s)
    m = _UTGEFANDI.match(t)
    if m:
        t = m.group("nafn")
    return t.rstrip(" ,")


def mal_kodi(s):
    """'isl' → 'is', 'kal' → 'kl'. Óþekktur kóði helst óbreyttur."""
    k = hreinsa(s).lower()
    return MAL.get(k, k)


def hreinsa_lysingu(s):
    """Bil samræmd og MARC-deilisviðsmerki („|b “, „|c “) tekin út."""
    return hreinsa(_MARC.sub(" ", s or ""))


def lysing(uppruni, titill, setning):
    """Ein lýsing @is: útgáfutíminn fyrst (okkar setning), svo lýsing
    Tímarit.is. Lýsingu sem er aðeins titillinn eða „Lýsingu vantar“ er
    sleppt. Skilar (texti, hvað_varð_um_upprunann)."""
    u = hreinsa_lysingu(uppruni)
    if not u:
        stada = "tom"
    elif u.casefold() in TOMT:
        stada, u = "vantar", ""
    elif u.rstrip(" .").casefold() == hreinsa(titill).rstrip(" .").casefold():
        stada, u = "titill", ""
    else:
        stada = "marc" if _MARC.search(hreinsa(uppruni)) else "ur_heimild"
    return " ".join(h for h in (setning, u) if h), stada


def _x(s):
    return html.escape(s, quote=False)


def _el(tag, gildi, lang=None):
    if not gildi:
        return ""
    at = ' xml:lang="%s"' % lang if lang else ""
    return "      <%s%s>%s</%s>\n" % (tag, at, _x(gildi), tag)


# ------------------------------------------------------------- lestur
def lesa_svar(gogn):
    """Eitt ListRecords-svar (bæti) → {'faerslur', 'token', 'fjoldi'}.

    Hver færsla: {'id', 'datestamp', 'eydd', 'dc': [(nafn, lang, texti), …]}.
    """
    rot = ET.fromstring(gogn)
    villa = rot.find(OAI + "error")
    if villa is not None:
        raise SystemExit("OAI-villa: %s — %s" % (villa.get("code"), hreinsa(villa.text)))
    lr = rot.find(OAI + "ListRecords")
    if lr is None:
        raise SystemExit("Svarið er ekki ListRecords.")
    faerslur = []
    for r in lr.findall(OAI + "record"):
        h = r.find(OAI + "header")
        dc = []
        md = r.find(OAI + "metadata")
        if md is not None and len(md):
            dc = [(e.tag.split("}")[-1], e.get(XML_LANG), e.text or "") for e in md[0]]
        faerslur.append({"id": hreinsa(h.findtext(OAI + "identifier")),
                         "datestamp": hreinsa(h.findtext(OAI + "datestamp")),
                         "eydd": h.get("status") == "deleted", "dc": dc})
    tok = lr.find(OAI + "resumptionToken")
    token = hreinsa(tok.text) if tok is not None else ""
    fjoldi = tok.get("completeListSize") if tok is not None else None
    return {"faerslur": faerslur, "token": token,
            "fjoldi": int(fjoldi) if fjoldi and fjoldi.isdigit() else None}


def _saekja(slod, tilraunir=3):
    for n in range(tilraunir):
        try:
            beidni = urllib.request.Request(slod, headers={"User-Agent": UA})
            with urllib.request.urlopen(beidni, timeout=180) as svar:
                return svar.read()
        except Exception as villa:                   # net: reyna aftur, svo gefast upp
            if n == tilraunir - 1:
                raise SystemExit("Náðist ekki í %s: %s" % (slod, villa))
            time.sleep(1.5 * (n + 1))


def uppskera(baseurl, bid=1.0):
    """Sækir ListRecords alla leið; eltir resumptionToken ef hann birtist.
    Tímarit.is skilar öllu á einni síðu (29.9.2026), en það gæti breyst."""
    rok = {"verb": "ListRecords", "metadataPrefix": "oai_dc"}
    sidur = []
    while True:
        gogn = _saekja(baseurl + "?" + urllib.parse.urlencode(rok))
        sidur.append(gogn)
        tok = lesa_svar(gogn)["token"]
        if not tok:
            return sidur
        rok = {"verb": "ListRecords", "resumptionToken": tok}
        time.sleep(bid)


# ------------------------------------------------------------- umbreyting
def umbreyta(f, talning=None):
    """Ein færsla úr Tímarit.is → <record> í gullna sniðinu (texti)."""
    t = talning if talning is not None else _ny_talning()
    reitir = collections.defaultdict(list)
    for nafn, lang, texti in f["dc"]:
        reitir[(nafn, lang)].append(texti)
        reitir[(nafn, "*")].append(texti)

    titlar = [hreinsa(s) for s in reitir[("title", "*")] if hreinsa(s)]
    titill = titlar[0] if titlar else ""

    slodir, onnur = [], []
    for s in reitir[("identifier", "*")]:
        heim = _SLOD.match(hreinsa(s))
        if heim:
            slodir.append(SLOD_TITILS + heim.group(1))
        elif hreinsa(s):
            onnur.append(hreinsa(s))
    audkenni = list(dict.fromkeys(slodir + [f["id"]] + onnur))

    ensk = [hreinsa(s) for s in reitir[("description", "en")] if hreinsa(s)]
    dags, setning = "", ""
    for e in ensk:
        tulkad = tulka_utgafuar(e)
        if tulkad:
            dags, setning = tulkad
            t["dags"]["opid" if dags.endswith("/..") else "bil" if "/" in dags else "ar"] += 1
            break
    else:
        if ensk:
            for e in ensk:
                t["othekkt"][mynstur(e)].append(f["id"])
            t["dags"]["othekkt"] += 1
        else:
            t["dags"]["vantar"] += 1

    uppruni = " ".join(reitir[("description", "is")] + reitir[("description", None)])
    lys, stada = lysing(uppruni, titill, setning)
    t["lysing"][stada] += 1

    efni_en = []
    for s in reitir[("subject", "*")]:
        s = hreinsa(s)
        if not s:
            continue
        if s not in EFNI_EN_THEKKT:
            t["othekkt_efni"][s] += 1
        efni_en.append(s)

    mal = []
    for s in reitir[("language", "*")]:
        k = mal_kodi(s)
        if k:
            mal.append(k)
            t["mal"][k] += 1
            if len(k) != 2:
                t["othekkt_mal"][k] += 1

    utgefendur = []
    for s in reitir[("publisher", "*")]:
        if not hreinsa(s):
            continue
        t["utgefendur_inn"] += 1
        if not _UTGEFANDI.match(hreinsa(s)):
            t["utgefendur_an_ara"] += 1
        n = hreinsa_utgefanda(s)
        if n and n not in utgefendur:
            utgefendur.append(n)
    if utgefendur:
        t["med_utgefanda"] += 1
        t["utgefendur_ut"] += len(utgefendur)

    L = [_el("dc:identifier", a) for a in audkenni]
    L.append(_el("dc:title", titill, "is"))
    L += [_el("dcterms:alternative", a, "is") for a in titlar[1:]]
    L.append(_el("dc:type", TEGUND_IS, "is"))
    L.append(_el("dc:type", TEGUND_EN, "en"))
    L.append(_el("dc:date", dags))
    L.append(_el("dc:subject", EFNI_IS, "is"))
    L += [_el("dc:subject", s, "en") for s in dict.fromkeys(efni_en)]
    L.append(_el("dc:description", lys, "is"))
    L += [_el("dc:language", m) for m in dict.fromkeys(mal)]
    L += [_el("dc:publisher", u, "is") for u in utgefendur]
    L.append(_el("dc:rights", RETTINDI, "is"))

    ds = f["datestamp"]
    if re.match(r"^\d{4}-\d{2}-\d{2}$", ds):
        ds += "T00:00:00Z"
    return ("  <record>\n"
            "    <header>\n"
            "      <identifier>%s</identifier>\n"
            "      <datestamp>%s</datestamp>\n"
            "      <setSpec>%s</setSpec>\n"
            "    </header>\n"
            "    <metadata>\n"
            '<oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
            "%s</oai_dc:dc>\n"
            "    </metadata>\n"
            "  </record>\n") % (_x(f["id"]), _x(ds), SETT, "".join(L))


def _ny_talning():
    return {"dags": collections.Counter(), "othekkt": collections.defaultdict(list),
            "lysing": collections.Counter(), "othekkt_efni": collections.Counter(),
            "mal": collections.Counter(), "othekkt_mal": collections.Counter(),
            "utgefendur_inn": 0, "utgefendur_ut": 0, "utgefendur_an_ara": 0,
            "med_utgefanda": 0}


def smida(faerslur):
    """Færslur (úr lesa_svar) → (ListRecords-texti, talning)."""
    t = _ny_talning()
    texti = "<ListRecords>\n" + "".join(umbreyta(f, t) for f in faerslur) + "</ListRecords>\n"
    return texti, t


# ------------------------------------------------------------- sannprófun
def sannprofa(texti, fjoldi):
    """Skilar lista af villum (tómur = í lagi). Sömu atriði og Alma og
    gullna sniðið krefjast; skráin er ekki skrifuð ef eitthvað finnst."""
    villur = []
    if texti.startswith("<?xml"):
        villur.append("skráin byrjar á <?xml …?> — Alma-skiptirinn vill bera <ListRecords>")
    try:
        rot = ET.fromstring(texti.encode("utf-8"))
    except ET.ParseError as e:
        return ["ógilt XML: %s" % e]
    if rot.tag != "ListRecords":
        villur.append("rótin er %s, ekki ber ListRecords (án xmlns)" % rot.tag)
    faerslur = rot.findall("record")
    if len(faerslur) != fjoldi:
        villur.append("%d færslur út en %d inn" % (len(faerslur), fjoldi))
    if not faerslur or not (faerslur[0].findtext("header/identifier") or "").strip():
        villur.append("root.findall('record')[0].find('header/identifier') finnur ekkert")
    sed = set()
    for r in faerslur:
        aud = (r.findtext("header/identifier") or "").strip()
        if aud in sed:
            villur.append("tvítekið auðkenni: %s" % aud)
        sed.add(aud)
        if r.findtext("header/setSpec") != SETT:
            villur.append("%s: setSpec er ekki %s" % (aud, SETT))
        if not _DAGSTIMPILL.match(r.findtext("header/datestamp") or ""):
            villur.append("%s: datestamp á röngu formi" % aud)
        md = r.find("metadata")
        dc = md[0] if md is not None and len(md) else None
        if dc is None or dc.tag != OAI_DC + "dc" or not len(dc):
            villur.append("%s: tómt eða vantar oai_dc:dc" % aud)
            continue
        for e in dc:
            g = e.text or ""
            nafn = e.tag.split("}")[-1]
            if not g.strip() or g != g.strip():
                villur.append("%s: %s er tómur eða með endabilum" % (aud, nafn))
            elif g.casefold() in _NONE:
                villur.append("%s: %s = %r" % (aud, nafn, g))
            if _HTML.search(g):
                villur.append("%s: HTML í %s: %s" % (aud, nafn, g[:60]))
            if _STYRITAKN.search(g):
                villur.append("%s: stýritákn í %s" % (aud, nafn))

        def allt(tag, lang="*"):
            return [e.text for e in dc.findall(tag)
                    if lang == "*" or e.get(XML_LANG) == lang]
        if len(allt(DC + "title")) != 1 or len(allt(DC + "title", "is")) != 1:
            villur.append("%s: ekki nákvæmlega einn dc:title @is" % aud)
        if not any((s or "").startswith(SLOD_TITILS) for s in allt(DC + "identifier")):
            villur.append("%s: vantar slóð heim (%s…)" % (aud, SLOD_TITILS))
        if not (allt(DC + "type", "is") and allt(DC + "type", "en")):
            villur.append("%s: vantar dc:type par @is + @en" % aud)
        if not allt(DC + "subject", "is"):
            villur.append("%s: vantar dc:subject @is" % aud)
        for d in allt(DC + "date"):
            m = _EDTF.match(d or "")
            if not m or (m.group(2) and m.group(2) != ".." and m.group(1) >= m.group(2)):
                villur.append("%s: dc:date ekki á EDTF: %s" % (aud, d))
        for k in allt(DC + "language"):
            if not re.match(r"^[a-z]{2,3}$", k or ""):
                villur.append("%s: dc:language ekki ISO-kóði: %s" % (aud, k))
    return villur


# ------------------------------------------------------------- keyrsla
def _vista(slod, sidur):
    nofn = []
    stofn, ending = os.path.splitext(slod)
    for i, gogn in enumerate(sidur, 1):
        n = slod if i == 1 else "%s-%d%s" % (stofn, i, ending or ".xml")
        with open(n, "wb") as fh:
            fh.write(gogn)
        nofn.append(n)
    return nofn


def _skrifa(slod, texti):
    os.makedirs(os.path.dirname(os.path.abspath(slod)), exist_ok=True)
    with open(slod, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texti)


def main(argv=None):
    p = argparse.ArgumentParser(description="Tímarit.is (oai_dc) → gullið Dublin Core")
    p.add_argument("inntak", nargs="*",
                   help="vistuð ListRecords-svör, í röð; annars er gagnaveitan sótt")
    p.add_argument("--baseurl", default=BASEURL)
    p.add_argument("--vista", help="vista hráu svörin (hratt.xml, hratt-2.xml …)")
    p.add_argument("--ut", default=UT)
    p.add_argument("--synisveita", default=SYNISVEITA,
                   help="afrit fyrir Gáttagægi; tómur strengur = ekkert afrit")
    a = p.parse_args(argv)

    if a.inntak:
        sidur = []
        for slod in a.inntak:
            with open(slod, "rb") as fh:
                sidur.append(fh.read())
        uppruni = ", ".join(a.inntak)
    else:
        sidur = uppskera(a.baseurl)
        uppruni = a.baseurl
        if a.vista:
            print("Vistað hrátt: %s" % ", ".join(_vista(a.vista, sidur)))

    lesid = [lesa_svar(g) for g in sidur]
    if lesid[-1]["token"]:
        sys.exit("Síðasta svarið ber resumptionToken — vistaða inntakið er ekki heilt. "
                 "Keyrðu án inntaks til að sækja allt.")
    allar = [f for s in lesid for f in s["faerslur"]]
    uppgefid = next((s["fjoldi"] for s in lesid if s["fjoldi"] is not None), None)
    if uppgefid is not None and uppgefid != len(allar):
        print("⚠ completeListSize=%d en %d færslur bárust" % (uppgefid, len(allar)))
    eyddar = sum(1 for f in allar if f["eydd"])
    einstakar, sed = [], set()
    for f in allar:
        if f["eydd"] or f["id"] in sed:
            continue
        sed.add(f["id"])
        einstakar.append(f)
    tvitok = len(allar) - eyddar - len(einstakar)

    texti, t = smida(einstakar)
    villur = sannprofa(texti, len(einstakar))
    if villur:
        for v in villur[:40]:
            print("✗ " + v)
        sys.exit("Sannprófun brást (%d atriði) — ekkert skrifað." % len(villur))

    _skrifa(a.ut, texti)
    if a.synisveita:
        _skrifa(a.synisveita, texti)

    print("Inn: %d færslur úr %s (%d síða/síður) · eyddar %d · tvítök %d"
          % (len(allar), uppruni, len(sidur), eyddar, tvitok))
    print("Út:  %d færslur → %s (%d kB)" % (len(einstakar), a.ut, len(texti.encode("utf-8")) // 1024))
    if a.synisveita:
        print("Afrit: %s" % a.synisveita)
    d = t["dags"]
    print("dc:date: bil %d · eitt ár %d · opið bil %d · óþekkt %d · engin ensk lýsing %d"
          % (d["bil"], d["ar"], d["opid"], d["othekkt"], d["vantar"]))
    if t["othekkt"]:
        print("Óþekkt mynstur í enskri lýsingu (%d):" % len(t["othekkt"]))
        for m, ids in sorted(t["othekkt"].items(), key=lambda kv: -len(kv[1])):
            print("  %4d  %r  t.d. %s" % (len(ids), m, ", ".join(ids[:3])))
    else:
        print("Óþekkt mynstur í enskri lýsingu: engin")
    ly = t["lysing"]
    print("Lýsing @is úr heimild: %d óbreytt · %d með MARC-merkjum hreinsuðum · "
          "sleppt: %d aðeins titillinn · %d „Lýsingu vantar“ · %d tóm"
          % (ly["ur_heimild"], ly["marc"], ly["titill"], ly["vantar"], ly["tom"]))
    print("dc:language: %s" % " · ".join("%s %d" % kv for kv in t["mal"].most_common()))
    if t["othekkt_mal"]:
        print("⚠ tungumálskóðar án ISO 639-1: %s" % dict(t["othekkt_mal"]))
    if t["othekkt_efni"]:
        print("⚠ óþekkt efnisorð (haldið @en): %s" % dict(t["othekkt_efni"]))
    print("dc:publisher: %d gildi inn í %d færslum → %d út (%d án ártala í heimild)"
          % (t["utgefendur_inn"], t["med_utgefanda"], t["utgefendur_ut"], t["utgefendur_an_ara"]))
    print("Sannprófað: gilt XML · ber <ListRecords> án xmlns og án <?xml?> · "
          "fyrsta header/identifier = %s · engir tómir reitir, None né HTML"
          % einstakar[0]["id"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

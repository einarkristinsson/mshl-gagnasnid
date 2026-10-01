#!/usr/bin/env python3
"""Listasafn Íslands → gullna sniðið (sýningar og listamannasíður).

Vefur Listasafns (listasafn.is) er byggður á Prismic og efnið er opið í
vefþjónustu þess: https://listasafn-islands.cdn.prismic.io/api/v2. Þaðan er
lesið, ekki skafið af vefsíðum. Ekkert þarf að breyta hjá Listasafni.

Færslur:
  - sýning (Prismic `exhibition`, íslenska): titill, dagsetningar, safn,
    listamenn, lýsing, mynd. Slóð heim: https://www.listasafn.is/list/syningar/<uid>/
  - listamaður (`art_artist_page`): nafn, æviár, inngangur, mynd, Sarpsnúmer.
    Slóð heim: https://www.listasafn.is/list/listamenn/<uid>/
  Verk (`artwork`, 1.139) bera aðeins titil og stundum mynd — sleppt í bili.

Reiturinn `artist` á sýningu er stundum listamaður („James Merry“) og stundum
flokkur eða undirtitill („Samsýning“, „Íslensk grafík“). Hann verður höfundur
aðeins ef hann lítur út eins og nöfn: engin lágstafaorð og ekki á FLOKKAR.
Annars verður hann `dcterms:alternative`. Listamannalisti sýningar
(slice `artist_list`) er traustasta heimildin og bætist alltaf við.

    /usr/bin/python3 byggja_listasafn_dc.py                 # sækir og smíðar
    /usr/bin/python3 byggja_listasafn_dc.py --vista hratt.json
    /usr/bin/python3 byggja_listasafn_dc.py hratt.json      # smíðar úr vistuðu
"""
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HER = os.path.dirname(os.path.abspath(__file__))
ROT = os.path.abspath(os.path.join(HER, "..", ".."))
UT = os.path.join(HER, "LISTASAFN-tryA.xml")
UT_SYNI = os.path.join(ROT, "verkfaeri", "gattagaegir", "synisveitur", "listasafn.xml")
API = "https://listasafn-islands.cdn.prismic.io/api/v2"
VEFUR = "https://www.listasafn.is"
OAI = "oai:listasafn.is:"
HAUS = {"User-Agent": "MSHL Sagnatrog (einar@kann.is)"}

# Heiti safna úr Prismic (`visit-museum-page`); „Listasafnið“ er aðalhúsið við Tjörnina.
SOFN = {
    "listasafnid": "Listasafnið við Tjörnina",
    "safnahusid": "Safnahúsið",
    "hus-asgrims-jonssonar": "Hús Ásgríms Jónssonar",
    "listasafn-einars-jonssonar": "Listasafn Einars Jónssonar",
    "safnasafnið": "Safnasafnið á Svalbarðseyri",
    "isafjordur": "Listasafn Ísafjarðar",
    "skaftfell-seydisfjordur": "Skaftfell listamiðstöð á Austurlandi",
    "listasafn-reykjavikur": "Listasafn Reykjavíkur",
}
# Gildi í `artist` sem eru flokkar, ekki listamenn (eitt orð með hástaf er annars nafn: Steina, Rúrí)
FLOKKAR = {"samsýning", "safneignarsýning"}
TENGIORD = {"og", "&", "/", "–", "-", "van", "de", "von", "der", "da", "di", "la", "le"}


def _saekja(slod):
    for _ in range(4):
        try:
            time.sleep(0.3)
            with urllib.request.urlopen(urllib.request.Request(slod, headers=HAUS), timeout=60) as r:
                return json.load(r)
        except OSError:
            time.sleep(3)
    raise RuntimeError("náði ekki: " + slod)


def saekja_allt():
    ref = next(r["ref"] for r in _saekja(API)["refs"] if r.get("isMasterRef"))
    ut = {}
    for teg in ("exhibition", "art_artist_page"):
        sida, ut[teg] = 1, []
        while True:
            q = urllib.parse.urlencode({"ref": ref, "q": '[[at(document.type,"%s")]]' % teg,
                                        "pageSize": 100, "page": sida, "lang": "is"})
            r = _saekja(API + "/documents/search?" + q)
            ut[teg] += r["results"]
            if sida >= r["total_pages"]:
                break
            sida += 1
    return ut


# ---------------------------------------------------------------- hreinsun
def texti_ur_rich(rich):
    """Prismic rich text → hreinn texti, málsgreinar aðgreindar með auðri línu."""
    if not isinstance(rich, list):
        return ""
    return "\n\n".join(" ".join((b.get("text") or "").split()) for b in rich
                       if isinstance(b, dict) and (b.get("text") or "").strip())


def lysing_syningar(gogn):
    hlutar = []
    for sl in gogn.get("slices") or []:
        if sl.get("slice_type") in ("text", "text_and_image"):
            t = texti_ur_rich((sl.get("primary") or {}).get("text"))
            if t:
                hlutar.append(t)
    return "\n\n".join(hlutar).strip()


def er_nafnastrengur(s):
    """'James Merry' · 'Chantal Joffe, Gauthier Hubert og Tumi Magnússon' → True;
    'Samsýning' · 'Íslensk grafík' · 'Þar sem ljósið lifir' → False."""
    s = " ".join((s or "").split())
    if not s or s.casefold() in FLOKKAR:
        return False
    if s == s.lower() and " " not in s:          # „björk“ — einnefni í lágstöfum
        return True
    for ord_ in re.split(r"[\s,]+", s):
        if not ord_ or ord_.casefold() in TENGIORD:
            continue
        if ord_[0].islower():
            return False
    return True


def nofn_ur_streng(s):
    """'A, B og C' · 'A & B' · 'A\\nB' → ['A', 'B', 'C']; 'A / Alias' → ['A (Alias)']."""
    s = (s or "").strip()
    if " / " in s and "\n" not in s and "," not in s:
        a, b = [x.strip() for x in s.split(" / ", 1)]
        return ["%s (%s)" % (a, b)]
    # kommur innan sviga („Elina Brotherus (Finnish, 1972)“) skipta ekki nöfnum
    s = re.sub(r"\(([^()]*)\)", lambda m: "(" + m.group(1).replace(",", "\u0001") + ")", s)
    hlutar = re.split(r"\s*(?:,|\n|\s&\s|\s&amp;\s|\sog\s)\s*", s)
    return [" ".join(h.replace("\u0001", ",").split()) for h in hlutar if h.strip()]


def hreinsa_nafn(n, talning=None):
    """Æviár aðeins ef dánarár er skráð (sama regla og hjá RÚV):
    'Ragnar Axelsson - RAX (1958)' → 'Ragnar Axelsson - RAX' · 'Sölvi Helgason (1820−1895)' → '… (1820-1895)'.
    'Óþekktur listamaður …' → None (ekki manneskja)."""
    n = " ".join((n or "").split())
    if not n or n.casefold().startswith("óþekktur listamaður"):
        return None
    m = re.match(r"^(.*?)\s*\((?:[^()\d]*,\s*)?(\d{4})\s*[-–−]\s*(\d{4})\s*\)\s*$", n)
    if m:
        return "%s (%s-%s)" % (m.group(1), m.group(2), m.group(3))
    m = re.match(r"^(.*?)\s*\((?:[^()\d]*,\s*)?(?:f\.\s*)?\d{4}\s*[-–−]?\s*\)\s*$", n)
    if m:
        if talning is not None:
            talning["aeviar_lifandi"] += 1
        return m.group(1).strip()
    return n


def dags(s):
    return s if re.match(r"^\d{4}-\d{2}-\d{2}$", s or "") else ""


def myndaslod(mynd):
    """Prismic-mynd → smámynd 400 px (myndþjónusta Prismic/imgix)."""
    url = (mynd or {}).get("url") or ""
    if not url:
        return ""
    grunnur = url.split("?", 1)[0]
    return grunnur + "?auto=format,compress&w=400"


def x(s):
    return html.escape(str(s), quote=False)


def el(tag, val, **at):
    if val in (None, ""):
        return ""
    nofn = {"xml_lang": "xml:lang", "xsi_type": "xsi:type", "mshl_role": "mshl:role"}
    a = "".join(' %s="%s"' % (nofn.get(k, k), html.escape(v, quote=True)) for k, v in at.items() if v)
    return "      <%s%s>%s</%s>\n" % (tag, a, x(val), tag)


def faersla(aud, datestamp, sett, linur):
    return ("  <record>\n    <header>\n      <identifier>%s</identifier>\n"
            "      <datestamp>%s</datestamp>\n      <setSpec>source:listasafn</setSpec>\n"
            "      <setSpec>%s</setSpec>\n    </header>\n    <metadata>\n"
            '<oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:mshl="https://mshl.is/terms#">\n'
            "%s</oai_dc:dc>\n    </metadata>\n  </record>\n") % (x(aud), datestamp, sett, "".join(linur))


def uidk(doc):
    """Auðkenni Prismic í slóð: íslenskir stafir hlutfallskóðaðir (sýningin „…-ð-…“)."""
    return urllib.parse.quote(doc["uid"], safe="-_.~")


def stimpill(doc):
    return (doc.get("last_publication_date") or "2026-10-01T00:00:00")[:19].replace("+0000", "") + "Z"


# ---------------------------------------------------------------- færslur
def syning(doc, talning):
    g = doc["data"]
    uid = uidk(doc)
    titill = " ".join((g.get("title") or "").split())
    if not titill:
        talning["slepptar"] += 1
        return ""
    yfir = " ".join((g.get("artist") or "").split())
    hofundar = []
    if yfir and er_nafnastrengur(g.get("artist")):
        hofundar += nofn_ur_streng(g.get("artist"))
        yfir_sem_undirtitill = ""
    else:
        yfir_sem_undirtitill = yfir
    for sl in g.get("slices") or []:
        if sl.get("slice_type") == "artist_list":
            for it in sl.get("items") or []:
                hofundar += nofn_ur_streng(it.get("name"))
    sedd, hof = set(), []
    for h in hofundar:
        h = hreinsa_nafn(h, talning)
        if h and h.casefold() not in sedd:
            sedd.add(h.casefold())
            hof.append(h)
    talning["hofundar"] += len(hof)
    if yfir_sem_undirtitill:
        talning["undirtitlar"] += 1
    upphaf, lok = dags(g.get("start_date")), dags(g.get("end_date"))
    safn = SOFN.get((g.get("museum") or {}).get("uid") or "", "")
    mynd = myndaslod(g.get("image"))
    L = [el("dc:identifier", "%s/list/syningar/%s/" % (VEFUR, uid)),
         el("dc:identifier", mynd),
         el("dc:identifier", OAI + "syning:" + uid),
         el("dc:title", titill, xml_lang="is"),
         el("dcterms:alternative", yfir_sem_undirtitill, xml_lang="is"),
         el("dc:type", "Sýning", xml_lang="is"),
         el("dc:type", "Event", xml_lang="en"),
         el("dc:date", "%s/%s" % (upphaf, lok) if upphaf and lok else (upphaf or lok))]
    for h in hof:
        L.append(el("dc:creator", h, mshl_role="listamaður"))
        L.append(el("dcterms:bibliographicCitation", "%s (listamaður)" % h, xml_lang="is"))
    L.append(el("dc:subject", "Myndlistarsýningar", xml_lang="is"))
    for k in re.split(r"[,\n]+", g.get("keywords") or ""):
        k = " ".join(k.split()).strip(" .")
        # aðeins efnisorð (lágstafur fremst); nöfn og ártöl eru í öðrum reitum
        if k and k[0].islower() and not re.search(r"\d", k) and len(k) <= 40:
            L.append(el("dc:subject", k, xml_lang="is"))
    L.append(el("dc:description", lysing_syningar(g), xml_lang="is"))
    L.append(el("dc:coverage", safn, xml_lang="is"))
    L += [el("dc:publisher", "Listasafn Íslands", xml_lang="is"),
          el("dc:language", "is"),
          el("dc:rights", "Lýsigögn: Listasafn Íslands. Myndir af verkum eru háðar höfundarrétti listamanna.",
             xml_lang="is")]
    talning["syningar"] += 1
    if mynd:
        talning["myndir"] += 1
    return faersla(OAI + "syning:" + uid, stimpill(doc), "type:syning", L)


def listamadur(doc, talning):
    g = doc["data"]
    uid = uidk(doc)
    nafn = " ".join((g.get("title") or "").split())
    if not nafn:
        talning["slepptar"] += 1
        return ""
    fd, dd = dags(g.get("date_of_birth")), dags(g.get("date_of_death"))
    inngangur = " ".join((g.get("intro") or "").split())
    meginmal = "\n\n".join(texti_ur_rich((sl.get("primary") or {}).get("text"))
                           for sl in g.get("slices") or [] if (sl.get("primary") or {}).get("text"))
    mynd = myndaslod(g.get("image"))
    L = [el("dc:identifier", "%s/list/listamenn/%s/" % (VEFUR, uid)),
         el("dc:identifier", mynd),
         el("dc:identifier", OAI + "listamadur:" + uid),
         el("dc:title", nafn, xml_lang="is"),
         el("dc:type", "Einstaklingur", xml_lang="is"),
         el("dc:type", "Person", xml_lang="en"),
         el("dc:date", "%s/%s" % (fd[:4], dd[:4]) if fd and dd else fd[:4]),
         el("dcterms:temporal", "%s – %s" % (fd, dd) if fd and dd else fd, xml_lang="is"),
         el("dc:subject", "Myndlistarmenn", xml_lang="is"),
         el("dc:description", "\n\n".join(t for t in (inngangur, meginmal.strip()) if t), xml_lang="is"),
         el("dc:relation", ("Sarpur, aðili %s" % g["sarpur_id"]) if g.get("sarpur_id") else "", xml_lang="is"),
         el("dc:publisher", "Listasafn Íslands", xml_lang="is"),
         el("dc:language", "is"),
         el("dc:rights", "Lýsigögn: Listasafn Íslands. Myndir af verkum eru háðar höfundarrétti listamanna.",
            xml_lang="is")]
    talning["listamenn"] += 1
    if mynd:
        talning["myndir"] += 1
    return faersla(OAI + "listamadur:" + uid, stimpill(doc), "type:listamadur", L)


def smida(hratt):
    talning = {"syningar": 0, "listamenn": 0, "myndir": 0, "hofundar": 0, "undirtitlar": 0, "slepptar": 0,
               "aeviar_lifandi": 0}
    linur = [syning(d, talning) for d in sorted(hratt["exhibition"], key=lambda d: d["uid"])]
    linur += [listamadur(d, talning) for d in sorted(hratt["art_artist_page"], key=lambda d: d["uid"])]
    texti = "<ListRecords>\n" + "".join(linur) + "</ListRecords>\n"
    rot = ET.fromstring(texti.encode("utf-8"))
    assert rot.findall("record")[0].find("header/identifier").text
    assert len(rot.findall("record")) == talning["syningar"] + talning["listamenn"]
    assert "None" not in re.findall(r">([^<]*)<", texti)
    return texti, talning


def main(argv):
    vista = None
    if "--vista" in argv:
        vista = argv[argv.index("--vista") + 1]
        argv = [a for a in argv if a not in ("--vista", vista)]
    if argv:
        hratt = json.load(open(argv[0], encoding="utf-8"))
    else:
        hratt = saekja_allt()
    if vista:
        json.dump(hratt, open(vista, "w", encoding="utf-8"), ensure_ascii=False)
    texti, t = smida(hratt)
    for slod in (UT, UT_SYNI):
        os.makedirs(os.path.dirname(slod), exist_ok=True)
        open(slod, "w", encoding="utf-8").write(texti)
    print("Sýningar: %(syningar)d · listamenn: %(listamenn)d · með mynd: %(myndir)d · "
          "höfundatengsl: %(hofundar)d · undirtitlar (artist ekki nafn): %(undirtitlar)d · "
          "fæðingarár lifandi fjarlægð: %(aeviar_lifandi)d · sleppt: %(slepptar)d" % t)
    print("Skrifað:", os.path.relpath(UT, ROT), "og", os.path.relpath(UT_SYNI, ROT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

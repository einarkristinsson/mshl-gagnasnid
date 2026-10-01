#!/usr/bin/env python3
"""byggja_baekur_dc.py — Bækur.is (OAI-PMH, edm) → gullið Dublin Core.

Bækur.is (Landsbókasafn Íslands – Háskólabókasafn) á opna OAI-PMH gagnaveitu
á https://baekur.is/oai með tveimur sniðum, `oai_dc` og `edm`. Við sækjum
`edm`: þar eru höfundar með æviárum, land, smámynd, réttindi og tilvísun í
Bókaskrá, en `oai_dc` ber fátt af því. Hver færsla er ein stafræn bók.

Forritið sækir alla gagnaveituna (eða les vistuð svör), færir hana í gullna
sniðið (snidmat/GULLNA-SNIDID.md), sannprófar og skrifar:

    gagnaveitur/baekur/BAEKUR-tryA.xml            í git; fer í Upload File/s í Alma
    verkfaeri/gattagaegir/synisveitur/baekur.xml  sama skrá; sýnisveita (utan git)

Sniðið sem Alma tekur við: ber <ListRecords> án xmlns og án <?xml …?>-línu;
nafnrýmin eru á hverju <oai_dc:dc>. Kortlagningin og rökin fyrir henni eru í
README.md hér við hliðina. Ekkert er skrifað ef sannprófunin bregst.

Keyrsla (Python 3.9+, engin ytri söfn):
    python3 byggja_baekur_dc.py                  # sækir gagnaveituna (~120 síður, ~3 mín.)
    python3 byggja_baekur_dc.py --vista hratt/   # sækir og vistar hráu síðurnar
    python3 byggja_baekur_dc.py hratt/           # les vistaðar síður (mappa eða skrár, í röð)
"""
import argparse
import collections
import glob
import html
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HER = os.path.dirname(os.path.abspath(__file__))
ROT = os.path.abspath(os.path.join(HER, "..", ".."))
UT = os.path.join(HER, "BAEKUR-tryA.xml")
SYNISVEITA = os.path.join(ROT, "verkfaeri", "gattagaegir", "synisveitur", "baekur.xml")

# Identify auglýsir http://baekur.is/oai, sem fer í 301 hingað. POST svarar 403.
BASEURL = "https://baekur.is/oai"
SNID = "edm"
UA = "MSHL-Sagnatrog harvest (einar@kann.is)"
SETT = "source:baekur"

# Slóðir (mælt 1.10.2026):
#  - bókin: https svarar 200. Bækur.is gefur sjálf slóðina án nafnhluta
#    (/bok/<uuid>) sem `url` í schema.org-lýsingu síðunnar; nafnhlutinn
#    (/bok/<uuid>/Biblia) getur breyst ef titli er breytt.
#  - smámynd: /cover/tbn/<uuid> er `thumbnailUrl` síðunnar og sama slóð og
#    Bókaskrá Landsbókasafns notar. Svarar 302 á /skra/JPG/<n> (image/jpeg,
#    200 px á breidd, 4–14 kB). /cover/<uuid> (edm:object) er mynd í fullri
#    stærð, 2.468 px og 280 kB.
SLOD_BOKAR = "https://baekur.is/bok/"
SLOD_SMAMYNDAR = "https://baekur.is/cover/tbn/"
SLOD_BOKASKRAR = "https://bokaskra.landsbokasafn.is/search?s_any="

OAI = "{http://www.openarchives.org/OAI/2.0/}"
OAI_DC = "{http://www.openarchives.org/OAI/2.0/oai_dc/}"
RDF = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
EDM = "{http://www.europeana.eu/schemas/edm/}"
ORE = "{http://www.openarchives.org/ore/terms/}"
SKOS = "{http://www.w3.org/2004/02/skos/core#}"
DC = "{http://purl.org/dc/elements/1.1/}"
DCT = "{http://purl.org/dc/terms/}"
MSHL = "{https://mshl.is/terms#}"
XSI = "{http://www.w3.org/2001/XMLSchema-instance}"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

TEGUND_IS = "Bók"
TEGUND_EN = "Text"
EFNI_IS = "Bækur"                     # fast efnisorð á öllum (eins og „Tímarit og blöð“)
UTGEFANDI = "Landsbókasafn Íslands – Háskólabókasafn"
TILVISUN = "Bókaskrá Landsbókasafns"
HLUTVERK = "höfundur"                 # Bækur.is merkir alla „Höfundur“ á bókarsíðunni
STADARHLUTVERK = "útgáfustaður"       # LoC-landakóðinn er útgáfuland (MARC 008)

# ---- land: Bækur.is gefur landið tvisvar, sem LoC-kóða og GeoNames-auðkenni.
# Landið er aðeins skráð þegar hvort tveggja segir sama land. Þar sem
# LoC-kóðinn er `null` eða `xx` setur Bækur.is Ísland í GeoNames — það er
# sjálfgefið gildi, ekki upplýsing (296 + 5 bækur 1.10.2026).
LOND_LOC = {"ic": "Ísland", "dk": "Danmörk", "gw": "Þýskaland", "sw": "Svíþjóð",
            "enk": "Bretland", "stk": "Bretland", "xxk": "Bretland", "no": "Noregur",
            "fr": "Frakkland", "xxu": "Bandaríkin", "ne": "Holland", "xxc": "Kanada",
            "fi": "Finnland", "sz": "Sviss", "au": "Austurríki", "it": "Ítalía",
            "pl": "Pólland", "ie": "Írland"}
LOND_GEONAMES = {"2629691": "Ísland", "2623032": "Danmörk", "2921044": "Þýskaland",
                 "2661886": "Svíþjóð", "2635167": "Bretland", "3144096": "Noregur",
                 "3017382": "Frakkland", "6252001": "Bandaríkin", "2750405": "Holland",
                 "6251999": "Kanada", "660013": "Finnland", "2658434": "Sviss",
                 "2782113": "Austurríki", "3175395": "Ítalía", "798544": "Pólland",
                 "2963597": "Írland"}
OTHEKKT_LOC = {"null", "xx"}

# ---- réttindi: rightsstatements.org og Creative Commons → íslenskt heiti + slóð
RETTINDI_RS = {"InC": "Höfundarréttur í gildi",
               "NoC-US": "Ekki höfundarréttur í Bandaríkjunum",
               "CNE": "Höfundarréttur ekki metinn",
               "UND": "Höfundarréttur óljós",
               "NKC": "Enginn þekktur höfundarréttur"}
RETTINDI_CC = {"publicdomain/mark": "Almenningseign",
               "publicdomain/zero": "Afsal höfundarréttar (CC0)"}

# ---- fólk, stofnanir og verk. Bækur.is setur öll þrjú í dc:creator.
# Stofnanir: félög, söfn, sjóðir, nefndir, skólar, dómstólar, sýningar, og
# lönd sem gefa út lög („Ísland“ á 198 bókum, flestum tilskipunum).
_STOFNUN = re.compile(
    r"(félag|safn\b|safnið|sjóð|nefnd|stofnun|stiftun|skól|spítal|sýning|hreyfing|"
    r"klúbb|listahátíð|bandalag|rétturinn|amtið|listamenn|kvennalistinn|triennal|"
    r"udstilling|kunst|taidetta|selskab|f[oö]rbund|institut|bibliotek|council|"
    r"federation|association)", re.IGNORECASE)
STOFNANIR = {"Ísland", "Danmörk", "Íslenskar kvennarannsóknir", "Det Stærke lys",
             "Islandsk farvespil", "Höggmyndir á þjóðhátíðarári"}
# Verk (samræmdir titlar): sögur, þættir, kvæði, lögbækur, Biblían …
_VERK = re.compile(
    r"(\bsaga\b|\bsögur\b|\bþáttur\b|kviða$|kvæði$|bók$|bókin$|lög$|ljóð$|mál$|"
    r"annálar|kristinréttur|^biblían$|^handbók)", re.IGNORECASE)
VERK = {"Rímbegla", "Fagurskinna", "Munkalíf", "Chronica Danorum",
        "Þúsund og ein nótt", "Hátta-Lykill Lopts ríka Guttormssonar"}

_NONE = {"none", "null", "n/a", "na", "-", "–", "—", "?", "undefined", "nan"}
_UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
_AR = re.compile(r"^\d{3,4}$")
_ISBD = re.compile(r"\s+[=/;:]$")
_STYRITAKN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_HTML = re.compile(r"<[A-Za-z/!]|&[A-Za-z]+;|&#\d+;")
_EDTF = re.compile(r"^\d{4}(?:/\d{4})?$")
_DAGSTIMPILL = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_MAL3 = {"isl": "is", "ice": "is", "dan": "da", "lat": "la", "eng": "en", "swe": "sv",
         "deu": "de", "ger": "de", "fra": "fr", "fre": "fr", "nor": "no", "nob": "nb",
         "dut": "nl", "nld": "nl", "gre": "el", "ell": "el", "est": "et", "fin": "fi",
         "kal": "kl", "ita": "it", "fao": "fo"}


# ------------------------------------------------------------- smáföll
def hreinsa(s):
    """Allt bil (líka \\r, tab og \\xa0) verður eitt bil; endabil fara."""
    return " ".join((s or "").split())


def hreinsa_titil(s):
    """ISBD-tákn aftast fara: 'Íslenzk list =' → 'Íslenzk list'.

    Aðeins =, /, ; og : með bili á undan — þá er titillinn slitinn á undan
    samhliða titli eða ábyrgðaraðild. Punktur aftast helst, því hann getur
    verið hluti skammstöfunar („o.fl.“, „R. af D.“)."""
    return _ISBD.sub("", hreinsa(s))


def flokka(nafn, fra=None, til=None):
    """Hvað er þessi „höfundur“? → 'persona', 'stofnun' eða 'verk'.

    Röðin skiptir máli: stofnun fyrst (líka „Nordisk textiltriennal“ sem
    ber upphafsár), svo ár eða komma (öfugt nafn: „Luther, Martin,“) =
    manneskja, svo samræmdur titill. Annað telst manneskja („Jón Einarsson“,
    „Laozi“). Forritið prentar allar stofnanir og öll verk sem það finnur.
    """
    n = hreinsa(nafn)
    hreint = n.rstrip(" .,")
    if hreint in STOFNANIR or _STOFNUN.search(n):
        return "stofnun"
    if fra or til or "," in n:
        return "persona"
    if hreint in VERK or _VERK.search(hreint) or n.endswith("."):
        return "verk"
    return "persona"


def hreinsa_nafn(nafn, flokkur):
    """Greinarmerki úr bókfræðifærslunni aftast fara.

    Manneskja: aðeins komman („Luther, Martin,“ → „Luther, Martin“), því
    punktur aftast er oft upphafsstafur („Ferrall, J. S.“).
    Stofnun og verk: líka punktur („Eddukvæði.“ → „Eddukvæði“)."""
    n = hreinsa(nafn)
    return n.rstrip(" ,") if flokkur == "persona" else n.rstrip(" ,.")


def aeviar(fra, til):
    """'(1614-1674)' ef bæði árin eru heil ártöl, annars ''.

    Eitt ár dugar ekki: upphafsár án dánarárs getur verið fæðingarár
    lifandi manneskju (sama regla og hjá RÚV). '-180' (áratugur óþekktur)
    telst ekki ár."""
    fra, til = hreinsa(fra), hreinsa(til)
    if _AR.match(fra) and _AR.match(til):
        return "(%s-%s)" % (fra, til)
    return ""


def nafn_med_arum(nafn, fra, til):
    """'Hallgrímur Pétursson' + 1614, 1674 → 'Hallgrímur Pétursson (1614-1674)'."""
    ar = aeviar(fra, til)
    return "%s %s" % (nafn, ar) if ar else nafn


def land(slodir):
    """dcterms:spatial-slóðir einnar bókar → (lönd á íslensku, staða).

    Staða: 'samhljoda' (LoC og GeoNames segja sama land), 'othekkt' (LoC
    `null`/`xx`), 'osamraemi' (ólík lönd, eða land utan töflunnar) eða
    'vantar'. Aðeins 'samhljoda' gefur land."""
    loc, geo = [], []
    for s in slodir:
        s = hreinsa(s).rstrip("/")
        if "id.loc.gov/vocabulary/countries/" in s:
            loc.append(s.rsplit("/", 1)[1])
        elif "geonames.org/" in s:
            geo.append(s.rsplit("/", 1)[1])
    if not loc and not geo:
        return [], "vantar"
    if loc and all(k in OTHEKKT_LOC for k in loc):
        return [], "othekkt"
    nofn_loc = {LOND_LOC.get(k) for k in loc if k not in OTHEKKT_LOC} - {None}
    nofn_geo = {LOND_GEONAMES.get(g) for g in geo} - {None}
    sameig = sorted(nofn_loc & nofn_geo)
    if sameig:
        return sameig, "samhljoda"
    return [], "osamraemi"


def rettindi(uri):
    """edm:rights → (íslenskt heiti eða None, stöðluð slóð).

    rightsstatements.org: 'page'-slóðin (fyrir fólk) verður 'vocab'-slóðin,
    sem er auðkenni yfirlýsingarinnar og vísar á síðuna."""
    u = hreinsa(uri)
    m = re.match(r"^https?://rightsstatements\.org/(?:page|vocab)/([A-Za-z-]+)/([\d.]+)/?", u)
    if m:
        return (RETTINDI_RS.get(m.group(1)),
                "http://rightsstatements.org/vocab/%s/%s/" % (m.group(1), m.group(2)))
    m = re.match(r"^https?://creativecommons\.org/(publicdomain/(?:mark|zero))/([\d.]+)/?", u)
    if m:
        return RETTINDI_CC.get(m.group(1)), "https://creativecommons.org/%s/%s/" % m.groups()
    return None, u


def umfang(s):
    """'730 p.' → '730 síður í stafrænu eintaki'; '21 p.' → '21 síða …'.

    Talan er fjöldi mynda í stafræna eintakinu, með bandi, saurblöðum og
    litaspjaldi: Biblía 1859 er 1122 í straumnum en „Blaðsíður 1118“ á
    bókarsíðunni. „bls.“ myndi lesast sem blaðsíðutal prentuðu bókarinnar."""
    m = re.match(r"^(\d+)\s*p\.?$", hreinsa(s))
    if not m or int(m.group(1)) == 0:
        return None
    n = int(m.group(1))
    ord_ = "síða" if n % 10 == 1 and n % 100 != 11 else "síður"
    return "%d %s í stafrænu eintaki" % (n, ord_)


_STAFROF = "0123456789aábcdðeéfghiíjklmnoópqrstuúvwxyýzþæö"
_RAD = {c: i for i, c in enumerate(_STAFROF)}
_RAD.update({"ø": _RAD["ö"], "ä": _RAD["æ"], "å": _RAD["á"], "ü": _RAD["ý"]})


def islensk_rod(s):
    """Röðunarlykill í íslenskri stafrófsröð: Á á eftir A, Þ Æ Ö aftast.

    Bækur.is skilar efnisorðum hverrar bókar í nýrri röð við hverja
    uppskeru (mælt 29.9 og 1.10.2026); röðun gerir afurðina stöðuga."""
    return ([_RAD.get(c, 100 + ord(c)) for c in s.casefold()], s)


def mal_kodi(s):
    """'is' helst; 'isl' → 'is'. Óþekktur kóði helst óbreyttur."""
    k = hreinsa(s).lower()
    return _MAL3.get(k, k)


def _x(s):
    return html.escape(s, quote=False)


def _el(tag, gildi, lang=None, **eigindi):
    if not gildi:
        return ""
    at = "".join(' %s="%s"' % (k.replace("__", ":"), html.escape(v, quote=True))
                 for k, v in eigindi.items() if v)
    if lang:
        at += ' xml:lang="%s"' % lang
    return "      <%s%s>%s</%s>\n" % (tag, at, _x(gildi), tag)


# ------------------------------------------------------------- lestur
def _texti(e):
    return hreinsa(e.text) if e is not None else ""


def _res(e):
    return hreinsa(e.get(RDF + "resource")) if e is not None else ""


def lesa_faerslu(rec):
    """Ein <record> úr edm-svari → orðabók með því sem umbreytingin þarf."""
    h = rec.find(OAI + "header")
    f = {"id": hreinsa(h.findtext(OAI + "identifier")),
         "datestamp": hreinsa(h.findtext(OAI + "datestamp")),
         "eydd": h.get("status") == "deleted",
         "titlar": [], "dags": [], "mal": [], "umfang": [], "efni": [],
         "hofundar": [], "stadir": [], "rettindi": [], "tilvisanir": [],
         "slodir": [], "synt": "", "mynd": "", "agentar": {}, "annad": []}
    md = rec.find(OAI + "metadata")
    if md is None or not len(md):
        return f
    rdf = md[0]
    cho = rdf.find(EDM + "ProvidedCHO")
    for a in rdf.findall(EDM + "Agent"):
        f["agentar"][a.get(RDF + "about")] = {
            "nafn": _texti(a.find(SKOS + "prefLabel")),
            "fra": _texti(a.find(EDM + "begin")), "til": _texti(a.find(EDM + "end"))}
    agg = rdf.find(ORE + "Aggregation")
    if agg is not None:
        f["synt"] = _res(agg.find(EDM + "isShownAt"))
        f["mynd"] = _res(agg.find(EDM + "object"))
    if cho is None:
        return f
    for e in cho:
        nafn = e.tag
        if nafn == DC + "title":
            f["titlar"].append(_texti(e))
        elif nafn == DC + "date":
            f["dags"].append(_texti(e))
        elif nafn == DC + "language":
            f["mal"].append(_texti(e))
        elif nafn == DCT + "extent":
            f["umfang"].append(_texti(e))
        elif nafn == DC + "subject":
            f["efni"].append((e.get(XML_LANG), _texti(e)))
        elif nafn in (DC + "creator", DC + "contributor"):
            # oftast rdf:resource á edm:Agent; stundum gæti nafnið staðið sem texti
            f["hofundar"].append((_res(e), _texti(e)))
        elif nafn == DCT + "spatial":
            f["stadir"].append(_res(e) or _texti(e))
        elif nafn == EDM + "rights":
            f["rettindi"].append(_res(e))
        elif nafn == DCT + "isReferencedBy":
            f["tilvisanir"].append(_res(e) or _texti(e))
        elif nafn == DC + "identifier":
            f["slodir"].append(_texti(e))
        elif nafn in (DC + "type", EDM + "type"):
            pass                                 # alltaf Book / TEXT; okkar par kemur í staðinn
        else:
            f["annad"].append(nafn.split("}")[-1])
    if not f["rettindi"] and agg is not None:
        f["rettindi"] = [_res(e) for e in agg.findall(EDM + "rights")]
    return f


def lesa_svar(gogn):
    """Eitt ListRecords-svar (bæti) → {'faerslur', 'token', 'fjoldi'}."""
    rot = ET.fromstring(gogn)
    villa = rot.find(OAI + "error")
    if villa is not None:
        raise SystemExit("OAI-villa: %s — %s" % (villa.get("code"), hreinsa(villa.text)))
    lr = rot.find(OAI + "ListRecords")
    if lr is None:
        raise SystemExit("Svarið er ekki ListRecords.")
    faerslur = [lesa_faerslu(r) for r in lr.findall(OAI + "record")]
    tok = lr.find(OAI + "resumptionToken")
    token = hreinsa(tok.text) if tok is not None else ""
    fjoldi = tok.get("completeListSize") if tok is not None else None
    return {"faerslur": faerslur, "token": token,
            "fjoldi": int(fjoldi) if fjoldi and fjoldi.isdigit() else None}


class _EngarBeinar(urllib.request.HTTPRedirectHandler):
    """Beiningar eru eltar í _saekja: urllib í Python 3.9 eltir ekki 308."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPNARI = urllib.request.build_opener(_EngarBeinar)


def _saekja(slod, tilraunir=4, hopp=5):
    """GET með endurtekningum (2, 4, 6 s) og beiningum (301/302/303/307/308)."""
    for n in range(tilraunir):
        nu = slod
        try:
            for _ in range(hopp + 1):
                beidni = urllib.request.Request(nu, headers={"User-Agent": UA})
                try:
                    with _OPNARI.open(beidni, timeout=180) as svar:
                        return svar.read()
                except urllib.error.HTTPError as e:
                    stadur = e.headers.get("Location")
                    e.close()
                    if e.code in (301, 302, 303, 307, 308) and stadur:
                        nu = urllib.parse.urljoin(nu, stadur)
                        continue
                    raise
            raise RuntimeError("of margar beiningar")
        except Exception as villa:               # net: reyna aftur, svo gefast upp
            if n == tilraunir - 1:
                raise SystemExit("Náðist ekki í %s: %s" % (nu, villa))
            time.sleep(2.0 * (n + 1))


def uppskera(baseurl, bid=1.0, vista=None):
    """Sækir ListRecords (edm) alla leið eftir resumptionToken.
    25 færslur á síðu (1.10.2026), svo ~120 síður. Bið `bid` s milli síðna."""
    rok = {"verb": "ListRecords", "metadataPrefix": SNID}
    sidur = []
    while True:
        gogn = _saekja(baseurl + "?" + urllib.parse.urlencode(rok))
        sidur.append(gogn)
        if vista:
            _vista_sidu(vista, len(sidur), gogn)
        s = lesa_svar(gogn)
        if len(sidur) % 20 == 0:
            print("  … %d síður, %d færslur" % (len(sidur), 25 * len(sidur)), file=sys.stderr)
        if not s["token"]:
            return sidur
        rok = {"verb": "ListRecords", "resumptionToken": s["token"]}
        time.sleep(bid)


# ------------------------------------------------------------- umbreyting
def _ny_talning():
    return {"flokkar": collections.Counter(), "nofn": collections.defaultdict(collections.Counter),
            "bok_flokkar": collections.Counter(), "oleyst": collections.Counter(),
            "aeviar": collections.Counter(), "land": collections.Counter(),
            "lond": collections.Counter(), "osamraemi": collections.Counter(),
            "rettindi": collections.Counter(), "othekkt_rettindi": collections.Counter(),
            "umfang_othekkt": collections.Counter(), "dags": collections.Counter(),
            "dags_othekkt": collections.Counter(), "mal": collections.Counter(),
            "titill_isbd": 0, "med_efni": 0, "slod_onnur": 0, "annad": collections.Counter(),
            "folk_i_bok": collections.Counter()}


def umbreyta(f, talning=None):
    """Ein færsla úr Bækur.is → <record> í gullna sniðinu (texti)."""
    t = talning if talning is not None else _ny_talning()
    for a in f["annad"]:
        t["annad"][a] += 1

    m = _UUID.search(f["id"]) or _UUID.search(f["synt"]) or _UUID.search(" ".join(f["slodir"]))
    uuid = m.group(0) if m else ""
    if uuid and not any(uuid in s for s in [f["synt"]] + f["slodir"]):
        t["slod_onnur"] += 1

    titlar = [hreinsa_titil(s) for s in f["titlar"] if hreinsa(s)]
    titill = titlar[0] if titlar else ""
    if titlar and titlar[0] != hreinsa(f["titlar"][0]):
        t["titill_isbd"] += 1

    audkenni = []
    if uuid:
        audkenni.append(SLOD_BOKAR + uuid)
        if f["mynd"]:
            audkenni.append(SLOD_SMAMYNDAR + uuid)
    audkenni.append(f["id"])

    dags = ""
    for d in f["dags"]:
        if _EDTF.match(d):
            dags = d
            t["dags"]["%s00" % d[:2]] += 1
            break
        if d:
            t["dags_othekkt"][d] += 1
    else:
        if not f["dags"]:
            t["dags"]["vantar"] += 1

    efni = []
    for lang, s in sorted(f["efni"], key=lambda ls: islensk_rod(ls[1])):
        if s and (lang or "is", s) not in efni:
            efni.append((lang or "is", s))
    if efni:
        t["med_efni"] += 1

    lond, stada = land(f["stadir"])
    t["land"][stada] += 1
    for n in lond:
        t["lond"][n] += 1
    if stada == "osamraemi":
        t["osamraemi"][" + ".join(s.rsplit("/", 1)[-1] for s in f["stadir"])] += 1

    hofundar, adrir, verk, tilvisanir = [], [], [], []
    flokkar_bokar = set()
    for uri, texti in f["hofundar"]:
        a = f["agentar"].get(uri) if uri else None
        if a is None and not texti:
            t["oleyst"][uri] += 1
            continue
        nafn, fra, til = (a["nafn"], a["fra"], a["til"]) if a else (texti, "", "")
        if not hreinsa(nafn):
            t["oleyst"][uri] += 1
            continue
        flokkur = flokka(nafn, fra, til)
        hreint = hreinsa_nafn(nafn, flokkur)
        t["flokkar"][flokkur] += 1
        t["nofn"][flokkur][hreint] += 1
        flokkar_bokar.add(flokkur)
        if flokkur == "persona":
            fullt = nafn_med_arum(hreint, fra, til)
            t["aeviar"]["med" if fullt != hreint else "an"] += 1
            if fullt not in hofundar:
                hofundar.append(fullt)
                tilvisanir.append("%s (%s)" % (fullt, HLUTVERK))
                t["folk_i_bok"][fullt] += 1
        elif flokkur == "stofnun":
            if hreint not in adrir:
                adrir.append(hreint)
        elif hreint not in verk:
            verk.append(hreint)
    for k in flokkar_bokar:
        t["bok_flokkar"][k] += 1

    rett = []
    for uri in dict.fromkeys(u for u in f["rettindi"] if u):
        heiti, slod = rettindi(uri)
        t["rettindi"][slod] += 1
        if heiti is None:
            t["othekkt_rettindi"][uri] += 1
        rett.append((heiti, slod))

    umf = ""
    for s in f["umfang"]:
        umf = umfang(s)
        if umf:
            break
        t["umfang_othekkt"][s] += 1

    mal = []
    for s in f["mal"]:
        k = mal_kodi(s)
        if k and k not in mal:
            mal.append(k)
            t["mal"][k] += 1

    bokaskra = []
    for s in f["tilvisanir"]:
        mm = re.match(r"^https?://bokaskra\.landsbokasafn\.is/search\?s_any=(\d+)$", s)
        if mm:
            bokaskra.append(SLOD_BOKASKRAR + mm.group(1))

    L = [_el("dc:identifier", a) for a in audkenni]
    L.append(_el("dc:title", titill, "is"))
    L.append(_el("dc:type", TEGUND_IS, "is"))
    L.append(_el("dc:type", TEGUND_EN, "en"))
    L.append(_el("dc:date", dags))
    L += [_el("dc:subject", s, lang) for lang, s in efni]
    L.append(_el("dc:subject", EFNI_IS, "is"))
    L += [_el("dcterms:spatial", n, "is", xsi__type="mshl:land", mshl__role=STADARHLUTVERK)
          for n in lond]
    L += [_el("dc:creator", n, mshl__role=HLUTVERK) for n in hofundar]
    L += [_el("dc:contributor", n) for n in adrir]
    L += [_el("dcterms:bibliographicCitation", s, "is") for s in tilvisanir]
    L += [_el("dcterms:hasPart", v, "is", xsi__type="mshl:verk") for v in verk]
    L.append(_el("dcterms:extent", umf, "is"))
    L += [_el("dc:language", k) for k in mal]
    L.append(_el("dc:publisher", UTGEFANDI, "is"))
    for heiti, slod in rett:
        L.append(_el("dc:rights", heiti, "is"))
        L.append(_el("dc:rights", slod))
    for slod in bokaskra:
        L.append(_el("dcterms:isReferencedBy", TILVISUN, "is"))
        L.append(_el("dcterms:isReferencedBy", slod))

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
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xmlns:mshl="https://mshl.is/terms#">\n'
            "%s</oai_dc:dc>\n"
            "    </metadata>\n"
            "  </record>\n") % (_x(f["id"]), _x(ds), SETT, "".join(L))


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
    if rot.tag != "ListRecords" or rot.attrib:
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
            elif g.casefold() in _NONE or "None" in g.split():
                villur.append("%s: %s = %r" % (aud, nafn, g))
            if _HTML.search(g):
                villur.append("%s: HTML í %s: %s" % (aud, nafn, g[:60]))
            if _STYRITAKN.search(g):
                villur.append("%s: stýritákn í %s" % (aud, nafn))
            for k, v in e.attrib.items():
                if not v.strip() or v.strip().casefold() in _NONE:
                    villur.append("%s: tóm eigind %s á %s" % (aud, k, nafn))

        def allt(tag, lang="*"):
            return [e.text for e in dc.findall(tag)
                    if lang == "*" or e.get(XML_LANG) == lang]
        if len(allt(DC + "title")) != 1 or len(allt(DC + "title", "is")) != 1:
            villur.append("%s: ekki nákvæmlega einn dc:title @is" % aud)
        slodir = allt(DC + "identifier")
        if not slodir or not (slodir[0] or "").startswith(SLOD_BOKAR):
            villur.append("%s: fyrsti dc:identifier er ekki slóð heim (%s…)" % (aud, SLOD_BOKAR))
        if not (allt(DC + "type", "is") and allt(DC + "type", "en")):
            villur.append("%s: vantar dc:type par @is + @en" % aud)
        if not allt(DC + "subject", "is"):
            villur.append("%s: vantar dc:subject @is" % aud)
        for d in allt(DC + "date"):
            if not _EDTF.match(d or ""):
                villur.append("%s: dc:date ekki á EDTF: %s" % (aud, d))
        for k in allt(DC + "language"):
            if not re.match(r"^[a-z]{2,3}$", k or ""):
                villur.append("%s: dc:language ekki ISO-kóði: %s" % (aud, k))
        for e in dc.findall(DC + "creator"):
            if e.get(MSHL + "role") != HLUTVERK:
                villur.append("%s: dc:creator án mshl:role" % aud)
        if len(dc.findall(DC + "creator")) != len(dc.findall(DCT + "bibliographicCitation")):
            villur.append("%s: dc:creator og bibliographicCitation stemma ekki" % aud)
        for e in dc.findall(DCT + "spatial"):
            if e.get(XSI + "type") != "mshl:land":
                villur.append("%s: dcterms:spatial án xsi:type mshl:land" % aud)
    return villur


# ------------------------------------------------------------- keyrsla
def _vista_sidu(mappa, n, gogn):
    os.makedirs(mappa, exist_ok=True)
    with open(os.path.join(mappa, "sida-%03d.xml" % n), "wb") as fh:
        fh.write(gogn)


def _inntaksskrar(inntak):
    """Skrár í röð: mappa → sida-*.xml (eða *.xml) í stafrófsröð."""
    skrar = []
    for slod in inntak:
        if os.path.isdir(slod):
            fundid = sorted(glob.glob(os.path.join(slod, "sida-*.xml"))) or \
                sorted(glob.glob(os.path.join(slod, "*.xml")))
            if not fundid:
                raise SystemExit("Engar .xml-skrár í %s" % slod)
            skrar += fundid
        else:
            skrar.append(slod)
    return skrar


def _skrifa(slod, texti):
    os.makedirs(os.path.dirname(os.path.abspath(slod)), exist_ok=True)
    with open(slod, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texti)


def _tolur(n):
    """1680 → '1.680' (íslensk þúsundaskil)."""
    return "{:,}".format(n).replace(",", ".")


def main(argv=None):
    p = argparse.ArgumentParser(description="Bækur.is (edm) → gullið Dublin Core")
    p.add_argument("inntak", nargs="*",
                   help="vistuð ListRecords-svör (skrár eða mappa), í röð; annars er sótt")
    p.add_argument("--baseurl", default=BASEURL)
    p.add_argument("--vista", help="mappa fyrir hráu síðurnar (sida-001.xml …)")
    p.add_argument("--bid", type=float, default=1.0, help="sekúndur milli síðna (sjálfgefið 1)")
    p.add_argument("--ut", default=UT)
    p.add_argument("--synisveita", default=SYNISVEITA,
                   help="afrit fyrir Gáttagægi; tómur strengur = ekkert afrit")
    a = p.parse_args(argv)

    if a.inntak:
        skrar = _inntaksskrar(a.inntak)
        sidur = []
        for slod in skrar:
            with open(slod, "rb") as fh:
                sidur.append(fh.read())
        uppruni = "%s (%d skrár)" % (", ".join(a.inntak), len(skrar))
    else:
        sidur = uppskera(a.baseurl, a.bid, a.vista)
        uppruni = a.baseurl
        if a.vista:
            print("Vistað hrátt: %s/sida-001.xml … sida-%03d.xml" % (a.vista, len(sidur)))

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

    N = len(einstakar)
    print("Inn: %s færslur úr %s (%d síður) · completeListSize %s · eyddar %d · tvítök %d"
          % (_tolur(len(allar)), uppruni, len(sidur), uppgefid, eyddar, tvitok))
    print("Út:  %s færslur → %s (%d kB)" % (_tolur(N), a.ut, len(texti.encode("utf-8")) // 1024))
    if a.synisveita:
        print("Afrit: %s" % a.synisveita)
    if t["slod_onnur"]:
        print("⚠ %d færslur: uuid í auðkenni passar ekki við slóð bókarinnar" % t["slod_onnur"])
    print("Titlar: %d með ISBD-tákni aftast (=, /, ;, :) sem var tekið af" % t["titill_isbd"])
    d = t["dags"]
    print("dc:date: %s · vantar %d%s" % (
        " · ".join("%s–%s99 %d" % (k, k[:2], v) for k, v in sorted(d.items()) if k != "vantar"),
        d["vantar"], (" · óþekkt snið: %s" % dict(t["dags_othekkt"])) if t["dags_othekkt"] else ""))
    print("dc:subject úr heimild: %s bækur af %s; „%s“ bætt við allar"
          % (_tolur(t["med_efni"]), _tolur(N), EFNI_IS))
    ld = t["land"]
    print("Land: %s bækur fá land · LoC null/xx (óþekkt) %d · ósamræmi eða utan töflu %d · vantar %d"
          % (_tolur(ld["samhljoda"]), ld["othekkt"], ld["osamraemi"], ld["vantar"]))
    print("  " + " · ".join("%s %s" % (k, _tolur(v)) for k, v in t["lond"].most_common()))
    for k, v in t["osamraemi"].most_common():
        print("  ⚠ ósamræmi/utan töflu: %s (%d)" % (k, v))
    fl = t["flokkar"]
    print("Höfundar í heimild: %s tengingar · manneskjur %s · stofnanir %d · verk %d · óleyst %d"
          % (_tolur(sum(fl.values())), _tolur(fl["persona"]), fl["stofnun"], fl["verk"],
             sum(t["oleyst"].values())))
    print("  Manneskjur: %s ólík nöfn; æviár (bæði ár til) á %s af %s tengingum"
          % (_tolur(len(t["nofn"]["persona"])), _tolur(t["aeviar"]["med"]),
             _tolur(t["aeviar"]["med"] + t["aeviar"]["an"])))
    print("  Algengust: " + " · ".join("%s %d" % kv for kv in t["folk_i_bok"].most_common(6)))
    for flokkur, heiti, reitur in (("stofnun", "Stofnanir", "dc:contributor"),
                                   ("verk", "Verk", "dcterms:hasPart mshl:verk")):
        nofn = t["nofn"][flokkur]
        print("  %s → %s: %d ólík nöfn á %d bókum:" % (heiti, reitur, len(nofn), t["bok_flokkar"][flokkur]))
        print("    " + " · ".join("%s %d" % kv for kv in sorted(nofn.items(), key=lambda kv: (-kv[1], kv[0]))))
    print("dc:rights: " + " · ".join("%s %s" % (k, _tolur(v)) for k, v in t["rettindi"].most_common()))
    if t["othekkt_rettindi"]:
        print("⚠ réttindi án íslensks heitis: %s" % dict(t["othekkt_rettindi"]))
    if t["umfang_othekkt"]:
        print("⚠ dcterms:extent á óþekktu sniði: %s" % dict(t["umfang_othekkt"]))
    print("dc:language: %s" % " · ".join("%s %d" % kv for kv in t["mal"].most_common()))
    if t["annad"]:
        print("⚠ ókortlagðir reitir í edm:ProvidedCHO: %s" % dict(t["annad"]))
    print("Sannprófað: gilt XML · ber <ListRecords> án xmlns og án <?xml?> · "
          "fyrsta header/identifier = %s · engir tómir reitir, None né HTML"
          % einstakar[0]["id"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

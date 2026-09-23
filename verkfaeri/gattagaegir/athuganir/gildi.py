"""Athuganir á gildunum sjálfum — dagsetningar, hnit, forskeyti, auðkenni."""
import re

from . import (GILDI, VILLA, ADVORUN, ABENDING)

DOC = "oai-pmh/LEIDBEININGAR.md"

# EDTF L0/L1 (naumt): ártal, ártal-mánuður(-dagur), bil með /, óvissa ~?%
_EDTF = re.compile(
    r"^-?\d{4}([-~?%])?$|"
    r"^-?\d{4}-\d{2}(-\d{2})?[~?%]?$|"
    r"^-?\d{4}(-\d{2}(-\d{2})?)?/-?\d{4}(-\d{2}(-\d{2})?)?$|"
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)
_POINT = re.compile(r"^POINT\(\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s*\)$")
_FORSKEYTI = re.compile(
    r"^[A-ZÁÐÉÍÓÚÝÞÆÖ][a-záðéíóúýþæö ]{1,25}:\s")
_STADAREITIR = ("dc:subject", "dc:coverage", "dcterms:spatial", "dc:type",
                "dc:format", "dcterms:temporal")
_SAMLEIT = ("dc:subject", "dc:coverage", "dcterms:spatial")

# einföld þágufalls→nefnifalls tafla (vélræn ágiskun)
_THAGUFALL = [
    ("holti", "holt"), ("nesi", "nes"), ("felli", "fell"),
    ("stöðum", "staðir"), ("völlum", "vellir"), ("hólum", "hólar"),
    ("firði", "fjörður"), ("koti", "kot"), ("túni", "tún"),
    ("landi", "land"), ("tungum", "tungur"),
]
_NEFNIFALL_UNDANTEKNING = {"eyri", "skagi", "hagi", "bakki", "lóni"}

_TYPUR_EN = {
    "place", "person", "volume", "register", "manuscript", "legend",
    "soundrecording", "photography", "drawing", "art", "book / archive",
    "artifact", "coin", "house", "archaeology remain",
    "mineralogy / petrology", "archaeology", "folk customs response",
}


def _nd(s, kenni, heiti, alv):
    return s.n(kenni, GILDI, heiti, alv, False, DOC)


def _berandi(s):
    return [f for f in s.faerslur if not f.eydd and f.reitir]


def _laga_dags(g):
    m = re.match(r"^\s*(\d{4})\s*-\s*(\d{4})\s*$", g)
    if m:
        return "%s/%s" % (m.group(1), m.group(2))
    m = re.match(r"^\s*(\d{2})\.(\d{2})\.(\d{4})\s*-\s*"
                 r"(\d{2})\.(\d{2})\.(\d{4})\s*$", g)
    if m:
        return "%s/%s" % (m.group(3), m.group(6))
    m = re.match(r"^\s*um\s+(\d{4})\s*-\s*(\d{4})", g, re.IGNORECASE)
    if m:
        return "%s/%s (geymið frumtextann í dcterms:temporal)" \
               % (m.group(1), m.group(2))
    m = re.match(r"^\s*(\d{2})\.(\d{2})\.(\d{4})\s*$", g)
    if m:
        return "%s-%s-%s" % (m.group(3), m.group(2), m.group(1))
    return None


def G01(s):
    nd = _nd(s, "G01", "Dagsetningar á EDTF", ADVORUN)
    faerslur = _berandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    fell = 0
    for f in faerslur:
        for r in f.reitir_heitir("dc:date"):
            if r.gildi and not _EDTF.match(r.gildi):
                fell += 1
                tillaga = _laga_dags(r.gildi)
                nd.baeta(audkenni=f.audkenni, reitur="dc:date", gildi=r.gildi,
                         skyring=("→ %s" % tillaga) if tillaga
                         else "ekki EDTF")
    if fell:
        return nd.fell_("%d dc:date-gildi eru ekki á EDTF." % fell, fell=fell)
    return nd.stodst_("Öll dc:date-gildi eru á EDTF (þar sem þau eru til).")


def _hnit(s):
    ut = []
    for f in _berandi(s):
        for r in f.reitir:
            if r.xsi_type == "dcterms:Point" or r.gildi.startswith("POINT"):
                ut.append((f.audkenni, r))
    return ut


def G02(s):
    nd = _nd(s, "G02", "Hnit á sniðinu POINT(lengd breidd)", VILLA)
    hnit = _hnit(s)
    if not hnit:
        return nd.sleppt_("Engin hnit í sýni.")
    fell = 0
    for aud, r in hnit:
        if not _POINT.match(r.gildi):
            fell += 1
            nd.baeta(audkenni=aud, reitur=r.nafn, gildi=r.gildi,
                     skyring="ekki á sniðinu POINT(lengd breidd)")
    if fell:
        return nd.fell_("%d hnit eru ekki á réttu sniði." % fell, fell=fell)
    return nd.stodst_("Öll hnit eru á sniðinu POINT(lengd breidd).")


def G03(s):
    nd = _nd(s, "G03", "Öll hnit innan raunhæfra marka", VILLA)
    hnit = _hnit(s)
    if not hnit:
        return nd.sleppt_("Engin hnit í sýni.")
    fell = 0
    for aud, r in hnit:
        m = _POINT.match(r.gildi)
        if not m:
            continue
        lengd, breidd = float(m.group(1)), float(m.group(2))
        i_landi = (-25 <= lengd <= -13) and (63 <= breidd <= 67)
        ofug = (63 <= lengd <= 67) and (-25 <= breidd <= -13)
        if ofug:
            fell += 1
            nd.baeta(audkenni=aud, gildi=r.gildi,
                     skyring="öfug röð — lendir í Indlandshafi "
                             "(lengd fyrst!)")
        elif not i_landi:
            nd.baeta(audkenni=aud, gildi=r.gildi,
                     skyring="utan Íslands — er það rétt?")
    if fell:
        return nd.fell_("%d hnit eru með öfuga röð (breidd/lengd víxlað)."
                        % fell, fell=fell)
    return nd.stodst_("Hnit innan marka (eða skýrð utanlands).")


def G04(s):
    nd = _nd(s, "G04", "Engin forskeyti í gildum", VILLA)
    faerslur = _berandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    fell = 0
    for f in faerslur:
        for r in f.reitir:
            if r.nafn in _STADAREITIR and r.gildi and _FORSKEYTI.match(
                    r.gildi):
                fell += 1
                nd.baeta(audkenni=f.audkenni, reitur=r.nafn, gildi=r.gildi,
                         skyring="forskeyti í gildi — flokkun á heima í "
                                 "xsi:type")
    if fell:
        return nd.fell_("%d gildi bera forskeyti í textanum (t.d. "
                        "'Sýsla: …')." % fell, fell=fell)
    return nd.stodst_("Engin forskeyti í gildum samleitarreita.")


def _er_hnit(r):
    return r.xsi_type == "dcterms:Point" or (r.gildi or "").startswith("POINT")


def _stadarnofn(f):
    """Nafnareitir staðar, ekki hnitareiturinn."""
    return [r for r in f.reitir
            if r.nafn in ("dcterms:spatial", "dc:coverage")
            and r.gildi and not _er_hnit(r)]


def _hefur_hnit(f):
    return any(_er_hnit(r) for r in f.reitir)


def _hefur_stadaraudkenni(f):
    """Varanlegt auðkenni á staðarreit (mshl:id), eins og á efnisorðum."""
    for r in _stadarnofn(f):
        if any(k in ("mshl:id", "id") for k in r.eigindir):
            return True
    return False


def _thagufallsmynd(gildi):
    """Skilar nefnifallsendingu ef gildið lítur út eins og þágufall."""
    lag = gildi.casefold()
    if lag in _NEFNIFALL_UNDANTEKNING:
        return None
    for endir, nefni in _THAGUFALL:
        if lag.endswith(endir):
            return nefni
    return None


def G05(s):
    """Þrepaskipt beiðni úr LEIDBEININGAR 2.5.

    Beygð mynd er í lagi þegar hnit eða varanlegt auðkenni fylgja færslunni.
    Án hvors tveggja er lágmarkið nafn í nefnifalli. Ágiskunin er vélræn.
    """
    nd = _nd(s, "G05", "Staðanöfn: nefnifall, hnit eða auðkenni", ABENDING)
    faerslur = _berandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    an_fylgdar = 0
    med_fylgd = 0
    for f in faerslur:
        fylgir = _hefur_hnit(f) or _hefur_stadaraudkenni(f)
        for r in _stadarnofn(f):
            nefni = _thagufallsmynd(r.gildi)
            if not nefni:
                continue
            if fylgir:
                med_fylgd += 1
                continue
            an_fylgdar += 1
            nd.baeta(audkenni=f.audkenni, reitur=r.nafn, gildi=r.gildi,
                     skyring="lítur út eins og þágufall (→ …%s?) og hvorki "
                             "hnit né auðkenni fylgja" % nefni)
    if an_fylgdar:
        return nd.fell_(
            "%d staðanöfn líta út eins og þágufall og hvorki hnit né "
            "auðkenni fylgja færslunni." % an_fylgdar,
            lagfaering="Ef heimildin ber þágufall, sendið það og látið "
                       "POINT(lengd breidd) eða varanlegt auðkenni "
                       "(mshl:id) fylgja. Annars skilið nafninu í "
                       "nefnifalli.",
            fell=an_fylgdar)
    if med_fylgd:
        return nd.stodst_(
            "%d beygð staðanöfn fylgja hnitum eða auðkenni — það er í lagi."
            % med_fylgd)
    return nd.stodst_("Engin augljós þágufallsmynd í staðanöfnum.")


def G06(s):
    nd = _nd(s, "G06", "Efnisorð bera varanlegt auðkenni", ABENDING)
    faerslur = _berandi(s)
    efni = [(f, r) for f in faerslur for r in f.reitir_heitir("dc:subject")
            if r.gildi]
    if not efni:
        return nd.sleppt_("Engin efnisorð í sýni.")
    med_id = sum(1 for _f, r in efni
                 if any(k in ("mshl:id", "id") for k in r.eigindir))
    hlutf = 100.0 * med_id / len(efni)
    if med_id == 0:
        return nd.fell_("Ekkert efnisorð ber varanlegt auðkenni (mshl:id) — "
                        "án þess þarf að þýða orðaforðann aftur og aftur.")
    return nd.stodst_("%.0f%% efnisorða bera varanlegt auðkenni." % hlutf)


def G07(s):
    nd = _nd(s, "G07", "Hlutverk fylgja fólki", ABENDING)
    faerslur = _berandi(s)
    folk = [(f, r) for f in faerslur
            for r in f.reitir if r.nafn in ("dc:creator", "dc:contributor")
            and r.gildi]
    if not folk:
        return nd.sleppt_("Ekkert fólk í sýni.")
    an_hlutverks = 0
    for f, r in folk:
        if "mshl:role" not in r.eigindir:
            an_hlutverks += 1
        if re.search(r"\(\d{1,2}\.\d{1,2}\.\d{4}\s*-", r.gildi):
            nd.baeta(audkenni=f.audkenni, reitur=r.nafn, gildi=r.gildi,
                     skyring="æviár inni í nafnastreng")
    if an_hlutverks == len(folk):
        return nd.fell_("Ekkert af %d nöfnum ber hlutverk (mshl:role) — þá "
                        "vitum við ekki hver gerði hvað." % len(folk))
    return nd.stodst_("%d af %d nöfnum bera hlutverk."
                      % (len(folk) - an_hlutverks, len(folk)))


def G09(s):
    nd = _nd(s, "G09", "dc:type @en í þekktum orðaforða", ABENDING)
    faerslur = _berandi(s)
    ensk = [(f, r) for f in faerslur for r in f.reitir_heitir("dc:type")
            if r.lang == "en" and r.gildi]
    if not ensk:
        return nd.sleppt_("Engin ensk dc:type-gildi í sýni.")
    othekkt = set()
    for f, r in ensk:
        if r.gildi.casefold() not in _TYPUR_EN:
            othekkt.add(r.gildi)
            nd.baeta(audkenni=f.audkenni, reitur="dc:type", gildi=r.gildi,
                     skyring="fellur í 'other' — ekki í þekktum orðaforða")
    if othekkt:
        return nd.fell_("Óþekkt dc:type @en gildi: %s"
                        % ", ".join(sorted(othekkt)))
    return nd.stodst_("Öll ensk dc:type-gildi eru í þekktum orðaforða.")


ALLAR = [G01, G02, G03, G04, G05, G06, G07, G09]

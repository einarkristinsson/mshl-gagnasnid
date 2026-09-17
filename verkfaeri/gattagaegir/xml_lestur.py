"""Þolið XML-lesning fyrir OAI-PMH svör.

Verkfærið á að finna gölluð gögn — þá má það ekki sjálft hrynja á þeim.
Öll greining er vafin inn í try/except og skilar skýrri greiningu í stað
undantekningar.
"""
import re
import xml.etree.ElementTree as ET

OAI = "http://www.openarchives.org/OAI/2.0/"
OAI_DC = "http://www.openarchives.org/OAI/2.0/oai_dc/"
DC = "http://purl.org/dc/elements/1.1/"
DCTERMS = "http://purl.org/dc/terms/"
XSI = "http://www.w3.org/2001/XMLSchema-instance"
XML_NS = "http://www.w3.org/XML/1998/namespace"
MSHL = "https://mshl.is/terms#"

_FORSKEYTI = {
    OAI: "oai", OAI_DC: "oai_dc", DC: "dc", DCTERMS: "dcterms",
    XSI: "xsi", MSHL: "mshl", XML_NS: "xml",
}

# Skrá forskeytin svo ET.tostring haldi læsilegum forskeytum (oai_dc:dc)
# í stað ns0: þegar við raðgreinum hráa færslu. (xml-forskeytið er
# sérmeðhöndlað af ElementTree og má ekki skrá.)
for _ns, _pfx in _FORSKEYTI.items():
    if _ns != XML_NS:
        ET.register_namespace(_pfx, _ns)

_HTML_MERKI = re.compile(
    r"<!doctype html|<html[\s>]|<b>\s*fatal error|<b>\s*warning|"
    r"stack trace|<br\s*/?>|parse error:",
    re.IGNORECASE,
)


def _nafn(tag):
    """Breytir '{ns}local' í 'forskeyti:local' (eða bara local)."""
    if tag and tag[0] == "{":
        ns, local = tag[1:].split("}", 1)
        return "%s:%s" % (_FORSKEYTI.get(ns, ns), local), ns
    return tag, None


class Reitur:
    def __init__(self, nafn, ns, gildi, lang, xsi_type, eigindir):
        self.nafn = nafn          # t.d. 'dc:title'
        self.ns = ns              # nafnrými (URI) eða None
        self.gildi = gildi        # texti, strípaður
        self.lang = lang          # xml:lang eða None
        self.xsi_type = xsi_type  # xsi:type eða None
        self.eigindir = eigindir  # aðrar eigindir: {'mshl:id': '...'}


class Faersla:
    def __init__(self):
        self.audkenni = None
        self.dagstimpill = None
        self.sett = []
        self.eydd = False
        self.reitir = []
        self.hefur_metadata = False
        self.hratt_xml = None     # raðgreint <record> XML (oai_dc-forskeyti)

    def reitir_heitir(self, nafn):
        return [r for r in self.reitir if r.nafn == nafn]


class Skjal:
    def __init__(self, texti):
        self.texti = texti
        self.rot = None
        self.villa = None       # {'lina','dalkur','texti','utdrattur'}
        self.er_html = bool(_HTML_MERKI.search(texti or ""))

    @property
    def gilt(self):
        return self.rot is not None


def _utdrattur(texti, lina):
    linur = (texti or "").splitlines()
    if 1 <= lina <= len(linur):
        brot = linur[lina - 1][:120]
        # sýna stýritákn sem \xNN svo þau sjáist
        return "".join(
            ch if (ch == "\t" or ch >= " ") else "\\x%02x" % ord(ch)
            for ch in brot
        )
    return ""


def lesa(svar):
    """Les eitt OAI-svar. Skilar Skjal (rót eða greindri villu)."""
    gogn = svar.gogn if hasattr(svar, "gogn") else svar
    texti = svar.texti if hasattr(svar, "texti") else ""
    skjal = Skjal(texti)
    hreint = gogn[3:] if gogn[:3] == b"\xef\xbb\xbf" else gogn
    try:
        skjal.rot = ET.fromstring(hreint)
    except ET.ParseError as e:
        lina, dalkur = (list(e.position) + [0, 0])[:2]
        skjal.villa = {
            "lina": lina, "dalkur": dalkur,
            "texti": str(e), "utdrattur": _utdrattur(texti, lina),
        }
    except Exception as e:
        skjal.villa = {"lina": 0, "dalkur": 0,
                       "texti": str(e), "utdrattur": ""}
    return skjal


def oai_villa(skjal):
    """Skilar (kodi, texti) ef svarið er OAI-villa, annars None."""
    if not skjal.gilt:
        return None
    for e in skjal.rot.iter("{%s}error" % OAI):
        return (e.get("code", ""), (e.text or "").strip())
    return None


def identify(skjal):
    """Les Identify-svar í orðabók."""
    ut = {"adminEmail": [], "metadataPrefixes": []}
    if not skjal.gilt:
        return ut
    idn = skjal.rot.find("{%s}Identify" % OAI)
    if idn is None:
        return ut
    for barn in idn:
        nafn, _ = _nafn(barn.tag)
        local = nafn.split(":", 1)[-1]
        if local == "adminEmail":
            ut["adminEmail"].append((barn.text or "").strip())
        else:
            ut[local] = (barn.text or "").strip()
    return ut


def _reitir_ur_dc(dc_el):
    reitir = []
    for barn in dc_el:
        nafn, ns = _nafn(barn.tag)
        lang = barn.get("{%s}lang" % XML_NS)
        xsi_type = barn.get("{%s}type" % XSI)
        eig = {}
        for k, v in barn.attrib.items():
            kn, _ = _nafn(k)
            if kn not in ("xml:lang", "xsi:type"):
                eig[kn] = v
        reitir.append(Reitur(nafn, ns, (barn.text or "").strip(),
                             lang, xsi_type, eig))
    return reitir


def _faersla_ur_record(rec):
    f = Faersla()
    try:
        f.hratt_xml = ET.tostring(rec, encoding="unicode")
    except Exception:
        f.hratt_xml = None
    haus = rec.find("{%s}header" % OAI)
    if haus is not None:
        f.eydd = haus.get("status") == "deleted"
        idn = haus.find("{%s}identifier" % OAI)
        if idn is not None:
            f.audkenni = (idn.text or "").strip()
        ds = haus.find("{%s}datestamp" % OAI)
        if ds is not None:
            f.dagstimpill = (ds.text or "").strip()
        for s in haus.findall("{%s}setSpec" % OAI):
            f.sett.append((s.text or "").strip())
    meta = rec.find("{%s}metadata" % OAI)
    if meta is not None:
        f.hefur_metadata = True
        dc_el = meta.find("{%s}dc" % OAI_DC)
        if dc_el is not None:
            f.reitir = _reitir_ur_dc(dc_el)
    return f


def faerslur(skjal):
    """Skilar öllum <record> í svari (ListRecords eða GetRecord)."""
    if not skjal.gilt:
        return []
    return [_faersla_ur_record(r)
            for r in skjal.rot.iter("{%s}record" % OAI)]


def hausar(skjal):
    """Skilar <header> úr ListIdentifiers sem einföldum Faerslum."""
    ut = []
    if not skjal.gilt:
        return ut
    for h in skjal.rot.iter("{%s}header" % OAI):
        f = Faersla()
        f.eydd = h.get("status") == "deleted"
        idn = h.find("{%s}identifier" % OAI)
        if idn is not None:
            f.audkenni = (idn.text or "").strip()
        ds = h.find("{%s}datestamp" % OAI)
        if ds is not None:
            f.dagstimpill = (ds.text or "").strip()
        for s in h.findall("{%s}setSpec" % OAI):
            f.sett.append((s.text or "").strip())
        ut.append(f)
    return ut


def resumption(skjal):
    """Skilar (token, completeListSize, cursor) eða (None, None, None)."""
    if not skjal.gilt:
        return (None, None, None)
    for rt in skjal.rot.iter("{%s}resumptionToken" % OAI):
        token = (rt.text or "").strip()
        cls = rt.get("completeListSize")
        cursor = rt.get("cursor")
        return (token or None,
                int(cls) if cls and cls.isdigit() else None,
                int(cursor) if cursor and cursor.isdigit() else None)
    return (None, None, None)


def sett_ur(skjal):
    """Skilar lista af (setSpec, setName) úr ListSets."""
    ut = []
    if not skjal.gilt:
        return ut
    for s in skjal.rot.iter("{%s}set" % OAI):
        spec = s.find("{%s}setSpec" % OAI)
        nafn = s.find("{%s}setName" % OAI)
        ut.append(((spec.text or "").strip() if spec is not None else "",
                   (nafn.text or "").strip() if nafn is not None else ""))
    return ut


_REC_SKIL = re.compile(r"(?=<record[\s>])")
_ID_LEIT = re.compile(r"<identifier>([^<]+)</identifier>")


def bjarga(texti):
    """Reynir að bjarga heilum færslum úr brotinni síðu.

    Skilar (heilar_faerslur, [audkenni_brotinna]). Notað þegar ein skemmd
    færsla fellir alla síðuna: við klippum á <record>-mörkum og reynum
    hverja fyrir sig, svo hægt sé að nafngreina þá skemmdu.
    """
    heilar, brotin = [], []
    umgjord = (
        '<w xmlns="%s" xmlns:oai_dc="%s" xmlns:dc="%s" '
        'xmlns:dcterms="%s" xmlns:xsi="%s" xmlns:mshl="%s" '
        'xmlns:xml="%s">%%s</w>' % (OAI, OAI_DC, DC, DCTERMS, XSI, MSHL,
                                    XML_NS)
    )
    bitar = _REC_SKIL.split(texti or "")
    for biti in bitar:
        if "<record" not in biti:
            continue
        endir = biti.rfind("</record>")
        if endir == -1:
            m = _ID_LEIT.search(biti)
            brotin.append(m.group(1).strip() if m else "(óþekkt)")
            continue
        brot = biti[:endir + len("</record>")]
        try:
            el = ET.fromstring(umgjord % brot)
            rec = el.find("{%s}record" % OAI)
            if rec is not None:
                heilar.append(_faersla_ur_record(rec))
        except ET.ParseError:
            m = _ID_LEIT.search(brot)
            brotin.append(m.group(1).strip() if m else "(óþekkt)")
    return heilar, brotin

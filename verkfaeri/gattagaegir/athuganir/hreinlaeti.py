"""Hreinlætisathuganir — það sem sniðið krefst umfram staðlað XML."""
import re

from .. import xml_lestur as xl
from . import (HREINLAETI, VILLA, ADVORUN, ABENDING)

DOC = "oai-pmh/GATLISTI.md"
_STYRITAKN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_NONE_GILDI = {"none", "null", "n/a", "na", "-", "\u2013", "\u2014", "?",
               "[]", "undefined", "nan"}


def _nd(s, kenni, heiti, alv):
    return s.n(kenni, HREINLAETI, heiti, alv, False, DOC)


def _oll_svor(s):
    return s.oll_svor


def H01(s):
    nd = _nd(s, "H01", "Skráin er gilt XML", VILLA)
    fell = 0
    for svar in _oll_svor(s):
        sk = xl.lesa(svar)
        if not sk.gilt and not sk.er_html:
            fell += 1
            v = sk.villa or {}
            skyr = "lína %s: %s" % (v.get("lina"), v.get("utdrattur"))
            if svar.texti.count("<![CDATA[") > svar.texti.count("]]>"):
                skyr += " (ólokað CDATA?)"
            nd.baeta(gildi=svar.slod.split("verb=")[-1][:40], skyring=skyr)
        elif sk.er_html and not sk.gilt:
            fell += 1
            nd.baeta(gildi=svar.slod.split("verb=")[-1][:40],
                     skyring="svar er HTML/PHP-villa, ekki XML")
    if fell:
        return nd.fell_("%d svör eru ekki gilt XML (sjá einnig E12)." % fell,
                        fell=fell)
    return nd.stodst_("Öll sótt svör eru gilt XML.")


def H02(s):
    nd = _nd(s, "H02", "UTF-8, engin BOM", VILLA)
    bom = [sv for sv in _oll_svor(s) if sv.bom]
    ekki = [sv for sv in _oll_svor(s) if sv.ekki_utf8]
    if bom:
        nd.baeta(skyring="svar byrjar á UTF-8 BOM (EF BB BF)")
    if ekki:
        nd.baeta(skyring="svar er ekki gilt UTF-8")
    if bom or ekki:
        return nd.fell_("%d svör með BOM, %d ekki gilt UTF-8."
                        % (len(bom), len(ekki)))
    return nd.stodst_("Öll svör eru UTF-8 án BOM.")


def _naesta_audkenni(texti, staða):
    m = None
    for m2 in re.finditer(r"<identifier>([^<]+)</identifier>",
                          texti[:staða]):
        m = m2
    return m.group(1).strip() if m else None


def H03(s):
    nd = _nd(s, "H03", "Engin stýritákn", VILLA)
    fjoldi = 0
    for svar in _oll_svor(s):
        for m in _STYRITAKN.finditer(svar.texti):
            fjoldi += 1
            aud = _naesta_audkenni(svar.texti, m.start())
            nd.baeta(audkenni=aud, gildi="\\x%02x" % ord(m.group()),
                     skyring="stýritákn brýtur XML")
            if fjoldi >= 20:
                break
    if fjoldi:
        return nd.fell_("%d stýritákn fundust (\\x00–\\x1f nema tab/línuskil)."
                        % fjoldi, fell=fjoldi)
    return nd.stodst_("Engin stýritákn í svörunum.")


def H04(s):
    nd = _nd(s, "H04", "Ekkert ]]> inni í CDATA", VILLA)
    fell = 0
    for svar in _oll_svor(s):
        opnar = svar.texti.count("<![CDATA[")
        lokar = svar.texti.count("]]>")
        if opnar != lokar or "]]>]]>" in svar.texti:
            fell += 1
            nd.baeta(gildi="CDATA: %d opnuð, %d lokuð" % (opnar, lokar),
                     skyring="ólokað eða tvöfalt ]]>")
    if fell:
        return nd.fell_("%d svör með ójafnvægi í CDATA." % fell, fell=fell)
    return nd.stodst_("CDATA-jafnvægi í lagi.")


def _gildandi(s):
    return [f for f in s.faerslur if not f.eydd]


def H05(s):
    nd = _nd(s, "H05", "Engin None, null, N/A eða - sem gildi", VILLA)
    faerslur = _gildandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    fjoldi = 0
    for f in faerslur:
        for r in f.reitir:
            if r.gildi and r.gildi.strip().casefold() in _NONE_GILDI:
                fjoldi += 1
                nd.baeta(audkenni=f.audkenni, reitur=r.nafn, gildi=r.gildi,
                         skyring="tómleikastrengur — sleppið reitnum")
    if fjoldi:
        return nd.fell_("%d reitir bera None/null/N-A/- sem gildi." % fjoldi,
                        fell=fjoldi)
    return nd.stodst_("Engin tómleikastrengja-gildi.")


def H06(s):
    nd = _nd(s, "H06", "Engir tómir reitir", VILLA)
    faerslur = _gildandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    fjoldi = 0
    for f in faerslur:
        for r in f.reitir:
            if not r.gildi:
                fjoldi += 1
                nd.baeta(audkenni=f.audkenni, reitur=r.nafn,
                         skyring="tómur reitur ber engar upplýsingar")
    if fjoldi:
        return nd.fell_("%d tómir reitir." % fjoldi, fell=fjoldi)
    return nd.stodst_("Engir tómir reitir.")


def H07(s):
    nd = _nd(s, "H07", "Engin færsla með haus en tómu oai_dc:dc", VILLA)
    faerslur = _gildandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    fjoldi = 0
    for f in faerslur:
        if not f.hefur_metadata or not f.reitir:
            fjoldi += 1
            nd.baeta(audkenni=f.audkenni,
                     skyring="haus til staðar en engin metadata")
    if fjoldi:
        return nd.fell_("%d færslur með haus en tómu/engu oai_dc:dc."
                        % fjoldi, fell=fjoldi)
    return nd.stodst_("Allar færslur bera metadata.")


def H08(s):
    nd = _nd(s, "H08", "Heildartexti er hreinn texti (ekkert HTML)", ADVORUN)
    faerslur = _gildandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    fjoldi = 0
    merki = re.compile(r"<br|</\w+>|<p[>\s]|&nbsp;", re.IGNORECASE)
    for f in faerslur:
        for r in f.reitir:
            if r.gildi and merki.search(r.gildi):
                fjoldi += 1
                nd.baeta(audkenni=f.audkenni, reitur=r.nafn,
                         skyring="HTML í texta (hreinn texti krafist)")
                break
    if fjoldi:
        return nd.fell_("%d færslur bera HTML í texta." % fjoldi, fell=fjoldi)
    return nd.stodst_("Enginn HTML-texti í reitum.")


ALLAR = [H01, H02, H03, H04, H05, H06, H07, H08]

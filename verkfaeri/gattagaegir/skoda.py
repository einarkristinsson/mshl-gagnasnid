"""Skoða — ein OAI-beiðni í einu, þáttuð og hrá. Flettihluti Gáttagægis.

Gátlistinn (velin.py) keyrir margar beiðnir og dæmir. Þetta gerir eina:
notandinn velur verb, sett, snið eða auðkenni, sér svarið þáttað og hrátt,
og flettir sjálfur á næstu síðu með resumptionToken. Aldrei uppskera.

Sama biðill og gátlistinn (saekja.Saekjari): auðkennandi User-Agent,
kurteisishlé, engin sjálfvirk beining nema beðið sé um hana, og vörnin
(vorn.py) í opinni útgáfu.
"""
from . import notandastrengur
from . import xml_lestur as xl
from .saekja import Saekjari

VERB = ("Identify", "ListMetadataFormats", "ListSets",
        "ListIdentifiers", "ListRecords", "GetRecord")
ROK = ("metadataPrefix", "identifier", "set", "from", "until",
       "resumptionToken")
HAMARK_XML = 2 * 1024 * 1024   # hrátt XML sem fer til vafrans

# Hverju hver aðgerð á að skila — birt í skjölunarhluta síðunnar líka.
LYSING = {
    "Identify": "hver veitan er: nafn, baseURL, adminEmail, elsti dagstimpill",
    "ListMetadataFormats": "hvaða snið eru í boði — oai_dc er skylda",
    "ListSets": "hvaða gagnasett (set) má sækja sér",
    "ListIdentifiers": "hausar allra færslna, síða fyrir síðu",
    "ListRecords": "færslurnar sjálfar, síða fyrir síðu",
    "GetRecord": "ein færsla eftir auðkenni",
}


def _reitur(r):
    return {"nafn": r.nafn, "gildi": r.gildi, "lang": r.lang,
            "xsi_type": r.xsi_type, "eigindir": r.eigindir}


def _haus(f):
    return {"audkenni": f.audkenni, "dagstimpill": f.dagstimpill,
            "sett": list(f.sett), "eydd": f.eydd}


def _faersla(f):
    ut = _haus(f)
    ut["reitir"] = [_reitur(r) for r in f.reitir]
    ut["hefur_metadata"] = f.hefur_metadata
    return ut


def _snid(skjal):
    ut = []
    for mf in skjal.rot.iter("{%s}metadataFormat" % xl.OAI):
        eitt = {}
        for barn in mf:
            nafn = barn.tag.split("}", 1)[-1]
            eitt[nafn] = (barn.text or "").strip()
        ut.append({"prefix": eitt.get("metadataPrefix", ""),
                   "schema": eitt.get("schema", ""),
                   "namespace": eitt.get("metadataNamespace", "")})
    return ut


def skoda(slod, verb, rok=None, bid=0.25, netfang=None, vorn=None, elta=True):
    """Ein OAI-beiðni. Skilar JSON-hæfri orðabók, aldrei kastar."""
    ut = {"verb": verb, "slod": slod, "stada": None, "content_type": None,
          "ms": 0, "baeti": 0, "beint": [], "nadist": False, "hafnad": False,
          "villa": None, "gilt_xml": False, "xml_villa": None,
          "er_html": False, "oai_villa": None, "domur": None,
          "thattad": {}, "xml": ""}
    if verb not in VERB:
        ut["villa"] = "Óþekkt verb: %r. Leyfð: %s" % (verb, ", ".join(VERB))
        ut["domur"] = "villa"
        return ut
    rok = {k: v for k, v in (rok or {}).items()
           if k in ROK and v not in (None, "")}
    if "resumptionToken" in rok:
        # Staðallinn: token er einkarök. SMB og Ísmús svara badArgument
        # ef metadataPrefix fylgir með.
        rok = {"resumptionToken": rok["resumptionToken"]}

    sk = Saekjari(slod, notandastrengur(netfang), bid=bid, vorn=vorn)
    svar = sk.oai(verb, elta=elta, **rok)
    ut.update(slod=svar.slod, stada=svar.stada,
              content_type=svar.haus("content-type") or None, ms=svar.ms,
              baeti=len(svar.gogn), beint=list(svar.beint),
              nadist=svar.nadist, hafnad=bool(getattr(svar, "hafnad", False)),
              villa=svar.villa)
    if not svar.nadist:
        ut["domur"] = "nadist_ekki"
        return ut

    skjal = xl.lesa(svar)
    ut["gilt_xml"] = skjal.gilt
    ut["er_html"] = skjal.er_html
    ut["xml_villa"] = skjal.villa
    ut["xml"] = (svar.texti or "")[:HAMARK_XML]
    if not skjal.gilt:
        ut["domur"] = "html_ekki_xml" if skjal.er_html else "ogilt_xml"
        return ut
    v = xl.oai_villa(skjal)
    if v:
        ut["oai_villa"] = {"kodi": v[0], "texti": v[1]}
        ut["domur"] = "oai_villa"
        return ut

    th = {}
    if verb == "Identify":
        th = xl.identify(skjal)
    elif verb == "ListMetadataFormats":
        snid = _snid(skjal)
        th = {"snid": snid, "prefixar": [s["prefix"] for s in snid]}
    elif verb == "ListSets":
        th = {"sett": [{"spec": a, "nafn": b} for a, b in xl.sett_ur(skjal)]}
    elif verb == "ListIdentifiers":
        token, cls, cursor = xl.resumption(skjal)
        th = {"hausar": [_haus(f) for f in xl.hausar(skjal)],
              "token": token, "completeListSize": cls, "cursor": cursor}
    else:  # ListRecords, GetRecord
        token, cls, cursor = xl.resumption(skjal)
        th = {"faerslur": [_faersla(f) for f in xl.faerslur(skjal)],
              "token": token, "completeListSize": cls, "cursor": cursor}
    ut["thattad"] = th
    ut["domur"] = "ok"
    return ut

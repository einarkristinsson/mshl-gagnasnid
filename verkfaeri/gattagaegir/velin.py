"""Vélin — raðar athugunum, sækir sýnið og streymir niðurstöðum.

Fasar:
  A  sækja: Identify (GET+POST), ListMetadataFormats, ListSets,
     ListIdentifiers (síða 1), ListRecords (ganga), GetRecord (sýni).
  B  athuganir yfir söfnuð gögn (endapunktur, færslur, hreinlæti, gildi).
"""
import datetime
import time

from . import UTGAFA, notandastrengur
from . import xml_lestur as xl
from .saekja import Saekjari, Haett
from .athuganir import Samhengi, HOPHEITI, SLEPPT, ABENDING, ENDAPUNKTUR
from .athuganir import endapunktur, faerslur as faersluath, hreinlaeti, gildi


def _nuna():
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def _saekja_fasi(s, ut):
    """Fasi A: sækja öll svör og fylla Samhengi. ut = event-listi."""
    sk = s.saekjari

    def skra(nafn, svar):
        s.hra[nafn] = svar
        s.oll_svor.append(svar)
        skjal = xl.lesa(svar)
        s.svor[nafn] = skjal
        ut.append({"tegund": "beidni", "nafn": nafn, "adferd": svar.adferd,
                   "stada": svar.stada, "ms": svar.ms,
                   "baeti": len(svar.gogn), "beint": svar.beint,
                   "nadist": svar.nadist})
        return skjal

    # Identify (fylgja beiningu til að ná gögnunum)
    idf = sk.oai("Identify", elta=True)
    skid = skra("identify", idf)
    s.identify = xl.identify(skid)
    if not idf.nadist:
        ut.append({"tegund": "villa",
                   "skilabod": "Náðist ekki í þjóninn: %s" % idf.villa})

    # Identify með POST (til að sjá 301-gildruna)
    skra("identify_post", sk.oai("Identify", adferd="POST"))
    # ListMetadataFormats + ListSets
    skra("listmetadataformats", sk.oai("ListMetadataFormats"))
    skra("listsets", sk.oai("ListSets"))
    # ListIdentifiers síða 1
    li = skra("listidentifiers", sk.oai("ListIdentifiers",
                                        metadataPrefix="oai_dc"))
    s.hausar_p1 = xl.hausar(li)

    # ListRecords ganga
    hamark = s.stillingar.get("sidur", 3)
    token = None
    brotnar = []
    fyrsta_skjal = None
    for i in range(hamark):
        if token:
            svar = sk.oai("ListRecords", resumptionToken=token)
        else:
            svar = sk.oai("ListRecords", metadataPrefix="oai_dc")
        s.oll_svor.append(svar)
        skjal = xl.lesa(svar)
        if i == 0:
            fyrsta_skjal = skjal
            s.hra["listrecords"] = svar
        ut.append({"tegund": "beidni", "nafn": "listrecords#%d" % (i + 1),
                   "adferd": svar.adferd, "stada": svar.stada,
                   "ms": svar.ms, "baeti": len(svar.gogn),
                   "beint": svar.beint, "nadist": svar.nadist})
        if not skjal.gilt:
            brotnar.append(svar.texti)
            break
        v = xl.oai_villa(skjal)
        if v:
            break
        s.faerslur.extend(xl.faerslur(skjal))
        s.listrecords_sidur += 1
        token, cls, _cursor = xl.resumption(skjal)
        if cls is not None:
            s.completeListSize = cls
        s.token = token
        if not token:
            break
    s.svor["listrecords"] = fyrsta_skjal
    s.svor["_listrecords_brotnar"] = brotnar

    # GetRecord sýni
    syni = s.stillingar.get("syni", 10)
    audkenni = [h.audkenni for h in s.hausar_p1
                if h.audkenni and not h.eydd][:syni]
    naud = {f.audkenni for f in s.faerslur}
    for aud in audkenni:
        svar = sk.oai("GetRecord", identifier=aud, metadataPrefix="oai_dc")
        s.oll_svor.append(svar)
        skjal = xl.lesa(svar)
        s.getrecord_fjoldi += 1
        for f in xl.faerslur(skjal):
            if f.audkenni not in naud:
                s.faerslur.append(f)
                naud.add(f.audkenni)


def _faerslur_json(s, nidurstodur):
    """Byggir drill-down gögn með athugasemdum úr niðurstöðum."""
    eftir_aud = {}
    for nd in nidurstodur:
        for t in nd.tilvik:
            if t.get("audkenni"):
                eftir_aud.setdefault(t["audkenni"], []).append(
                    {"athugun": nd.kenni, "alvarleiki": nd.alvarleiki,
                     "reitur": t.get("reitur"),
                     "skilabod": t.get("skyring") or t.get("gildi")})
    ut = []
    for f in s.faerslur[:25]:
        ut.append({
            "audkenni": f.audkenni, "dagstimpill": f.dagstimpill,
            "sett": f.sett, "eydd": f.eydd,
            "reitir": [{"nafn": r.nafn, "lang": r.lang,
                        "xsi_type": r.xsi_type, "gildi": r.gildi,
                        "eigindir": r.eigindir} for r in f.reitir],
            "athugasemdir": eftir_aud.get(f.audkenni, []),
        })
    return ut


def keyra(slod, stillingar=None, stopp=None, netfang=None):
    """Aðalgangvirkið. Skilar rennsli (generator) af atburðum."""
    stillingar = dict({"sidur": 3, "syni": 10, "sett": 5,
                       "slodaprof": True, "bid_ms": 250}, **(stillingar or {}))
    ua = notandastrengur(netfang)
    bid = stillingar.get("bid_ms", 250) / 1000.0
    sk = Saekjari(slod, ua, bid=bid, stopp=stopp)
    s = Samhengi(slod, sk, stillingar, stopp)
    kenni = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    byrjad = _nuna()
    t0 = time.time()

    ut = []
    yield {"tegund": "byrjun", "kenni": kenni, "slod": slod,
           "stillingar": stillingar, "utgafa": UTGAFA, "byrjad": byrjad}

    try:
        _saekja_fasi(s, ut)
    except Haett:
        yield {"tegund": "haett", "skilabod": "Hætt við í miðri göngu."}
        return
    for atburd in ut:
        yield atburd

    allar = ([("A", f) for f in endapunktur.ALLAR]
             + [("B", f) for f in faersluath.ALLAR]
             + [("C", f) for f in hreinlaeti.ALLAR]
             + [("D", f) for f in gildi.ALLAR])
    nidurstodur = []
    for _fasi, fn in allar:
        if stopp is not None and stopp.is_set():
            break
        try:
            nd = fn(s)
        except Exception as e:  # ein athugun má ekki fella heildina
            nd = s.n(fn.__name__, ENDAPUNKTUR, fn.__name__, ABENDING)
            nd.sleppt_("Innri villa í athugun: %s" % e)
        nidurstodur.append(nd)
        yield {"tegund": "athugun", **nd.json()}

    faerslur_json = _faerslur_json(s, nidurstodur)
    for fj in faerslur_json:
        yield {"tegund": "faersla", **fj}

    skyrsla = _byggja_skyrslu(s, nidurstodur, kenni, slod, byrjad, t0,
                              faerslur_json)
    yield {"tegund": "lok", "skyrsla": skyrsla}


def _byggja_skyrslu(s, nidurstodur, kenni, slod, byrjad, t0, faerslur_json):
    from .athuganir import STODST, FELL, VILLA, ADVORUN
    samantekt = {"villur": 0, "advaranir": 0, "abendingar": 0,
                 "stodst": 0, "sleppt": 0}
    for nd in nidurstodur:
        if nd.stada == STODST:
            samantekt["stodst"] += 1
        elif nd.stada == SLEPPT:
            samantekt["sleppt"] += 1
        elif nd.stada == FELL:
            if nd.alvarleiki == VILLA:
                samantekt["villur"] += 1
            elif nd.alvarleiki == ADVORUN:
                samantekt["advaranir"] += 1
            else:
                samantekt["abendingar"] += 1

    hopar_rod = ["endapunktur", "faerslur", "hreinlaeti", "gildi"]
    hopar = []
    for h in hopar_rod:
        athuganir = [nd.json() for nd in nidurstodur if nd.hopur == h]
        hopar.append({"kenni": h, "heiti": HOPHEITI[h],
                      "athuganir": athuganir})

    from . import skyrsla as skmodul
    skyrsla = {
        "kenni": kenni, "slod": slod, "utgafa": UTGAFA,
        "baseurl_auglyst": s.identify.get("baseURL"),
        "byrjad": byrjad, "lokid": _nuna(),
        "identify": {
            "repositoryName": s.identify.get("repositoryName"),
            "adminEmail": s.identify.get("adminEmail", []),
            "granularity": s.identify.get("granularity"),
            "earliestDatestamp": s.identify.get("earliestDatestamp"),
            "deletedRecord": s.identify.get("deletedRecord"),
            "protocolVersion": s.identify.get("protocolVersion"),
            "metadataPrefixes": s.identify.get("metadataPrefixes", []),
        },
        "syni": {
            "faerslur": len([f for f in s.faerslur if f.audkenni]),
            "listrecords_sidur": s.listrecords_sidur,
            "getrecord": s.getrecord_fjoldi,
            "beidnir": len(s.saekjari.beidnir),
            "completeListSize": s.completeListSize,
        },
        "samantekt": samantekt,
        "hopar": hopar,
        "faerslur": faerslur_json,
        "beidnir": s.saekjari.beidnir,
    }
    skyrsla["texti"] = skmodul.markdown(skyrsla)
    return skyrsla


def keyra_allt(slod, stillingar=None, stopp=None, netfang=None):
    """Þægindafall: keyrir allt og skilar lokaskýrslunni (dict)."""
    skyrsla = None
    for atburd in keyra(slod, stillingar, stopp, netfang):
        if atburd["tegund"] == "lok":
            skyrsla = atburd["skyrsla"]
    return skyrsla

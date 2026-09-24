"""Athuganir á endapunktinum sjálfum (OAI-PMH afhendingin)."""
import datetime
import re

from .. import xml_lestur as xl
from . import (ENDAPUNKTUR, VILLA, ADVORUN, ABENDING, Nidurstada)

DOC = "oai-pmh/LEIDBEININGAR.md"
_NETFANG = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def _nd(s, kenni, heiti, alv, gildra=False):
    return s.n(kenni, ENDAPUNKTUR, heiti, alv, gildra, DOC)


def E01(s):
    nd = _nd(s, "E01", "Identify svarar", VILLA)
    sk = s.svor.get("identify")
    hra = s.hra.get("identify")
    if hra is not None and not hra.nadist:
        return nd.sleppt_("Náðist ekki í þjóninn: %s" % hra.villa)
    if sk is None or not sk.gilt:
        return nd.fell_("Identify skilaði ekki gildu XML.")
    v = xl.oai_villa(sk)
    if v:
        return nd.fell_("Identify skilaði OAI-villu: %s" % v[0])
    idn = s.identify
    vantar = [k for k in ("repositoryName", "baseURL", "protocolVersion")
              if not idn.get(k)]
    if vantar:
        return nd.fell_("Identify vantar: %s" % ", ".join(vantar))
    if idn.get("protocolVersion") != "2.0":
        nd.baeta(gildi=idn.get("protocolVersion"),
                 skyring="protocolVersion ætti að vera 2.0")
    return nd.stodst_("repositoryName: %s" % idn.get("repositoryName"))


def E02(s):
    nd = _nd(s, "E02", "baseURL virkar orðrétt", VILLA)
    auglyst = s.identify.get("baseURL")
    if not auglyst:
        return nd.sleppt_("baseURL ekki auglýst í Identify.")
    hreinsud = s.slod.split("?", 1)[0].rstrip("/")
    if auglyst.rstrip("/") != hreinsud:
        nd.baeta(gildi=auglyst,
                 skyring="auglýst baseURL er ekki sama og prófaða slóðin")
    skil = "&" if "?" in auglyst else "?"
    svar = s.saekjari.profa_slod(auglyst + skil + "verb=Identify", "GET")
    if not svar.nadist:
        return nd.fell_("baseURL svaraði ekki: %s" % svar.villa)
    if 300 <= (svar.stada or 0) < 400:
        return nd.fell_(
            "GET á auglýsta baseURL fór í %s (%s) — slóðin sem er auglýst "
            "er ekki sú sem virkar." % (svar.stada, svar.haus("location")),
            lagfaering="Auglýstu í baseURL þá slóð sem svarar beint (t.d. "
                       "með skástriki), eða láttu slóðina svara sjálf.")
    sk = xl.lesa(svar)
    if sk.gilt and sk.rot.find("{%s}Identify" % xl.OAI) is not None:
        return nd.stodst_("baseURL svarar Identify beint.")
    return nd.fell_("baseURL svaraði %s en ekki gildu Identify."
                    % svar.stada)


def E03(s):
    nd = _nd(s, "E03", "GET og POST virka bæði á slóðinni", VILLA,
             gildra=True)
    svar = s.hra.get("identify_post")
    if svar is None:
        return nd.sleppt_("POST-prófun var ekki keyrð.")
    if not svar.nadist:
        return nd.fell_("POST náði ekki sambandi: %s" % svar.villa)
    if 300 <= (svar.stada or 0) < 400:
        return nd.fell_(
            "POST fór í %s → %s; meginmál beiðninnar féll niður."
            % (svar.stada, svar.haus("location")),
            lagfaering="Láttu slóðina svara POST beint, án 3xx-beiningar.")
    sk = xl.lesa(svar)
    v = xl.oai_villa(sk)
    if v and v[0] == "badVerb":
        return nd.fell_("POST skilaði badVerb — POST er ekki studdur á "
                        "slóðinni.", lagfaering="Staðallinn krefst GET og "
                        "POST (kafli 3.1.1.3).")
    if svar.stada == 405:
        return nd.fell_("POST skilaði 405 (aðferð ekki leyfð).")
    if sk.gilt and sk.rot.find("{%s}Identify" % xl.OAI) is not None:
        return nd.stodst_("Bæði GET og POST skila Identify.")
    return nd.fell_("POST skilaði %s en ekki gildu Identify." % svar.stada)


def E04(s):
    nd = _nd(s, "E04", "adminEmail er til staðar", VILLA, gildra=True)
    netfong = [e for e in s.identify.get("adminEmail", []) if e]
    if not netfong:
        return nd.fell_("adminEmail vantar — enginn til að skrifa þegar "
                        "eitthvað bilar. Staðallinn krefst þess.")
    ogild = [e for e in netfong if not _NETFANG.search(e)]
    for e in ogild:
        nd.baeta(gildi=e, skyring="lítur ekki út eins og netfang")
    return nd.stodst_("adminEmail: %s" % ", ".join(netfong))


def E05(s):
    nd = _nd(s, "E05", "earliestDatestamp og granularity gild", ADVORUN)
    g = s.identify.get("granularity")
    ed = s.identify.get("earliestDatestamp")
    if not g:
        return nd.fell_("granularity vantar í Identify.")
    if g not in ("YYYY-MM-DD", "YYYY-MM-DDThh:mm:ssZ"):
        nd.baeta(gildi=g, skyring="óþekkt granularity")
        return nd.fell_("granularity er óþekkt: %s" % g)
    if not ed:
        return nd.fell_("earliestDatestamp vantar.")
    return nd.stodst_("granularity: %s · earliestDatestamp: %s" % (g, ed))


def E06(s):
    nd = _nd(s, "E06", "deletedRecord er persistent", ABENDING)
    d = s.identify.get("deletedRecord")
    if not d:
        return nd.fell_("deletedRecord vantar í Identify.")
    if d == "persistent":
        return nd.stodst_("deletedRecord: persistent")
    return nd.fell_("deletedRecord er '%s' — þá vitum við ekki með vissu "
                    "hvað á að hverfa (persistent er best)." % d)


def E07(s):
    nd = _nd(s, "E07", "ListMetadataFormats auglýsir oai_dc", VILLA)
    sk = s.svor.get("listmetadataformats")
    if sk is None or not sk.gilt:
        return nd.fell_("ListMetadataFormats skilaði ekki gildu XML.")
    prefixar = [(e.text or "").strip()
                for e in sk.rot.iter("{%s}metadataPrefix" % xl.OAI)]
    s.identify["metadataPrefixes"] = prefixar
    if "oai_dc" not in prefixar:
        return nd.fell_("oai_dc er ekki auglýst — það er skyldusniðið. "
                        "Auglýst snið: %s" % (", ".join(prefixar) or "engin"))
    return nd.stodst_("Auglýst snið: %s" % ", ".join(prefixar))


def E08(s):
    nd = _nd(s, "E08", "ListIdentifiers virkar", VILLA)
    sk = s.svor.get("listidentifiers")
    if sk is None or not sk.gilt:
        return nd.fell_("ListIdentifiers skilaði ekki gildu XML.")
    v = xl.oai_villa(sk)
    if v:
        return nd.fell_("ListIdentifiers skilaði OAI-villu: %s" % v[0])
    if not s.hausar_p1:
        return nd.fell_("ListIdentifiers skilaði engum hausum.")
    return nd.stodst_("%d hausar á fyrstu síðu." % len(s.hausar_p1))


def E09(s):
    nd = _nd(s, "E09", "ListRecords virkar", VILLA)
    sk = s.svor.get("listrecords")
    if sk is None or not sk.gilt:
        return nd.fell_("ListRecords skilaði ekki gildu XML (sjá E12).")
    v = xl.oai_villa(sk)
    if v:
        return nd.fell_("ListRecords skilaði OAI-villu: %s" % v[0])
    if not xl.faerslur(sk):
        return nd.fell_("ListRecords skilaði engum færslum.")
    return nd.stodst_("ListRecords síða 1 í lagi.")


def E10(s):
    nd = _nd(s, "E10", "GetRecord virkar", VILLA)
    if s.getrecord_fjoldi == 0:
        return nd.fell_("GetRecord skilaði engri færslu.")
    return nd.stodst_("GetRecord sótti %d sýnisfærslur." % s.getrecord_fjoldi)


def E11(s):
    nd = _nd(s, "E11", "resumptionToken gengur og talan stemmir", VILLA)
    if s.listrecords_sidur == 0:
        return nd.sleppt_("Engin ListRecords-ganga.")
    cls = s.completeListSize
    hamark = s.stillingar.get("sidur", 3)
    talid = len([f for f in s.faerslur if f.audkenni])
    if s.listrecords_sidur >= hamark and s.token:
        return nd.stodst_(
            "Gengið %d síður; token virkar. Full ganga (%s færslur) ekki "
            "keyrð til að hlífa þjóninum." % (s.listrecords_sidur,
                                              cls if cls else "?"))
    if not s.token:
        # göngunni lauk innan sýnis
        if cls is not None and talid != cls:
            nd.baeta(gildi="talið %d, completeListSize %d" % (talid, cls))
        return nd.stodst_("Ganga kláraðist (%d síður)." % s.listrecords_sidur)
    return nd.stodst_("resumptionToken í lagi (%d síður)."
                      % s.listrecords_sidur)


def E12(s):
    nd = _nd(s, "E12", "Ein skemmd færsla fellir ekki heildina", VILLA,
             gildra=True)
    li_ok = bool(s.hausar_p1)
    brotnar_sidur = s.svor.get("_listrecords_brotnar", [])
    if not brotnar_sidur:
        return nd.stodst_("Allar sóttar ListRecords-síður lásust (innan "
                          "sýnis).")
    if not li_ok:
        return nd.fell_("Bæði ListIdentifiers og ListRecords féllu.")
    fjoldi_brotinna = 0
    for texti in brotnar_sidur:
        _, brotin = xl.bjarga(texti)
        for b in brotin:
            fjoldi_brotinna += 1
            nd.baeta(audkenni=b, skyring="skemmd færsla felldi síðuna")
    return nd.fell_(
        "ListRecords féll á skemmdri síðu en ListIdentifiers virkar — "
        "%d skemmd(ar) færsla/ur nafngreindar." % fjoldi_brotinna,
        lagfaering="Sannreyndu XML við útgáfu og slepptu/merktu skemmdum "
                   "færslum í stað þess að láta þjóninn hrynja.")


def _dagur_ur(faerslur):
    for f in faerslur:
        if f.dagstimpill:
            return f.dagstimpill
    return None


def E13(s):
    nd = _nd(s, "E13", "from/until sía raunverulega", VILLA, gildra=True)
    if not s.hausar_p1:
        return nd.sleppt_("Engir hausar til að prófa síun á.")
    # (a) framtíðardagur á að skila engu
    amorgun = (datetime.date.today()
               + datetime.timedelta(days=1)).isoformat()
    sa = s.saekjari.oai("ListIdentifiers", metadataPrefix="oai_dc",
                        **{"from": amorgun})
    ska = xl.lesa(sa)
    va = xl.oai_villa(ska)
    haus_a = xl.hausar(ska)
    framtid_tomt = (va and va[0] == "noRecordsMatch") or len(haus_a) == 0
    # (b) þröngt bil á að lækka töluna
    dagur = _dagur_ur(s.hausar_p1)
    dsett = dagur.split("T", 1)[0] if dagur else None
    laekkar = None
    if dsett:
        sb = s.saekjari.oai("ListIdentifiers", metadataPrefix="oai_dc",
                            **{"from": dsett, "until": dsett})
        skb = xl.lesa(sb)
        vb = xl.oai_villa(skb)
        if vb and vb[0] == "noRecordsMatch":
            laekkar = True
        else:
            _, clb, _ = xl.resumption(skb)
            hb = xl.hausar(skb)
            fjoldi_b = clb if clb is not None else len(hb)
            heild = s.completeListSize
            if heild:
                laekkar = fjoldi_b < heild
            else:
                laekkar = len(hb) <= len(s.hausar_p1)
    if not framtid_tomt:
        return nd.fell_(
            "from=%s (á morgun) skilaði samt færslum — from/until er "
            "hunsað. Þá verður hver uppfærsla full uppskera." % amorgun)
    if laekkar is False:
        return nd.fell_("Þröngt from/until (%s) lækkaði ekki töluna — síun "
                        "virkar ekki." % dsett)
    return nd.stodst_("from/until sía virðist virka.")


def E14(s):
    nd = _nd(s, "E14", "Auglýst sett eru ekki tóm", VILLA, gildra=True)
    sk = s.svor.get("listsets")
    if sk is None or not sk.gilt:
        return nd.sleppt_("ListSets skilaði ekki gildu XML.")
    v = xl.oai_villa(sk)
    if v and v[0] == "noSetHierarchy":
        return nd.stodst_("Engin sett auglýst (noSetHierarchy).")
    sett = xl.sett_ur(sk)
    if not sett:
        return nd.stodst_("Engin sett auglýst.")
    hamark = s.stillingar.get("sett", 5)
    tom = []
    for spec, _nafn in sett[:hamark]:
        svar = s.saekjari.oai("ListIdentifiers", metadataPrefix="oai_dc",
                              set=spec)
        sksett = xl.lesa(svar)
        vv = xl.oai_villa(sksett)
        if (vv and vv[0] == "noRecordsMatch") or not xl.hausar(sksett):
            tom.append(spec)
            nd.baeta(gildi=spec, skyring="auglýst sett en skilar engu")
    if tom:
        return nd.fell_("Sett auglýst en tóm: %s" % ", ".join(tom),
                        skodad=min(len(sett), hamark), fell=len(tom))
    return nd.stodst_("Prófuð %d sett — engin tóm."
                      % min(len(sett), hamark))


def E15(s):
    nd = _nd(s, "E15", "Gagnasett (OAI set) skila aðeins eigin færslum", VILLA, gildra=True)
    sk = s.svor.get("listsets")
    if sk is None or not sk.gilt:
        return nd.sleppt_("Engin sett til að prófa leka á.")
    sett = xl.sett_ur(sk)
    if not sett:
        return nd.sleppt_("Engin sett auglýst.")
    spec = sett[0][0]
    hamark = s.stillingar.get("sidur", 3)
    token = None
    leki = 0
    skodad = 0
    for _ in range(hamark):
        if token:
            svar = s.saekjari.oai("ListIdentifiers", resumptionToken=token)
        else:
            svar = s.saekjari.oai("ListIdentifiers", metadataPrefix="oai_dc",
                                  set=spec)
        sksida = xl.lesa(svar)
        hausar = xl.hausar(sksida)
        for h in hausar:
            skodad += 1
            if h.sett and not any(x == spec or x.startswith(spec + ":")
                                  for x in h.sett):
                leki += 1
                nd.baeta(audkenni=h.audkenni,
                         skyring="er í setti '%s' en ber það ekki"
                                 % spec)
        token, _cls, _c = xl.resumption(sksida)
        if not token:
            break
    if leki:
        return nd.fell_("Sett '%s' inniheldur %d færslu(r) sem tilheyra því "
                        "ekki." % (spec, leki), skodad=skodad, fell=leki)
    return nd.stodst_("Set '%s': %d hausar skoðaðir, enginn leki (innan "
                      "sýnis)." % (spec, skodad))


def E16(s):
    nd = _nd(s, "E16", "Villur koma sem OAI-villukóðar, ekki HTML", VILLA,
             gildra=True)
    profanir = [
        ("badVerb", {"verb": "Gaegir"}),
        ("idDoesNotExist", {"verb": "GetRecord",
                            "identifier": "oai:gaegir:finnst-ekki",
                            "metadataPrefix": "oai_dc"}),
        ("cannotDisseminateFormat", {"verb": "ListRecords",
                                     "metadataPrefix": "gaegir_x"}),
        ("badArgument", {"verb": "ListIdentifiers"}),
    ]
    fell = 0
    for vaent, rok in profanir:
        verb = rok.pop("verb")
        svar = s.saekjari.oai(verb, **rok)
        sk = xl.lesa(svar)
        if sk.er_html or not sk.gilt:
            fell += 1
            nd.baeta(gildi="%s → HTML/ógilt" % vaent,
                     skyring="villa kom sem HTML eða PHP-villa, ekki OAI")
            continue
        v = xl.oai_villa(sk)
        if not v:
            fell += 1
            nd.baeta(gildi=vaent, skyring="engin OAI-villa þar sem hennar "
                                          "var vænst")
    if fell:
        return nd.fell_("%d af %d villuprófunum skiluðu ekki OAI-villukóða."
                        % (fell, len(profanir)), skodad=len(profanir),
                        fell=fell)
    return nd.stodst_("Allar %d villuprófanir skiluðu OAI-villukóðum."
                      % len(profanir))


def E17(s):
    nd = _nd(s, "E17", "Content-Type er XML með UTF-8", ADVORUN)
    hra = s.hra.get("identify")
    if hra is None or not hra.nadist:
        return nd.sleppt_("Ekkert Identify-svar til að skoða haus á.")
    ct = hra.haus("content-type").lower()
    if "xml" not in ct:
        return nd.fell_("Content-Type er '%s' — ætti að innihalda 'xml'."
                        % (ct or "(vantar)"))
    if "charset" in ct and "utf-8" not in ct:
        return nd.fell_("Content-Type charset er ekki utf-8: %s" % ct)
    return nd.stodst_("Content-Type: %s" % ct)


ALLAR = [E01, E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13,
         E14, E15, E16, E17]

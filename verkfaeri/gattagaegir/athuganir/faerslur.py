"""Athuganir á færslunum sjálfum — gullna sniðið, reitur fyrir reit."""
import re

from . import (FAERSLUR, VILLA, ADVORUN, ABENDING)

DOC = "snidmat/GULLNA-SNIDID.md"
_SLOD = re.compile(r"^https?://", re.IGNORECASE)
_MYND = re.compile(r"\.(jpe?g|png|webp|gif)(\?.*)?$", re.IGNORECASE)
_MYND_STIGUR = re.compile(r"/(multimedia|thumb|thumbnail|image|images|mynd|"
                          r"myndir)/", re.IGNORECASE)
_TIMABUNDID = re.compile(r"(token=|expires=|sig=|signature=|x-amz-)",
                         re.IGNORECASE)


def _nd(s, kenni, heiti, alv, gildra=False):
    return s.n(kenni, FAERSLUR, heiti, alv, gildra, DOC)


def _berandi(s):
    """Færslur sem geta borið gildi (ekki eyddar, hafa metadata)."""
    return [f for f in s.faerslur if not f.eydd and f.reitir]


def _myndaslodir(f):
    ut = []
    for r in f.reitir_heitir("dc:identifier"):
        if _MYND.search(r.gildi) or _MYND_STIGUR.search(r.gildi):
            ut.append(r.gildi)
    return ut


def _sidusslodir(f):
    ut = []
    for r in f.reitir_heitir("dc:identifier"):
        if _SLOD.search(r.gildi) and not (_MYND.search(r.gildi)
                                          or _MYND_STIGUR.search(r.gildi)):
            ut.append(r.gildi)
    return ut


def F01(s):
    nd = _nd(s, "F01", "dc:title á öllum, aldrei tómur", VILLA)
    faerslur = _berandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    an_titils = 0
    an_lang = 0
    for f in faerslur:
        titlar = [r for r in f.reitir_heitir("dc:title") if r.gildi]
        if not titlar:
            an_titils += 1
            nd.baeta(audkenni=f.audkenni, reitur="dc:title",
                     skyring="vantar eða tómur")
        elif not any(r.lang == "is" for r in titlar):
            an_lang += 1
    if an_titils:
        return nd.fell_("%d af %d færslum vantar dc:title."
                        % (an_titils, len(faerslur)),
                        skodad=len(faerslur), fell=an_titils)
    skil = "Allar %d færslur bera dc:title." % len(faerslur)
    if an_lang:
        skil += " (%d án xml:lang=\"is\")" % an_lang
    return nd.stodst_(skil)


def F02(s):
    nd = _nd(s, "F02", "dc:identifier með varanlegri slóð", VILLA)
    faerslur = _berandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    an = 0
    for f in faerslur:
        if not _sidusslodir(f):
            an += 1
            nd.baeta(audkenni=f.audkenni, reitur="dc:identifier",
                     skyring="engin slóð (tengill heim) fannst")
    if an:
        return nd.fell_("%d af %d færslum vantar slóð í dc:identifier."
                        % (an, len(faerslur)), skodad=len(faerslur), fell=an)
    return nd.stodst_("Allar %d færslur bera slóð." % len(faerslur))


def F03(s):
    nd = _nd(s, "F03", "Slóðin svarar 200 (ekki 302 á forsíðu)", VILLA)
    if not s.stillingar.get("slodaprof", True):
        return nd.sleppt_("Slóðaprófun var slökkt.")
    faerslur = [f for f in _berandi(s) if _sidusslodir(f)]
    if not faerslur:
        return nd.sleppt_("Engar slóðir til að prófa.")
    fell = 0
    skodad = 0
    for f in faerslur[:10]:
        url = _sidusslodir(f)[0]
        svar = s.saekjari.profa_slod(url, "HEAD")
        if not svar.nadist or svar.stada == 405:
            svar = s.saekjari.profa_slod(url, "GET")
        skodad += 1
        if not svar.nadist:
            fell += 1
            nd.baeta(audkenni=f.audkenni, gildi=url,
                     skyring="náðist ekki: %s" % svar.villa)
        elif 300 <= (svar.stada or 0) < 400:
            loc = svar.haus("location")
            fell += 1
            rot = bool(re.match(r"^https?://[^/]+/?$", loc)) or loc in (
                "/", "")
            nd.baeta(audkenni=f.audkenni, gildi="%s → %s"
                     % (svar.stada, loc),
                     skyring=("beining á forsíðu, ekki hlutinn" if rot
                              else "varanleg slóð á að svara 200, ekki %s"
                              % svar.stada))
        elif (svar.stada or 0) >= 400:
            fell += 1
            nd.baeta(audkenni=f.audkenni, gildi=str(svar.stada),
                     skyring="slóð svarar villu")
    if fell:
        return nd.fell_("%d af %d prófuðum slóðum svara ekki 200."
                        % (fell, skodad), skodad=skodad, fell=fell)
    return nd.stodst_("Allar %d prófaðar slóðir svara 200." % skodad)


def F04(s):
    nd = _nd(s, "F04", "dc:type sem par: @is og @en", VILLA)
    faerslur = _berandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    fell = 0
    for f in faerslur:
        typur = [r for r in f.reitir_heitir("dc:type") if r.gildi]
        hefur_is = any(r.lang == "is" for r in typur)
        hefur_en = any(r.lang == "en" for r in typur)
        if not (hefur_is and hefur_en):
            fell += 1
            if typur and not any(r.lang for r in typur):
                skyr = "dc:type án @lang (þarf ensk og íslensk heiti)"
            else:
                skyr = "vantar par @is + @en"
            nd.baeta(audkenni=f.audkenni, reitur="dc:type", skyring=skyr)
    if fell:
        return nd.fell_("%d af %d færslum vantar dc:type par (@is + @en). "
                        "Enska gildið stýrir flokkuninni."
                        % (fell, len(faerslur)),
                        skodad=len(faerslur), fell=fell)
    return nd.stodst_("Allar %d færslur bera dc:type par." % len(faerslur))


def F05(s):
    nd = _nd(s, "F05", "dc:subject á öllum sem geta borið það", VILLA)
    faerslur = _berandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    med = sum(1 for f in faerslur
              if any(r.gildi for r in f.reitir_heitir("dc:subject")))
    hlutf = 100.0 * med / len(faerslur)
    if med == 0:
        return nd.fell_("Engin færsla ber dc:subject — samleitarlykill #1 "
                        "vantar alveg.")
    if hlutf < 90:
        return nd.fell_("Aðeins %.0f%% færslna bera dc:subject." % hlutf,
                        skodad=len(faerslur), fell=len(faerslur) - med)
    return nd.stodst_("%.0f%% færslna bera dc:subject (samleitarlykill #1)."
                      % hlutf)


def F06(s):
    nd = _nd(s, "F06", "Staðarreitur á öllum sem geta borið hann", ADVORUN)
    faerslur = _berandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")

    def hefur_stad(f):
        for nafn in ("dcterms:spatial", "dc:coverage"):
            for r in f.reitir_heitir(nafn):
                if r.gildi and r.xsi_type != "dcterms:Point":
                    return True
        return False

    med = sum(1 for f in faerslur if hefur_stad(f))
    hlutf = 100.0 * med / len(faerslur)
    if med == 0:
        return nd.fell_("Engin færsla ber staðarreit — samleitarlykill #2 "
                        "vantar.")
    return nd.stodst_("%.0f%% færslna bera staðarreit (samleitarlykill #2)."
                      % hlutf)


def F07(s):
    nd = _nd(s, "F07", "Smámyndaslóð: bein, opin, aðgreinanleg", ADVORUN)
    faerslur = _berandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    med_mynd = [f for f in faerslur if _myndaslodir(f)]
    if not med_mynd:
        nd.alvarleiki = ABENDING
        return nd.fell_("Engin færsla ber smámyndaslóð — reiturinn sem "
                        "oftast gleymist. Færsla með mynd er margfalt "
                        "gagnlegri.")
    # aðgreinanleiki með regex: mynd vs síða
    allar_myndir = [u for f in med_mynd for u in _myndaslodir(f)]
    allar_sidur = [u for f in faerslur for u in _sidusslodir(f)]
    skorun = [u for u in allar_myndir if u in allar_sidur]
    if skorun:
        nd.baeta(gildi=skorun[0],
                 skyring="myndslóð er ekki aðgreinanleg frá síðuslóð")
        return nd.fell_("Myndslóðir eru ekki aðgreinanlegar frá síðuslóðum "
                        "með regex.")
    # bein + opin (netprófun)
    fell = 0
    skodad = 0
    if s.stillingar.get("slodaprof", True):
        for f in med_mynd[:10]:
            url = _myndaslodir(f)[0]
            svar = s.saekjari.profa_slod(url, "HEAD")
            if not svar.nadist or svar.stada == 405:
                svar = s.saekjari.profa_slod(url, "GET")
            skodad += 1
            ct = svar.haus("content-type").lower()
            if not svar.nadist:
                fell += 1
                nd.baeta(audkenni=f.audkenni, gildi=url,
                         skyring="náðist ekki")
            elif svar.stada in (401, 403):
                fell += 1
                nd.baeta(audkenni=f.audkenni, gildi=url,
                         skyring="krefst innskráningar (%s)" % svar.stada)
            elif "text/html" in ct:
                fell += 1
                nd.baeta(audkenni=f.audkenni, gildi=url,
                         skyring="slóð á síðu, ekki mynd (text/html)")
            elif _TIMABUNDID.search(url):
                nd.baeta(audkenni=f.audkenni, gildi=url,
                         skyring="tímabundið auðkenni í slóð?")
    if fell:
        nd.alvarleiki = VILLA
        return nd.fell_("%d af %d smámyndaslóðum eru ekki beinar/opnar."
                        % (fell, skodad), skodad=skodad, fell=fell)
    return nd.stodst_("%d/%d færslna bera aðgreinanlega smámyndaslóð."
                      % (len(med_mynd), len(faerslur)))


def F08(s):
    nd = _nd(s, "F08", "dc:rights segir hvað má", ADVORUN)
    faerslur = _berandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    an = 0
    frjals = 0
    for f in faerslur:
        rettur = [r for r in f.reitir_heitir("dc:rights") if r.gildi]
        if not rettur:
            an += 1
        elif not any(_SLOD.search(r.gildi) for r in rettur):
            frjals += 1
    if an:
        return nd.fell_("%d af %d færslum vantar dc:rights."
                        % (an, len(faerslur)), skodad=len(faerslur), fell=an)
    skil = "Allar færslur bera dc:rights."
    if frjals:
        skil += " (%d með frjálsan texta — leyfisslóð ráðlögð)" % frjals
    return nd.stodst_(skil)


def F09(s):
    nd = _nd(s, "F09", "dc:language með ISO-kóða", ADVORUN)
    faerslur = _berandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    fell = 0
    for f in faerslur:
        mal = [r.gildi for r in f.reitir_heitir("dc:language") if r.gildi]
        if not mal:
            continue
        for m in mal:
            if not re.match(r"^[a-z]{2,3}(-[A-Za-z]{2,4})?$", m):
                fell += 1
                nd.baeta(audkenni=f.audkenni, reitur="dc:language", gildi=m,
                         skyring="ekki ISO-kóði (nota t.d. 'is')")
                break
    if fell:
        return nd.fell_("%d færslur bera dc:language sem er ekki ISO-kóði."
                        % fell, fell=fell)
    return nd.stodst_("dc:language er ISO-kóði þar sem hann er til staðar.")


def F10(s):
    nd = _nd(s, "F10", "dc:publisher á öllum", ADVORUN)
    faerslur = _berandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    an = sum(1 for f in faerslur
             if not any(r.gildi for r in f.reitir_heitir("dc:publisher")))
    if an:
        return nd.fell_("%d af %d færslum vantar dc:publisher."
                        % (an, len(faerslur)), fell=an)
    return nd.stodst_("Allar færslur bera dc:publisher.")


def F12(s):
    nd = _nd(s, "F12", "dc:source er ekki slóð", ADVORUN)
    faerslur = _berandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    fell = 0
    for f in faerslur:
        for r in f.reitir_heitir("dc:source"):
            if _SLOD.search(r.gildi):
                fell += 1
                nd.baeta(audkenni=f.audkenni, reitur="dc:source",
                         gildi=r.gildi,
                         skyring="slóðir fara í dc:identifier, ekki dc:source")
                break
    if fell:
        return nd.fell_("%d færslur bera slóð í dc:source." % fell, fell=fell)
    return nd.stodst_("dc:source ber engar slóðir.")


def F13(s):
    nd = _nd(s, "F13", "Engir eigin reitir inni í oai_dc", ADVORUN)
    from .. import xml_lestur as xl
    leyfd = (xl.DC, xl.DCTERMS)
    faerslur = _berandi(s)
    if not faerslur:
        return nd.sleppt_("Engar færslur í sýni.")
    framandi = set()
    for f in faerslur:
        for r in f.reitir:
            if r.ns not in leyfd:
                framandi.add(r.nafn)
                nd.baeta(audkenni=f.audkenni, reitur=r.nafn,
                         skyring="eigin reitur inni í oai_dc-nafnrými")
    if framandi:
        return nd.fell_("Eigin reitir inni í oai_dc: %s. Notið dcterms eða "
                        "eigin metadataPrefix við hlið oai_dc."
                        % ", ".join(sorted(framandi)))
    return nd.stodst_("Aðeins DC/DCTERMS reitir inni í oai_dc.")


ALLAR = [F01, F02, F03, F04, F05, F06, F07, F08, F09, F10, F12, F13]

#!/usr/bin/env python3
"""skyringar.py — hvað villan þýðir, og hvað á að gera við hana.

Skoðarinn sýnir hráa svarið. Þessi eining segir hvað það ÞÝÐIR: OAI-villukóðar,
HTTP-stöður, raunveruleg bilunarmynstur sem við höfum mælt, og tilvísanir í
staðalinn sjálfan.

Öll mynstrin hér eiga sér mælingu í þessu verkefni, ekki bara lestur á
staðlinum. Þess vegna er `maelt`-reiturinn með — hann segir hvar það kom upp.

    import skyringar
    skyringar.oai_villa("badArgument")       -> dict eða None
    skyringar.http_stada(301)                -> dict eða None
    skyringar.finna_mynstur(text, stada)     -> listi af dict
    skyringar.skoda_identify(xml_text)       -> listi af dict (skyldureitir)
    skyringar.allt()                         -> allt sem JSON-tækt dict

Prófun:  python3 skyringar.py
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET

SPEC = "https://www.openarchives.org/OAI/openarchivesprotocol.html"

# ---------------------------------------------------------------- OAI-villukóðar
# Staðallinn skilgreinir nákvæmlega sex. Allt annað er ekki OAI-villa.
OAI_VILLUR = {
    "badArgument": {
        "heiti": "Rangt viðfang",
        "hvad": "Beiðnin ber viðfang sem á ekki við þetta verb, endurtekið viðfang, "
                "eða vantar skylduviðfang.",
        "gera": "Algengast hjá okkur: að senda bæði resumptionToken OG metadataPrefix. "
                "Þegar token er notað má EKKERT annað fylgja nema verb.",
        "maelt": "SMB og Ísmús svara badArgument ef prefix fylgir token.",
        "spec": SPEC + "#ErrorConditions",
    },
    "badVerb": {
        "heiti": "Óþekkt verb",
        "hvad": "Verb-viðfangið vantar, er ólöglegt, eða kom oftar en einu sinni.",
        "gera": "Ef þú sendir POST og færð badVerb: athugaðu hvort slóðin endi á "
                "skástriki. 301-endurvísun hendir meginmáli POST-beiðni og þá kemur "
                "hún verb-laus á áfangastað.",
        "maelt": "Jarðir: POST á /oai (án /) skilaði badVerb; /oai/ virkaði.",
        "spec": SPEC + "#ErrorConditions",
    },
    "cannotDisseminateFormat": {
        "heiti": "Sniðið er ekki í boði",
        "hvad": "Þjónninn styður ekki það metadataPrefix sem beðið var um — "
                "hvorki fyrir safnið í heild né þessa tilteknu færslu.",
        "gera": "Keyrðu ListMetadataFormats og sjáðu hvað er raunverulega í boði. "
                "oai_dc er skyldusnið skv. staðlinum en það er ekki alltaf virt.",
        "maelt": "Ísmús styður AÐEINS isebel; oai_dc skilar þessari villu þótt "
                 "skemað vísi sjálft á oai_dc.xsd.",
        "spec": SPEC + "#ListMetadataFormats",
    },
    "idDoesNotExist": {
        "heiti": "Auðkennið er ekki til",
        "hvad": "Ekkert er til með þessu identifier — eða það er ekki á því formi "
                "sem þjónninn notar.",
        "gera": "Sæktu auðkenni með ListIdentifiers og smelltu á eitt þeirra. "
                "OAI-auðkenni er sjaldnast sama og slóðin.",
        "maelt": "Ísmús: is.sagnagrunnur.SG_1247 — ekki slóðin á ismus.is.",
        "spec": SPEC + "#GetRecord",
    },
    "noRecordsMatch": {
        "heiti": "Engar færslur pössuðu",
        "hvad": "Samsetning from/until/set skilaði engu. Þetta er EKKI villa í "
                "þjóninum — hann er að segja að mengið sé tómt.",
        "gera": "Athugaðu hvort settið sé raunverulega notað. Sett geta verið "
                "auglýst í ListSets en verið tóm.",
        "maelt": "Jarðir auglýsti era:19c; ListRecords á því skilaði noRecordsMatch.",
        "spec": SPEC + "#SelectiveHarvestingandDatestamps",
    },
    "noSetHierarchy": {
        "heiti": "Engin sett",
        "hvad": "Þjónninn styður ekki sett. Það er leyfilegt — sett eru valkvæm "
                "í staðlinum.",
        "gera": "Ekkert. Sæktu allt og síaðu sjálfur ef þarf.",
        "maelt": "Ísmús skilar þessu; öll 22.729 færslurnar eru í einu mengi.",
        "spec": SPEC + "#Set",
    },
    "badResumptionToken": {
        "heiti": "Token er ógilt eða útrunnið",
        "hvad": "Token-ið er ekki þekkt hjá þjóninum, eða það er runnið út.",
        "gera": "Byrjaðu gönguna upp á nýtt. Token eru oftast skammlíf og bundin "
                "einni lotu — þau má ekki geyma milli daga.",
        "maelt": None,
        "spec": SPEC + "#FlowControl",
    },
}

# ---------------------------------------------------------------- HTTP-stöður
HTTP_STODUR = {
    301: {
        "heiti": "Varanleg tilvísun",
        "hvad": "Slóðin hefur flust. Fyrirspurnarstrengurinn helst venjulega, "
                "en meginmál POST-beiðni gerir það EKKI.",
        "gera": "Kveiktu á „Fylgja tilvísunum“ til að sjá hvað er á hinum endanum. "
                "Til lengri tíma: notaðu slóðina sem Identify auglýsir í baseURL.",
        "maelt": "SMB /oai -> 301 með TÓMU meginmáli. Alma las það sem "
                 "„Premature end of file“. Með skástriki virkar það.",
        "spec": SPEC + "#HTTPRequestFormat",
    },
    302: {
        "heiti": "Tímabundin tilvísun",
        "hvad": "Sama og 301 en þjónninn segir hana tímabundna.",
        "gera": "Ef slóðin lendir á forsíðu frekar en færslu er hlekkurinn dauður "
                "þótt HTTP-staðan sé 200 eftir að fylgt er.",
        "maelt": "Ævir: bindi 34–66 skila 302 á forsíðu skjalamynda. 1.406 menn "
                 "báru tengil sem lenti hvergi.",
        "spec": None,
    },
    404: {
        "heiti": "Ekki til",
        "hvad": "Slóðin er röng, eða endapunkturinn er ekki þar sem þú heldur.",
        "gera": "Prófaðu grunnslóðina eina með ?verb=Identify.",
        "maelt": None, "spec": None,
    },
    500: {
        "heiti": "Villa í þjóninum",
        "hvad": "Eitthvað sprakk þeirra megin. Meginmálið er þá oft HTML eða "
                "villuslóð, ekki OAI-XML.",
        "gera": "Lestu meginmálið — það nefnir oft skrána sem olli. Það er "
                "nákvæmlega það sem þarf í villutilkynningu til eigandans.",
        "maelt": "Ísmús skilar PHP fatal error á síðu 2 af ListRecords.",
        "spec": None,
    },
    503: {
        "heiti": "Þjónninn biður um bið",
        "hvad": "Oftast álagsstýring. Svarið ber þá Retry-After-haus.",
        "gera": "Bíddu þann tíma sem hausinn segir. Ekki endurtaka strax.",
        "maelt": None,
        "spec": SPEC + "#FlowControl",
    },
}

# ---------------------------------------------------------------- bilunarmynstur
# Mynstur sem eru EKKI OAI-villur en koma fyrir í alvöru. Hvert ber prófun
# á meginmálinu; `finna_mynstur` skilar þeim sem hitta.
MYNSTUR = [
    {
        "kodi": "php_fatal",
        "heiti": "PHP-villa í stað XML",
        "prof": lambda t, s: bool(re.search(r"<b>(Fatal error|Warning)</b>|Uncaught \w*Error", t)),
        "hvad": "Þjónninn hrundi meðan hann byggði svarið. Þetta er HTML, ekki OAI.",
        "gera": "Lestu skráarheitið í villunni — það nefnir færsluna sem olli. "
                "Farðu framhjá með ListIdentifiers + GetRecord á hverja færslu.",
        "maelt": "Ísmús: 71 færsla af 22.729 ber ólokað CDATA og fellir ListRecords.",
        "spec": None,
    },
    {
        "kodi": "cdata",
        "heiti": "Ólokað CDATA",
        "prof": lambda t, s: "CData section not finished" in t or "]]&gt;" in t,
        "hvad": "Textinn inni í <![CDATA[ … ]]> inniheldur sjálfur strenginn ]]> "
                "og hlutinn lokast of snemma. Skráin verður ógilt XML.",
        "gera": "Eigandinn þarf að umrita ]]> í textanum. Þangað til: sæktu "
                "færslurnar hverja fyrir sig og slepptu þeim brotnu.",
        "maelt": "Ísmús, 71 skrá, villan alltaf á línu 8 (content-línunni).",
        "spec": None,
    },
    {
        "kodi": "tomt_301",
        "heiti": "Tilvísun með tómu meginmáli",
        "prof": lambda t, s: s in (301, 302) and len(t.strip()) == 0,
        "hvad": "Þjónninn vísar áfram og skilar engu. Biðlari sem fylgir ekki "
                "tilvísun fær ekkert og les það sem skemmda skrá.",
        "gera": "Bættu skástriki aftan á slóðina. Það leysir þetta í öllum "
                "tilvikum sem við höfum mælt.",
        "maelt": "SMB /oai og Ísmús /oai_pmh. Alma sagði „Premature end of file“.",
        "spec": None,
    },
    {
        "kodi": "html",
        "heiti": "HTML, ekki XML",
        "prof": lambda t, s: bool(re.match(r"\s*<!doctype html|\s*<html", t, re.I)),
        "hvad": "Þú lentir á vefsíðu, ekki endapunkti.",
        "gera": "Athugaðu slóðina. Sumir hýsa vefinn og OAI á sömu rót og "
                "greina á skástriki eða undirslóð.",
        "maelt": "Ísmús /oai_pmh án skástriks skilar SPA-síðunni.",
        "spec": None,
    },
    {
        "kodi": "from_hunsad",
        "heiti": "from/until virðist hunsað",
        "prof": lambda t, s: False,   # metið í skoda_svar, ekki á texta einum
        "hvad": "Þjónninn tekur við from/until en síar ekki. completeListSize "
                "skilar þá heildartölu safnsins þótt beðið sé um eina sekúndu.",
        "gera": "Berðu completeListSize saman við tölu án síu. Séu þær eins er "
                "sían gagnslaus og hver uppfærsla verður full uppskera.",
        "maelt": "Ísmús: beiðni um eina sekúndu skilaði completeListSize=22729.",
        "spec": SPEC + "#SelectiveHarvestingandDatestamps",
    },
]

# ---------------------------------------------------------------- Identify
# Staðallinn, verb Identify: þessi element ERU skylda í svarinu.
IDENTIFY_SKYLDA = [
    ("repositoryName",    "Nafn safnsins eins og það á að birtast."),
    ("baseURL",           "Slóðin sem safnið auglýsir. Verður að vera sú sem virkar."),
    ("protocolVersion",   "Á að vera 2.0."),
    ("adminEmail",        "Netfang umsjónarmanns. Eitt eða fleiri. Án þess er "
                          "enginn til að skrifa þegar eitthvað bilar."),
    ("earliestDatestamp", "Elsti dagstimpill í safninu."),
    ("deletedRecord",     "no | persistent | transient — hvernig eyddar færslur eru meðhöndlaðar."),
    ("granularity",       "Nákvæmni dagstimpla: dagar eða sekúndur."),
]

OAI_NS = "{http://www.openarchives.org/OAI/2.0/}"


def oai_villa(kodi):
    return OAI_VILLUR.get(kodi)


def http_stada(stada):
    try:
        return HTTP_STODUR.get(int(stada))
    except (TypeError, ValueError):
        return None


def finna_mynstur(texti, stada=None):
    """Skilar þeim mynstrum sem hitta á þessu svari."""
    t = texti or ""
    try:
        s = int(stada) if stada is not None else 0
    except (TypeError, ValueError):
        s = 0
    ut = []
    for m in MYNSTUR:
        try:
            if m["prof"](t, s):
                ut.append({k: v for k, v in m.items() if k != "prof"})
        except Exception:
            pass
    return ut


def skoda_identify(xml_texti):
    """Mælir Identify-svar upp að staðlinum. Skilar lista af athugasemdum."""
    ut = []
    try:
        rot = ET.fromstring(xml_texti)
    except ET.ParseError:
        return [{"svid": "—", "stada": "villa", "texti": "Svarið er ekki gilt XML."}]
    ident = rot.find(".//" + OAI_NS + "Identify")
    if ident is None:
        return []
    for nafn, skyring in IDENTIFY_SKYLDA:
        gildi = [e.text.strip() for e in ident.findall(OAI_NS + nafn)
                 if e.text and e.text.strip()]
        if not gildi:
            ut.append({"svid": nafn, "stada": "vantar", "texti": skyring,
                       "spec": SPEC + "#Identify"})
        else:
            ut.append({"svid": nafn, "stada": "í lagi", "texti": " · ".join(gildi)})
    # baseURL á að vera sú slóð sem raunverulega virkar
    b = ident.findtext(OAI_NS + "baseURL", "", )
    if b and not b.endswith("/") and re.search(r"/oai(_pmh)?$", b):
        ut.append({"svid": "baseURL", "stada": "aðvörun",
                   "texti": "Auglýsta slóðin endar á /oai án skástriks. Mælt hefur "
                            "verið að hún skili þá 301 með tómu meginmáli og POST "
                            "tapi viðfangi sínu.",
                   "spec": SPEC + "#HTTPRequestFormat"})
    return ut


def allt():
    """Allt sem JSON-tækt dict, fyrir /skyringar-endapunktinn."""
    return {
        "spec": SPEC,
        "oai_villur": OAI_VILLUR,
        "http_stodur": {str(k): v for k, v in HTTP_STODUR.items()},
        "mynstur": [{k: v for k, v in m.items() if k != "prof"} for m in MYNSTUR],
        "identify_skylda": [{"svid": n, "skyring": s} for n, s in IDENTIFY_SKYLDA],
    }


if __name__ == "__main__":
    import json, sys, urllib.request
    print("OAI-villukóðar :", len(OAI_VILLUR))
    print("HTTP-stöður    :", len(HTTP_STODUR))
    print("bilunarmynstur :", len(MYNSTUR))
    print("Identify-skylda:", len(IDENTIFY_SKYLDA))
    print()
    if len(sys.argv) > 1:
        u = sys.argv[1].rstrip("/") + "/?verb=Identify"
        with urllib.request.urlopen(u, timeout=30) as r:
            t = r.read().decode("utf-8", "replace")
        print("Identify á", u)
        for a in skoda_identify(t):
            merki = {"í lagi": "  ok ", "vantar": "  🔴 ", "aðvörun": "  ⚠️ "}.get(a["stada"], "   ? ")
            print("%s%-18s %s" % (merki, a["svid"], a["texti"][:90]))
    else:
        print("notkun: python3 skyringar.py https://smb.mshl.is/oai/")

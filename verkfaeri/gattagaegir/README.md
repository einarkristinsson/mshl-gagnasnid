# Gáttagægir

**Vefverkfæri sem prófar OAI-PMH endapunkt gagnaveitu gegn gátlista MSHL
fyrir afhendingu í samleit.**

Límdu inn slóð endapunktsins (`baseURL`), smelltu á **Prófa**, og
fáðu stóðst/villu-skýrslu sem speglar [`../../oai-pmh/GATLISTI.md`](../../oai-pmh/GATLISTI.md)
og [`../../snidmat/GULLNA-SNIDID.md`](../../snidmat/GULLNA-SNIDID.md) — reitur
fyrir reit, með gildrunum úr [`../../oai-pmh/LEIDBEININGAR.md`](../../oai-pmh/LEIDBEININGAR.md).

*Gátt* = endapunkturinn (eins og í *leitargátt*); *gægir* gægist inn um hana.
Verkfærið **gægist** — það sækir lítið sýni, aldrei allt safnið.

Hreint `python3` úr stýrikerfinu — engin ytri söfn, ekkert `pip install`.

## Keyrsla

```bash
# vefþjónn á http://127.0.0.1:8765
python3 -m verkfaeri.gattagaegir

# vefþjónn + staðbundinn hermir (til að prófa án nets)
python3 -m verkfaeri.gattagaegir --med-hermi
#   heill:   http://127.0.0.1:8766/god/oai
#   brotinn: http://127.0.0.1:8766/brotin/oai

# í skel, prentar afritanlega Markdown-samantekt (0 = engar villur)
python3 -m verkfaeri.gattagaegir profa https://safn.is/oai
python3 -m verkfaeri.gattagaegir profa https://safn.is/oai --json
```

Valkostir: `--port`, `--host`, `--opinn`, `--netfang <þitt@netfang>` (fer í
User-Agent), `--sidur`, `--syni`, `--sett`, `--bid`, `--engin-slodaprof`.

## Í skýinu

Sama tól, aðgengilegt gagnaveitum án Python á eigin vél. Keyrt á Cloud Run
(Google Cloud) í `europe-west4`, innan EES. Tólið geymir engin gögn — það
sækir lítið sýni af endapunkti gestsins og skilar skýrslu.

```bash
docker build -t gattagaegir .          # Dockerfile er í rót safnsins
docker run --rm -p 8080:8080 gattagaegir
./verkfaeri/gattagaegir/deploy.sh      # í loftið — sjá skrána um forsendur
```

**Opin útgáfa er með vörn** (`--opinn`, eða `GATTAGAEGIR_OPINN=1` í umhverfi,
sem Dockerfile setur): slóðir sem vísa inn á innra net, á `127.0.0.1` eða á
lýsigagnaþjónustu skýsins (`169.254.169.254`) eru stöðvaðar **áður** en beiðnin
fer út — líka þegar 301 vísar þangað. Aðeins http/https á gáttum 80, 443,
8080 og 8000. Skýringin birtist í skýrslunni sem „Náðist ekki í þjóninn: …".
Hermis-flýtihnapparnir hverfa í opinni útgáfu, því hermirinn er á eigin vél.
Sjá `vorn.py` og `profanir/test_vorn.py`.

Í skýinu er `PORT` lesið úr umhverfinu og þjónninn bindur `0.0.0.0`; rök í skel
vinna yfir umhverfið (`__main__.lesa_rok`).

## Hvað er prófað

Athuganirnar eru í fjórum hópum, eins og gátlistinn:

| Hópur | Dæmi um athuganir |
|---|---|
| **Endapunktur** | Identify svarar · baseURL virkar orðrétt · GET **og** POST · adminEmail · `oai_dc` auglýst · `resumptionToken` og talan stemmir · `from`/`until` sía · sett ekki tóm og leka ekki · villur koma sem OAI-kóðar · ein skemmd færsla fellir ekki heildina |
| **Færslur** | `dc:title` · slóð sem svarar 200 · `dc:type` par (@is/@en) · `dc:subject` · staðarreitur · smámyndaslóð (bein, opin, aðgreinanleg) · `dc:rights` · `dc:language` · engir eigin reitir í `oai_dc` |
| **Hreinleiki** | gilt XML · UTF-8 án BOM · engin stýritákn · jafnvægi í CDATA · engin `None`/tóm gildi · engin færsla með tómu `oai_dc:dc` · hreinn texti (ekkert HTML) |
| **Gildin** | dagsetningar á EDTF · `POINT(lengd breidd)` innan Íslands · engin forskeyti í gildum · staðanöfn í nefnifalli, eða beygð mynd með hnitum/auðkenni · varanleg auðkenni efnisorða · hlutverk fylgi fólki |

Alvarleiki: **villa** (skylda/staðfest gildra), **aðvörun** (ráðlagt),
**ábending** (valkvæmt eða vélræn ágiskun).

## Kurteisi við þjóninn

Eins og [`../saekja-oai.py`](../saekja-oai.py): auðkennandi User-Agent, ein
beiðni í einu, vaxandi bið við endurtekningu (1,5 / 3 / 4,5 s), og aðeins
lítið sýni (sjálfgefið 3 síður af `ListRecords` + 10 `GetRecord`, ~45 beiðnir).
POST-beiðnir eru **ekki** eltar í 3xx — það er einmitt hvernig gildran „POST
tapar meginmáli í 301" sést.

## Uppbygging

| Skrá | Hlutverk |
|---|---|
| `thjonn.py` | stdlib vefþjónn: static síða + NDJSON API (`/api/profa`) |
| `vorn.py` | vörn opnu útgáfunnar: hafnar slóðum inn á innra net |
| `deploy.sh` | Cloud Run — sjá „Í skýinu" |
| `vefur/` | ein síða: `index.html`, `still.css`, `gaegir.js` |
| `velin.py` | raðar athugunum, sækir sýnið, streymir niðurstöðum |
| `saekja.py` | kurteis OAI-biðill (GET/POST, bið, engar sjálfvirkar beiningar) |
| `xml_lestur.py` | þolið XML-lesning; bjargar heilum færslum úr brotinni síðu |
| `athuganir/` | athuganirnar sjálfar (endapunktur / færslur / hreinlæti / gildi) |
| `skyrsla.py` | afritanleg Markdown-samantekt |
| `herma/` | staðbundinn OAI-hermir: heill og brotinn endapunktur |
| `profanir/` | einingaprófanir (`unittest`) |

## Prófanir

```bash
python3 -m unittest discover -s verkfaeri/gattagaegir/profanir -t .
```

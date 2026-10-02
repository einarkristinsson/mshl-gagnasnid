# Tímarit.is — innlestur í gegnir-psb

2.011 titlar blaða og tímarita í Sagnatrogið. Sama leið og RÚV: skrá upp í
Alma, ekki OAI-uppskera. Allir smellir eru Einars.

## 0 · Áður en smellt er

- **FRBR:** ný bælingarregla, `Discovery → Other → Suppress Dedup/FRBR`,
  skilyrði `External Data Source Equals` = `MSHL_TIMARIT_FILE`. Gegnir á
  MARC-færslur um mörg sömu blöð (Morgunblaðið, Þjóðólfur …); án reglunnar
  gæti Primo steypt þeim saman við titlana hér.

## 1 · Regla

`Discovery → Normalization Rules` → nýtt → `TIMARIT_XML_Processes`, tegund XML →
líma [`TIMARIT_XML_Processes.drl`](TIMARIT_XML_Processes.drl) (14 reglur,
aðlagaðar úr RÚV-reglunum).

## 2 · Prófíll

| Reitur | Gildi |
|---|---|
| Profile name | `MSHL_TIMARIT_FILE` |
| **Data Source Code** | **`TIMARIT`** ⚠️ ASCII, óbreytanlegt eftir stofnun (Æ-lexían, E11) |
| Data Source Label | Tímarit.is |
| **Status** | **Active** ⚠️ á Inactive klárast keyrslan á sekúndum með 0 færslur |
| Originating system | Other |
| Import Protocol | Upload File/s |
| Physical source format | XML · Generic XML · target Dublin Core |
| Splitter | root `ListRecords` · record `record` · id `record/header/identifier/text()` |
| Normalization | `TIMARIT_XML_Processes` |
| Delivery — Template | `$$LinkingParameter1` (tvö `$`) |
| Delivery — Link Label | Tímarit.is |
| Linking Parameter 1 — Source Tag | `dc:identifier` |
| Linking Parameter 1 — Use source tag | **Matching string using a regular expression** |
| Linking Parameter 1 — regex | `https://timarit\.is/publication/.*` |
| Linking Parameter 1 — normalization | No normalization |
| Link to Thumbnail | ekkert — straumurinn ber enga mynd |

Slóðin er fyrsti `dc:identifier`, svo `Always` myndi líka hitta hana. Regex er
samt öruggari ef mynd bætist við síðar.

## 3 · Innlestur

`Run` → [`TIMARIT-tryA.xml`](TIMARIT-tryA.xml) (2,4 MB) → Monitor Jobs:
**2.011** færslur.

🔴 **Fyrsta keyrsla er `Run` á virkum prófíl.** Engin gögn vistast fyrr en
prófíllinn hefur keyrt einu sinni meðan hann er Active; `Reload` á undan því
les ekkert inn (mælt 2.10 með Listasafni).

## 4 · Mæla

| Leit | Vænt |
|---|---|
| `lds05=TIMARIT` | 2.011 |
| „Þjóðólfur“ | minnst 4 titlar; sá elsti 1848–1920, með 8 útgefendum |
| „Ísafold“ | 1874–1929, útgefandi Björn Jónsson |
| „Fuglaframi“ | færeyskt blað, 1898–1902, tungumál færeyska |
| Tegundarsía | titlarnir undir `journals` |
| Tengillinn „Tímarit.is“ | opnar fyrstu síðu titilsins á timarit.is |

## 5 · Samleit

Leitarumfangið (custom scope) **`MSHL_TIMARIT`**, heiti „Tímarit.is“, skilyrði
`Data Source` · `Contains Keywords` · `TIMARIT`, sett í search profile
`MSHL_ALLT` → **Save**. Svo `Configure Views → MSHL_SAGNATROG_LIGHT_UNION` →
**Publish view**. Nýr Data Source fer ekki sjálfkrafa í neitt umfang (mælt 10.9).

## Óstaðfest

- `resourceType = journals` fyrir `Text`. `audio` og `video` eru staðfest. Hvort
  merkið og sían birtast á íslensku þarf að skoða eins og hjá RÚV.
- Hvernig Primo sýnir og raðar opnu bili, `1949/..` (165 titlar).
- `dc.date` sem markreitur (`dc.rights` er notaður í Handrit.is-reglunum).

## Smíða aftur

```bash
python3 gagnaveitur/timarit/byggja_timarit_dc.py      # sækir Tímarit.is og skrifar báðar skrárnar
python3 -m unittest discover -s gagnaveitur/timarit   # prófanir umbreytingarinnar
```

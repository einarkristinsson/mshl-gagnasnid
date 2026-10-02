# Bækur.is — innlestur í gegnir-psb

2.984 stafrænar bækur Landsbókasafns í Sagnatrogið. Sama leið og RÚV og
Tímarit.is: skrá upp í Alma, ekki OAI-uppskera. Allir smellir eru Einars.

## 0 · Áður en smellt er

- **FRBR:** ný bælingarregla, `Discovery → Other → Suppress Dedup/FRBR`,
  skilyrði `External Data Source Equals` = `MSHL_BAEKUR_FILE`. Bækurnar eru
  líka til sem MARC-færslur í Gegni (MMS-auðkennið er í tenglinum á
  Bókaskrá); án reglunnar gæti Primo steypt þeim saman.

## 1 · Regla

`Discovery → Normalization Rules` → nýtt → `BAEKUR_XML_Processes`, tegund XML →
líma [`BAEKUR_XML_Processes.drl`](BAEKUR_XML_Processes.drl) (19 reglur,
aðlagaðar úr reglum Tímarit.is og RÚV).

## 2 · Prófíll

| Reitur | Gildi |
|---|---|
| Profile name | `MSHL_BAEKUR_FILE` |
| **Data Source Code** | **`BAEKUR`** ⚠️ ASCII, óbreytanlegt eftir stofnun (Æ-lexían, E11) |
| Data Source Label | Bækur.is |
| **Status** | **Active** ⚠️ á Inactive klárast keyrslan á sekúndum með 0 færslur |
| Originating system | Other |
| Import Protocol | Upload File/s |
| Physical source format | XML · Generic XML · target Dublin Core |
| Splitter | root `ListRecords` · record `record` · id `record/header/identifier/text()` |
| Normalization | `BAEKUR_XML_Processes` |
| Delivery — Template | `$$LinkingParameter1` (tvö `$`) |
| Delivery — Link Label | Bækur.is |
| Linking Parameter 1 — Source Tag | `dc:identifier` |
| Linking Parameter 1 — Use source tag | **Matching string using a regular expression** |
| Linking Parameter 1 — regex | `https://baekur\.is/bok/.*` |
| Linking Parameter 1 — normalization | No normalization |
| Link to Thumbnail | `$$LinkingParameter2` (tvö `$`) |
| Linking Parameter 2 — Source Tag | `dc:identifier` |
| Linking Parameter 2 — Use source tag | **Matching string using a regular expression** |
| Linking Parameter 2 — regex | `https://baekur\.is/cover/tbn/.*` |
| Linking Parameter 2 — normalization | No normalization |

🔴 **Use source tag = Always** tekur fyrsta `dc:identifier`. Það er bókarslóðin,
svo tengillinn virkaði, en smámyndin yrði þá bókarslóðin líka. Regex á báðum.

## 3 · Innlestur

`Run` → [`BAEKUR-tryA.xml`](BAEKUR-tryA.xml) (6,2 MB) → Monitor Jobs:
**2.984** færslur.

🔴 **Fyrsta keyrsla er `Run` á virkum prófíl.** Engin gögn vistast fyrr en
prófíllinn hefur keyrt einu sinni meðan hann er Active; `Reload` á undan því
les ekkert inn (mælt 2.10 með Listasafni).

## 4 · Mæla

| Leit | Vænt |
|---|---|
| `lds05=BAEKUR` | 2.984 |
| „Hallgrímur Pétursson“ | 73 bækur með „Hallgrímur Pétursson (1614-1674)“, allar með smámynd; ein að auki eftir nafna hans (1875-1937) |
| „Antiquarisk-historiske bemærkninger“ | dönsk bók frá 1818 eftir Finn Magnússon (1781-1847), útgáfuland Danmörk |
| „Carmen finitis exercitiis militaribus“ | latnesk bók frá 1830 eftir Lárus Sigurðsson (1808-1832), útgáfuland Danmörk |
| Tegundarsía | bækurnar undir `books` |
| Staðarsía | Ísland 1.376 · Danmörk 987 |
| Tengillinn „Bækur.is“ | opnar bókina á baekur.is |
| Smámynd | fyrsta blaðsíða bókarinnar á spjaldinu |

## 5 · Samleit

Leitarumfangið (custom scope) **`MSHL_BAEKUR`**, heiti „Bækur.is“, skilyrði
`Data Source` · `Contains Keywords` · `BAEKUR`, sett í search profile
`MSHL_ALLT` → **Save**. Svo `Configure Views → MSHL_SAGNATROG_LIGHT_UNION` →
**Publish view**. Án Publish birtist ekkert (lært 29.9). Nýr Data Source fer
ekki sjálfkrafa í neitt umfang (mælt 10.9).

## Óstaðfest

- Hvort Primo eltir 302 á smámyndinni (`/cover/tbn/<uuid>` → `/skra/JPG/<n>`).
  Vafri gerir það. Ef myndin birtist ekki: sjá „Slóðirnar“ í
  [README](README.md).
- `dc.coverage` og `local22` úr `dcterms:spatial` (RÚV fyllir þau úr `dc:coverage`).
- Hvort `dcterms.haspart` (samræmdir titlar, t.d. „Njáls saga“) er leitanlegt.
- „Ísland“ verður efst í fólkssíunni (`local49`, 198 bækur) — skoða hvort það
  truflar.

## Smíða aftur

```bash
/usr/bin/python3 gagnaveitur/baekur/byggja_baekur_dc.py      # sækir Bækur.is og skrifar báðar skrárnar
/usr/bin/python3 -m unittest discover -s gagnaveitur/baekur  # prófanir umbreytingarinnar
```

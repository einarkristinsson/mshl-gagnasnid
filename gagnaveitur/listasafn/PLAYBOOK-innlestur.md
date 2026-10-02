# Listasafn Íslands — innlestur í gegnir-psb

124 sýningar og fjórar listamannasíður í Sagnatrogið. Sama leið og RÚV og
Tímarit.is: skrá upp í Alma, ekki OAI-uppskera. Allir smellir eru Einars.

## 0 · Áður en smellt er

- **FRBR:** ný bælingarregla, `Discovery → Other → Suppress Dedup/FRBR`,
  skilyrði `External Data Source Equals` = `MSHL_LISTASAFN_FILE`. Sýningar og
  listamenn bera algeng heiti („Yfirlitssýning“, „Jón Stefánsson“) sem Primo
  gæti annars steypt saman við færslur annarra gagnaveitna.
- **Leyfi:** Sigurður Gunnarsson (Listasafni) bað um tenginguna 16.9 og sendi
  slóðirnar 28.9. Vefþjónusta Prismic er opin og við lesum beint úr henni
  (ákveðið 2.10).

## 0b · Hreinsun eftir fyrstu tilraun (2.10.2026)

Fyrsti prófíllinn fékk kóðann `LS_RVK` og lýsinguna „Listasafn Reykjavíkur“,
og færslurnar 128 fóru í gegnum RÚV-reglurnar (`lds05 = RUV`, tegund `other`).
Kóðanum verður ekki breytt, svo færslunum er eytt og nýr prófíll stofnaður.

1. `Admin → Manage Jobs and Sets → Run a Job` → tegund **Discovery Management** →
   **Delete External Data Sources** → velja prófílinn sem las inn (`LS_RVK`) →
   Submit. Heimild: [Deleting External Data Sources for Primo VE](https://knowledge.exlibrisgroup.com/Primo/Product_Documentation/020Primo_VE/Primo_VE_(English)/Loading_Records_from_External_Sources_into_Primo_VE/Deleting_External_Data_Sources_for_Primo_VE).
2. Mæla: leit að „Ummyndlingar“ gefur 0.
3. Gamli prófíllinn: Inactive, og heitið losað (endurnefna eða eyða) svo sá nýi
   geti heitið `MSHL_LISTASAFN_FILE`. Óstaðfest hvort Alma leyfir að eyða prófíl.
4. Leitarumfangið sem vísar á `LS_RVK`: breyta skilyrðinu í `LISTASAFN` (5. liður).

## 1 · Regla

`Discovery → Normalization Rules` → nýtt → `LISTASAFN_XML_Processes`, tegund XML →
líma [`LISTASAFN_XML_Processes.drl`](LISTASAFN_XML_Processes.drl) (19 reglur,
úr Tímarit-reglunum + fólk og hlutverk úr RÚV-reglunum).

## 2 · Prófíll

| Reitur | Gildi |
|---|---|
| Profile name | `MSHL_LISTASAFN_FILE` |
| **Data Source Code** | **`LISTASAFN`** ⚠️ ASCII, óbreytanlegt eftir stofnun |
| Data Source Label | Listasafn Íslands |
| **Status** | **Active** ⚠️ á Inactive klárast keyrslan á sekúndum með 0 færslur |
| Originating system | Other |
| Import Protocol | Upload File/s |
| Physical source format | XML · Generic XML · target Dublin Core |
| Splitter | root `ListRecords` · record `record` · id `record/header/identifier/text()` |
| Normalization | `LISTASAFN_XML_Processes` |
| Delivery — Template | `$$LinkingParameter1` (tvö `$`) |
| Delivery — Link Label | Listasafn Íslands |
| Linking Parameter 1 — Source Tag | `dc:identifier` |
| Linking Parameter 1 — Use source tag | **Matching string using a regular expression** |
| Linking Parameter 1 — regex | `https://www\.listasafn\.is/list/.*` |
| Linking Parameter 1 — normalization | No normalization |
| Link to Thumbnail | `$$LinkingParameter2` (tvö `$`) |
| Linking Parameter 2 — Source Tag | `dc:identifier` |
| Linking Parameter 2 — Use source tag | **Matching string using a regular expression** |
| Linking Parameter 2 — regex | `https://images\.prismic\.io/listasafn-islands/.*` |
| Linking Parameter 2 — normalization | No normalization |

## 3 · Innlestur

`Run` → [`LISTASAFN-tryA.xml`](LISTASAFN-tryA.xml) → Monitor Jobs: **128** færslur.

🔴 **Fyrsta keyrsla er `Run` á virkum prófíl.** Engin gögn vistast fyrr en
prófíllinn hefur keyrt einu sinni meðan hann er Active; `Reload` á undan því
les ekkert inn (mælt 2.10 með Listasafni).

## 4 · Mæla

| Leit | Vænt |
|---|---|
| `lds05=LISTASAFN` | 128 |
| „Ásgrímur Jónsson“ | listamannasíða + sýningar hans, með „listamaður“ í hlutverkasíu |
| „Ummyndlingar“ | sýning James Merry, með smámynd |
| „Þjóðsögur í íslenskri myndlist“ | samleit við þjóðsögur í Ísmús |

## 5 · Leitarumfang

Nýtt leitarumfang (custom scope) **`MSHL_LISTASAFN`**, skilyrði `Data Source` ·
`Contains Keywords` · `LISTASAFN` → bæta í `Search Profiles → MSHL_ALLT` → Save →
`Configure Views → MSHL_SAGNATROG_LIGHT_UNION` → **Publish view**. Án Publish
sést ekkert (mælt 29.9 með RÚV).

## 6 · Þýðingar (ef merkið sýnir hráan kóða)

Sýningar fá sérkóðann `exhibitions`. Í `Facet Resource Type Labels`:
`facets.facet.facet_rtype.exhibitions` → **Sýningar**, og í `Icon Codes Labels`:
`mediatype.exhibitions` → **Sýning**. Listamenn fá `people`, sem er þegar þýtt (Fólk).

## Óstaðfest

- `resourceType = exhibitions` og `dcterms.alternative` sem markreitur.
- Hvort Primo sækir smámyndir af `images.prismic.io` (svarar venjulegum vöfrum, mælt 1.10).

## Smíða aftur

```
/usr/bin/python3 byggja_listasafn_dc.py                       # sækir úr Prismic og smíðar
/usr/bin/python3 byggja_listasafn_dc.py --vista hratt.json    # sama, og vistar hrá gögn
/usr/bin/python3 byggja_listasafn_dc.py hratt.json            # smíðar úr vistuðu
```

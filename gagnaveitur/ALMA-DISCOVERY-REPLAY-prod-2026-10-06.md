# Alma Discovery — replay-listi fyrir PROD (gegnir)

Allt hér var gert **hands-on í gegnir-psb (sandbox)** 6.10.2026 gegnum Claude in Chrome,
Configuring: Gegnir (NZ 354ILC_NETWORK). **Endurtaka á prod (gegnir) í sömu röð.**
Enginn af þessum breytingum var gerð á prod. Allir smellir Einars (eða vafralotu með leyfi).

Staðfesting í sandbox: Primo-API `scope=MSHL_BAEKUR` skilaði 2.531/2.984 (vísun í gangi) kl. ~17:00.

---

## A · LISTASAFN — leiðrétting (var þegar byggt, bara röng tenging)

Rót: ferlið `LS_RVK_XML_Processes` vísaði í reglu sem var ekki til.

1. **Configuration → Discovery → Normalization Process Task → `LS_RVK_XML_Processes` → Task Parameters**
   - Drools File Key: `SMB_Listasafn_RVK_xml (not listed)` → **`MSHL_Listasafn_xml`** → Save.
2. **Discovery Import Profiles → MSHL_LISTASAFN_FILE → Run** → hlaða `LISTASAFN-tryA.xml` (129) → Submit.
   - Niðurstaða sandbox: 129/129, 0 féllu.

> Á prod: ef prod speglar sandbox er þetta bara Drools-key leiðréttingin + endurkeyrsla.
> Ef Listasafn er ekki til á prod → byggja eins og Bækur.is (kafli B) með LS_RVK/MSHL_Listasafn_xml.

---

## B · BÆKUR.is — byggt frá grunni (regla → ferli → prófíll → innlestur → scope → view)

Skrár: `gagnasnid/gagnaveitur/baekur/` (BAEKUR_XML_Processes.drl, BAEKUR-tryA.xml).

### B1 · Normalization-regla
- **Discovery → Normalization rules for External Data sources (ME) → Rules → New → Normalization (Discovery)**
  - Name `BAEKUR_XML_Processes`, Description `Bækur.is`, **Type XML** → Save.
  - Líma allt úr `BAEKUR_XML_Processes.drl` (19 reglur) í ritilinn → Save (Alma staðfestir Drools).
  - **Rule Actions → Properties → Access Level = Shared** → Save. ⚠️ Annars sést reglan EKKI í Drools File Key.

### B2 · Normalization Process
- **Normalization Process Task → Add Process**
  - Business Entity `Discovery BIB Records`, Type `Discovery generic XML normalization` → Next.
  - Name `BAEKUR_XML_Processes`, Description `Bækur.is`, Status Active → Next.
  - Add Tasks → haka við `Generic XML- Normalization` → Add and Close → Next.
  - Task Parameters → Drools File Key = **`BAEKUR_XML_Processes`** (reglan) → Save.

### B3 · Import Profile
- **Discovery Import Profiles → Add New Profile → Discovery → Next**
  - Profile name `MSHL_BAEKUR_FILE`, Description `Bækur.is`
  - **Data Source Code `BAEKUR`** (ASCII, óbreytanlegt), Data Source Label `Bækur.is`
  - Originating system `Other`, Import Protocol `Upload File/s`
  - Physical source format `XML`, Source format `Generic XML` → Target format `Dublin Core` (sjálfkrafa)
  - Status **Active**, Share with Network ✓
  - Splitter: Root element tag `ListRecords`, Record elements tag `record`, XPath to identifier `record/header/identifier/text()` → Next
  - Normalization: `BAEKUR_XML_Processes` (ferlið) → Next
  - Delivery:
    - Link to Resource → Template `$$LinkingParameter1`, Link Label `Bækur.is`
    - Link to Thumbnail → Template `$$LinkingParameter2`
    - LinkingParameter1 (Edit): Source Tag `dc:identifier`, Use source tag **Matching string using a regular expression**, Matching String `https://baekur\.is/bok/.*`, Normalization `No normalization`
    - LinkingParameter2 (Edit): Source Tag `dc:identifier`, Matching string regex `https://baekur\.is/cover/tbn/.*`, No normalization
  - Save.

### B4 · Innlestur
- **MSHL_BAEKUR_FILE → Run** → Select File → hlaða `BAEKUR-tryA.xml` (6,2 MB; Alma skiptir í ~60 hluta) → Add → Submit.
  - Niðurstaða sandbox: **2.984 / 2.984, 0 féllu** (58 sek).

### B5 · FRBR-bæling
- **Discovery → Other → Suppress Dedup/FRBR → Add a Suppress Rule**
  - Code `BAEKUR`, Name `Bækur.is`, Suppress **Dedup and FRBR**
  - Condition: **External Data Source · Equals · Bækur.is** → Save.

### B6 · Custom scope
- **Search Profiles → Custom Local Data Scopes → Add a Custom Scope**
  - Code `MSHL_BAEKUR`, Name `Bækur.is`, Description `Bækur.is`, Scope Population `My Institution`
  - Condition: **External data source · Equals · Bækur.is** → Save. (Eins og MSHL_RUV.)

### B7 · Search Profile
- **Search Profiles → Add a Search Profile**
  - Code `MSHL_BAEKUR`, Display Name `Bækur.is`, Description `Bækur.is`
  - Add Scope → Scope Type `Custom (Local data)` → Custom Scope `Bækur.is (MSHL_BAEKUR)` → Add and Close → Save.

### B8 · View slot
- **Configure Views → `MSHL_SAGNATROG_LIGHT_UNION` → Edit → Search Profile Slots → Add a Slot**
  - Code `MSHL_BAEKUR`, Name `Bækur.is`
  - Select Search Profiles for slot → kveikja á `MSHL_BAEKUR` (Active) → Save (slot kemur í listann).

### B9 · (EKKI gert — bíður ákvörðunar Einars)
- **„Switch to Live“** á view-inu = gerir allt NDE-view-ið live + redirect frá klassíska Primo fyrir ALLA notendur.
  Það er view-breið ræsing, ekki „birta Bækur.is". **Reyndist óþarft** — scope MSHL_BAEKUR var þegar leitanlegt (API 2.531). Gera aðeins ef verið er að ræsa allt NDE-Sagnatrog í fyrsta sinn.

### B10 · FRBR-hópun löguð + lönd úr contributor (7.10 kl. 14:43–14:59)
Samleit sýndi 2.531 af 2.984 — FRBR-hópaði útgáfur saman (Graduale 18→1, Guðbrandur Þorláksson 50 bækur).
Rót: **Suppress Dedup/FRBR-reglan BAEKUR var búin til EFTIR 6.10-innlesturinn**, svo gömlu færslurnar fengu
ekki bælinguna. Reglan (lesin, ekki breytt): Configuration → Discovery → **Suppress Dedup/FRBR** → BAEKUR,
skilyrði **External Data Source Equals „Bækur.is"**, bælir **Dedup and FRBR** — rétt uppsett.
Auk þess: lönd sem „höfundar" (Ísland 198, Danmörk 1) tekin úr `dc:contributor` (byggja-skrifta, commit e8abd2e;
13 „Ísland" eftir eru löglegt stofnananöfn „…á Íslandi/Íslands").
**Lagfæring:** Run á `MSHL_BAEKUR_FILE` með `gagnasnid/gagnaveitur/baekur/BAEKUR-tryA.xml` (6,37 MB, bein
upphleðsla, 60 bulks, 2.984). Job 17249812210006886, Completed Successfully 14:43:20→14:51:38 (FRBR-endurmat
tók ~8 mín — mun lengra en venjulegur innlestur), 0 rejected.
**✅ Staðfest 14:59 (mshl-cdha-72):** 2.984 í samleit (var 2.531), frbrtype 6 á öllum (engir FRBR-hópar),
„Ísland" 0 í Fólk-síu (var 140), Guðbrandur Þorláksson 75 bækur, Graduale 18.
**Lærdómur:** Suppress Dedup/FRBR-regla sem er búin til eftir innlestur virkar ekki aftur í tímann → endurkeyra
(Run) svo bælingin taki á fyrirliggjandi færslur; FRBR-endurmat gerir keyrsluna margfalt lengri.

---

## C · ÍSMÚS v2 — endurinnlestur (eyða gömlu 22.656 → lesa 66.476 í sagnatrog-sniði)

Gagnaveitan var þegar til (Data Source Code `MSHL_ISMUS`, prófíll
`MSHL_ISMUS_FILE_TEST`, Label „Íslenskur músík- og menningararfur"). v2 er
endurinnlestur: nýtt `metadataPrefix=sagnatrog` frá ismus.is (Trausti opnaði
6.10), nær þrefalt fleiri hljóðrit, auk nýrra einstaklingsfærslna. 76 gömul
auðkenni eru horfin úr nýja safninu → eyða fyrst svo þau sitji ekki eftir
heimilislaus. Skrár: `leidarljos/dc-template/sources/ismus/ISMUS-v2-*.xml`.

Ítarlegri playbook (ákvarðanir, pörun við SMB, væntingar á spjaldinu):
[`sources/ismus/PLAYBOOK-innlestur.md`](../../leidarljos/dc-template/sources/ismus/PLAYBOOK-innlestur.md) kafli „v2".

**✅ Niðurstöður sandbox 6.10.2026 — allar keyrslur Completed Successfully, 0 föll, 0 rejected:**

| Keyrsla | Skrár | Færslur | Job ID | Bulks |
|---|---|---:|---|---:|
| C0 Delete | — | 22.656 eydd | 17236968840006886 | — |
| C3 TEST-3 | ISMUS-v2-TEST-3 | 3 | 17236970860006886 | 1 |
| C4 Run A | sagnir_01 | 3.231 | 17236972170006886 | 65 |
| C4 Run B | sagnir_02+03+04 | 8.081 | 17237235980006886 | 163 |
| C4 Run C1 | hljóðrit 01–03 | 30.000 | 17237698010006886 | 603 |
| C4 Run C2 | hljóðrit 04_01/02, 05_01/02, 06 | 20.395 | 17240338010006886 | 410 |
| C5 Run D | fólk | 4.769 | 17241994910006886 | 96 |

Einstök heild eftir dedup: **66.476** (TEST-3 og 2 sagnir + 1 hljóðrit lyklast saman). Vísir í Leitum náði 41.312 eftir C1 (dedup staðfest: 11.313 eftir sagnir, ekki 11.315) og heldur áfram upp í 66.476 á ~5 mín töf per keyrslu. **Staðfest 21:11: 66.476, þar af 4.769 rtype=people.**

### C6 · Sögn — sagnir fá eigin tegund resourceType „legend" (ákvörðun Einars 6.10 kl. 22:30)
Reglan `SMB_Ismus_xml`: í „ismus resourceType and local2" varð `replace string by string (TEMP"2","^LegendYY$","legend")` (var „other"); TEMP"1" var þegar „legend". Svo bæði `local2` og `resourceType` = „legend" fyrir sagnir. (.drl commit 43134ec — eina virka línubreytingin.) → Save (23 reglur, Drools staðfest). Svo **Run** sagnir_01..04 aftur (MSHL_ISMUS_FILE_TEST, job 17242384370006886, 228 bulks, 11.312, 0 föll); Run uppfærir eftir auðkenni, heild óbreytt 66.476. Eftir: merki „Sögn" (facet_rtype.legend/.legends + mediatype.legend/.legends) og view-stillingar — smellir Einars (NZ/view; auto-mode hafnar vafralotu).

**Sögn staðfest 6.10 kl. 23:31:** rtype legend = 11.312, other = 0, heild 66.476. Merki „Sögn" komin (Einar, 23:07).

### C7 · Opið eftir 6.10 kvöld (smellir Einars — auto-mode hafnar NZ/view hjá vafralotu)
1. **lds75 „Hlutverk" birtist ekki** — EKKI fulldisplay (lds75 er þegar í Record details, Active). Rót: local75 er tómt í vísinum þótt `dcterms:bibliographicCitation` sé í gögnum. A/B í „Manage display and local fields": local_field_26 (fyllist) hefur „Enable for search" ✓ + „Enable for facet" ✓ + **„Use the parallel Local Field 01/50 from the Dublin Core record" ✓**; local_field_75 hefur öll þrjú ÓHÖKUÐ (MARC21 reitur 598). Lagfæring: haka a.m.k. „Use parallel … Dublin Core record" (+ search) á local_field_75 → endurkeyra. (VERK.md E8, commit d0ecfd2.)
2. **Síur lds22 (Staður) / lds93 (Efni) birtast ekki enn** — Einar hakaði „Enable for facet" kl. 23:16 en sagnir vísuðust 23:14–15, svo reitirnir urðu síur EFTIR vísun (síur krefjast endurvísunar). Próf: TEST-3 keyrt aftur 23:44 (job 17242963410006886) → mshl-cdha-72 mælir hvort síurnar birtist á þeim 3. Virki það → full endurkeyrsla (sömu skrár, Run uppfærir eftir auðkenni) svo allt safnið fái síurnar.

### C8 · lds75 leyst → local11/local12 + full endurkeyrsla (7.10 kl. 10:30–10:52)

**Rót C7#1 dýpkuð:** reitir **yfir 50** (local75, local93) taka EKKI við „Use the parallel Local
Field 01/50 from the Dublin Core record" — Alma hafnar: „…not allowed for local fields over 50".
Þess vegna var local75 (Hlutverk) alltaf tómt þótt `dcterms:bibliographicCitation` væri í gögnum,
og local93 (Efni) sömuleiðis. DC/ytri færslur fylla aðeins reiti ≤ 50 í gegnum parallel-DC.

**Lagfæring (Einar, NZ „Manage display and local fields"):** tveir nýir reitir ≤ 50 —
`local_field_11` **Hlutverk** og `local_field_12` **Efni** — báðir með „Use parallel … Dublin Core
record" ✓ + „Enable for search" ✓ (local_field_12 líka „Enable for facet" ✓). MSHL notar
`local_field_11–20` héðan í frá fyrir ný DC-svæði. (Reitir 75/93 skildir eftir óvirkir.)

**Regla `SMB_Ismus_xml` uppfærð (vafralota):** `bibliographicCitation` → `local11` (var `local75`),
`dc:subject[@xml:lang='is']` → `local12` (var `local93`). 23 reglur, „Rules were successfully saved",
Drools staðfest. (.drl commit 1cfd679.)

**Gögn endurbyggð 10:06** (`byggja_ismus_sagnatrog_dc.py`) — hljóðrit fá nú læsilega titla
(t.d. „Nykurtjörn · SÁM 90/2194 EF"). TEST-3 staðfest af mshl-cdha-72 kl. 10:22: `lds11` (hlutverk),
`lds12` (efnisorð) og nýr hljóðrititill fyllast allir.

**Full endurkeyrsla — nýja reglan + ný gögn, allar Completed Successfully, 0 rejected:**

| Run | Skrá(r) | Færslur | Job ID | Bulks |
|-----|---------|---------|--------|-------|
| A sagnir | sagnir_01–04 | 11.312 | 17242977860006886 | 228 |
| B hljóðrit 01–03 | hljodrit-01_01…03_02 (6 bútar) | 30.000 | 17243562920006886 | 602 |
| C hljóðrit 04–06 | hljodrit-04_01…05_03 (6 bútar) + hljóðrit-06 | 20.395 | 17245102900006886 | 412 |
| D fólk | ISMUS-v2-folk-tryA | 4.769 | 17246149040006886 | 96 |

Einstök heild eftir dedup: **66.476** (Run uppfærir eftir gagnaveitu+ID). mshl-cdha-72 mælir eftir
endurvísun: heild 66.476, legend 11.312, lds11/lds12 fjölda.

⚠️ **Prófíllinn keyrir bara EITT starf í einu:** ef `Run → Submit` er sent meðan annað job vinnst
hafnar Alma með „Job did not run – a dependent job is already in process" (gerðist við Run D meðan
Run C vann). Bíða þar til fyrra job er „Completed Successfully" áður en næsta er sent. (Build-fasann —
að hlaða bútum í nýtt Run — má hins vegar undirbúa meðan annað job vinnst.)

**Opið (smellur Einars, auto-mode hafnar view-config):** bæta `lds12` (Efni) og `lds22` (Staður) sem
local facets — **Configure Views → MSHL_SAGNATROG_LIGHT_UNION → Brief Results → „Add a Local Facet"**.
Síur krefjast þess að reiturinn sé virkur í view-inu, ekki bara „Enable for facet" á reitnum.
Fyrir `lds22`: aðgreina „Location" (lds22) frá innbyggðu `location_code` með því að lesa facet-kóðann.

### C9 · Hlutverk hreinsað + Heimildarmenn (lds13) — full endurkeyrsla (7.10 kl. 13:30–14:15)

Þrjár umbætur á síum, allar í EINNI endurkeyrslu:
1. **Viðfangsefni (lds12)** virk sía — Einar lagaði `local_field_12` (facet ✓ + MARC 090→999) um morguninn.
2. **Heimildarmenn (lds13)** — nýr reitur `local_field_13` (Einar: parallel-DC ✓, search ✓, facet ✓, MARC 999,
   merki „Heimildarmenn") + ný regla „ismus heimildarmenn to local13" (dc:contributor → local13).
3. **Hlutverk (lds11) ber nú BARA hlutverkin** (heimildaraðili/safnari/skrásetjari/sendandi) í stað
   „Nafn (ár) (hlutverk) · …" — leyst í GÖGNUNUM, ekki reglunni: `dcterms:bibliographicCitation`
   xsi:type="mshl:hlutverk" inniheldur nú bara hlutverkaorðið. Reglan `bibliographicCitation → local11` óbreytt.

**Regla** `SMB_ismus_xml` uppfærð í **24 reglur** (commit 840f0fe) — límt gegnum Metadata Editor
(Configuration → Discovery → Normalization rules for External Data sources → Rules → Shared →
SMB_ismus_xml → Cmd+A, Cmd+V úr `pbcopy`, Save; Drools staðfest „Rules were successfully saved").
Reglan var áður 23 reglur (1cfd679, morgun) — vantaði local13.

**Gögn** endurbyggð 13:32 (commit ffaadbf). Forbútað með chunk_ismus.py → **18 bútar** (allir xmllint-gildir,
≤8,80 MB; sagnir 4, hljóðrit-01 2, -02 3, -03 3, -04 3, -05 3) + hljóðrit-06 og fólk beint.

**TEST-3** (job 17246393150006886) staðfest af mshl-cdha-72 13:43: lds11 = bara hlutverk ✓,
lds12 virk sía ✓, lds13 fyllist ✓ („Flóvent Jónsson (1840-1911)"). lds13-sían bíður þess að vera
bætt í Brief Results (view-birting, óháð gögnum/vísun).

**Full endurkeyrsla — allar Completed Successfully, 0 rejected:**

| Run | Efni | Færslur | Job ID | Bulks |
|-----|------|--------:|--------|------:|
| A | sagnir (4 bútar) | 11.312 | 17246395960006886 | 229 |
| B | hljóðrit 01–03 (8 bútar) | 30.000 | 17246981160006886 | 604 |
| C | hljóðrit 04–06 (6 bútar + hljóðrit-06) | 20.395 | 17248521260006886 | 410 |
| D | fólk | 4.769 | 17249567280006886 | 96 |

Heild **66.476**. ⚠️ **Lærdómur staðfestur aftur:** prófíllinn keyrir eitt job í einu — Run D fékk
„dependent job is already in process" meðan Run C vann; beðið eftir „Completed Successfully", svo
fólk endurhlaðið (1 skrá) og sent. Build-fasinn má skarast við vinnslu fyrra jobs.

**✅ Lokastaðfest í Leitum 14:28 (mshl-cdha-72):** MSHL_ISMUS = 66.476. **Hlutverk (lds11) HREIN** —
aðeins heimildaraðili 55.411 · safnari 48.431 · skrásetjari 9.941 · sendandi 884 (passar nákvæmlega
við uppruna). **Viðfangsefni (lds12)** virk sía (Æviatriði 3.529…). **Heimildarmenn (lds13)** virk sía
(Guðmundur Þorsteinsson frá Lundi 486…). Ísmús v2 fullklárað með öllum þremur síuumbótum.

### C0 · Eyða gömlu færslunum (DESTRUCTIVE — Einar smellir)
- **Admin → Manage Jobs and Sets → Run a Job → Discovery Management → Delete External Data Sources**
  - Data Source „Íslenskur músík- og menningararfur" (= kóði `MSHL_ISMUS`) → Run.
  - Niðurstaða sandbox 6.10: **Completed Successfully, 22.656 unnar, 0 exceptions** (job 17236968840006886, ~1 mín). Leitir `MSHL_ISMUS` = 0 kl. 20:12.
  - ⚠️ Auto-mode í vafralotu HAFNAR þessu verki (destructive) — Einar gerir smellinn sjálfur. Sama verk endaði „with errors" á Listasafni 2.10 → **lesa Monitor Jobs skýrsluna**; ef „with errors" → ekki halda áfram.

### C1 · Uppfæra normalization-regluna (v1 19 reglur → v2 23 reglur)
- **Configuration → Discovery → Normalization rules for External Data sources (ME) → Rules →** reglan **`SMB_Ismus_xml`**.
  - ⚠️ Reglan heitir `SMB_Ismus_xml` — EKKI `ISMUS_XML_Processes` (það er skráarnafnið). Ferlið `Ismus_XML_Processes` vísar (Drools File Key) í `SMB_Ismus_xml`. Sama class af villu og Listasafn (kafli A) ef vitlaus regla er uppfærð.
  - Hreinsa ritilinn (Cmd+A, Delete) → líma allt úr `ISMUS_XML_Processes.drl` (23 reglur) → Save (Alma staðfestir Drools). Vinstra spjaldið á að sýna „Normalization (Discovery) (23)".
  - Drools File Key ferlisins er ÓBREYTT (vísar áfram í `SMB_Ismus_xml`) — engin ný regla, engin Shared/Private-breyting þörf.
  - Nýtt í v2: `dc:date` (upptökudagur → `creationdate`), `dc:source` → `local26`, `dcterms:temporal` → `local31`, `dc:relation` (SMB), Person → `people`/`person`.

### C2 · Prófíll Active
- **Discovery Import Profiles → `MSHL_ISMUS_FILE_TEST`** → Status **Active** (var Active 6.10). Data Source Code `MSHL_ISMUS`, Label „Íslenskur músík- og menningararfur".

### C3 · Prófkeyrsla (3 færslur) — hlið áður en stóru skrárnar fara inn
- **`MSHL_ISMUS_FILE_TEST` → Run** → hlaða `ISMUS-v2-TEST-3-tryA.xml` (3) → Add → Submit.
  - Niðurstaða sandbox 6.10: **Completed Successfully, 3 records, 0 problem, 0 files rejected** (job 17236970860006886).
  - Þessar 3 eru hlutmengi aðalgagnanna (SG_1073, SG_1082 í sagnir; ISMUS_1013476 í hljóðrit-01) — með Run uppfærast þær þegar stóru skrárnar fara inn (ytri færslur lyklast á gagnaveitu+ID), svo lokatalan verður 66.476, ekki 66.479.
  - Staðfesta í Leitum að færslurnar 3 líti rétt út (titill, tegund, `lds05=ISMUS`, tengill, dagsetning) ÁÐUR en skref 4–5.

### C4 · Sagnir + hljóðrit
- **`MSHL_ISMUS_FILE_TEST` → Run** → `ISMUS-v2-sagnir-tryA.xml` (11.312), svo hvert `ISMUS-v2-hljodrit-01…06-tryA.xml` (01–05 = 10.000 hvert, 06 = 395). Samtals 50.395 hljóðrit.

### C5 · Fólk (einstaklingar)
- **`MSHL_ISMUS_FILE_TEST` → Run** → `ISMUS-v2-folk-tryA.xml` (4.769).
- Eftir öll skref: `MSHL_ISMUS` = **66.476** í Leitum (sagnir 11.312 + hljóðrit 50.395 + fólk 4.769).

### ⚠️ Upphleðsla stórra skráa — munur vafralotu vs. handvirkt
- **Handvirkt á prod (Einar):** hlaða FULLU skránum beint (`ISMUS-v2-sagnir-tryA.xml` 29,8 MB, `ISMUS-v2-hljodrit-01…05` 15–16,5 MB hvert). Alma skiptir þeim sjálf í ~100 KB bulks. Engin forbútun þörf.
- **Vafralota (Claude in Chrome) 6.10:** `file_upload`-tólið takmarkast við ~10 MB á kall, svo skrár >10 MB voru forbútaðar í `<9 MB` vel-formaða `<ListRecords>`-búta (xmlns er lýst per-record á `<oai_dc:dc>`, svo bútar eru sjálfstæðir): `.tmp-ismus-chunks/sagnir_01–04.xml` (11.312) og `hljodrit-0N_01/02.xml` (10.000 hvert). TEST-3 (8 KB), hljóðrit-06 (0,6 MB) og fólk (7,4 MB) fóru beint.

---

## Lærdómar sem skipta máli við replay
- Ný ME-regla fer sjálfkrafa í **Private** → verður að verða **Shared** (B1), annars finnst hún ekki í Drools File Key.
- Drools File Key sem sýnir „(not listed)" = dinglandi tenging → allar færslur falla á „Parsing Error … Input record path".
- Kóðaritillinn tekur **raunverulegan innslátt** (type), ekki JS-gildissetningu.
- Scope + slot virkuðu án „Switch to Live" (vísun í NDE-view-ið beint).
- **Regluheitið í Ölmu getur verið annað en .drl-skráarnafnið** (`SMB_Ismus_xml` í Ölmu vs `ISMUS_XML_Processes.drl` á disk; sama með Listasafn). Alltaf opna ferlið (Normalization Process Task → Task Parameters → Drools File Key) og uppfæra ÞÁ reglu sem þar stendur — ekki giska út frá skráarnafni.
- Við að uppfæra reglu sem ferli vísar nú þegar í þarf hvorki nýtt ferli né Shared/Private-breytingu — bara skipta innihaldi út og Save.
- Við innlestur um `file_upload`-tólið (vafralota) er ~10 MB þak á kall → forbúta skrár >10 MB í `<9 MB` `<ListRecords>`-búta. Handvirk upphleðsla í vafra hefur ekki þetta þak (Alma bútar sjálf).
- **Local field > 50 tekur EKKI „Use the parallel Local Field 01/50 from the Dublin Core record"** (Alma hafnar) → DC/ytri færslur fylla hann aldrei. Nota reiti ≤ 50 fyrir ný DC-svæði (MSHL: `local_field_11–20`).
- **Reitabreyting fyllir ekki fyrirliggjandi færslur** — eftir að reitur fær parallel-DC/search þarf endurkeyrslu (Run) svo gögnin fari í vísinn.
- **Prófíll keyrir eitt job í einu** — `Submit` meðan annað job vinnst hafnar með „a dependent job is already in process". Bíða eftir „Completed Successfully". (Build-fasinn má skarast.)
- **Facet verður að vera virkur í view-inu** — „Enable for facet" á reitnum dugar ekki; bæta sem local facet í Configure Views → Brief Results → „Add a Local Facet".

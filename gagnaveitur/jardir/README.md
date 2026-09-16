# Jarðir og fasteignir

Skrá Þjóðskjalasafns Íslands yfir jarðir og fasteignir: bæir sem nefndir eru í
jarða- og landamerkjabókum, og bækurnar sjálfar. Þjóðskjalasafn Íslands á gögnin.

## Endapunktur

| Atriði | Gildi |
|---|---|
| `baseURL` sem `Identify` auglýsir | `https://jardir.skjalasafn.is/oai` (án skástriks) |
| Slóð sem virkar | `https://jardir.skjalasafn.is/oai/` (með skástriki) |
| `metadataPrefix` | `oai_dc` eingöngu (`ListMetadataFormats`) |
| Sett | `type:baer` · `type:bok` · `source:skjalasafn` · `era:18c` · `era:19c` · `era:20c` |
| `completeListSize` | `type:baer` 7.866 · `type:bok` 133 · `source:skjalasafn` 7.999 |
| `deletedRecord` / `earliestDatestamp` | `persistent` / 2015-07-02 |
| `datestamp` allra færslna | `2026-09-04T07:15:04Z` |
| Mælt | 4.9.2026, endurmælt 7. og 8.9.2026 (full uppskera, ekki úrtak) |

Uppskeran 7.9 borin saman við uppskeruna 4.9: 7.999 einkvæmar færslur bæði
skiptin, 0 færslur með breytt lýsigögn, sami `datestamp`.

## Umfang

| | Fjöldi |
|---|---:|
| Einkvæmar færslur (á `header/identifier`) | **7.999** |
| Bæir (`oai:…:baer:N`) | **7.866** |
| Bækur (`oai:…:bok:N`) | **133** |
| Bæir sem bera SMB-slóð í `dc:relation` | **7.866** (100 %) |
| Hlutfall af bæjum í SMB (7.866 af 17.371) | **45,3 %** |
| Ólíkir bókartitlar sem vitnað er í úr `dc:source` á bæjum | **112** af 133 (21 bók aldrei vitnað í) |
| Lesið inn í Leitir (mælt 14.9.2026) | 7.859 = 7.726 bæir + 133 bækur |

Báðar setgöngur (`type:baer` og `type:bok`) skila að lokum sömu 7.999 færslunum.

## Reitir sem berast

Þekja mæld 8.9.2026 á fullri uppskeru. Bæir n = 7.866, bækur n = 133.

| DC-reitur | Þekja bæir | Þekja bækur | Dæmi um gildi | Athugasemd |
|---|---:|---:|---|---|
| `dc:title` | 100 % | 100 % | `Eiði` · `Landamerkjabók Árnessýslu` | `xml:lang="is"`, 1×. 4.866 ólík bæjaheiti |
| `dc:type` | 100 % | 100 % | `Bær`/`Place` · `Bók`/`Register` | Par `@is`+`@en`, 2× |
| `dc:identifier` | 100 % | 100 % | `oai:jardir.skjalasafn.is:baer:1` + `https://jardir.skjalasafn.is/baer/1` | 2×: OAI-auðkenni og slóð |
| `dc:date` | 100 % | 100 % | `1921/1921` | 5.448 bæir og 119 bækur bera strenginn `None` |
| `dc:source` | 100 % | 100 % | `Fasteignamat 1916-1918` | Allt að 10 gildi á bæ; 26.459 ó-http eintök, 112 ólík |
| `dc:relation` | 100 % | 0 % | `https://smb.mshl.is/baer/1` | Sama númer og í OAI-auðkenninu, 0 misræmi |
| `dc:coverage` | 99,9 % | 84,2 % | `Hreppur: Staðarhreppur` · `Sýsla: Skagafjarðarsýsla` | 257 ólík gildi; allt að 5 á bæ og 23 á bók |
| `dcterms:spatial` | 83,2 % | 0 % | `POINT(-22.898 65.964)` | `xsi:type="dcterms:Point"` á öllum 6.543 |
| `dc:description` | 100 % | 99,2 % | `Eiði` | Orðrétt eins og titillinn á bæjum |
| `dc:creator` | 100 % | 100 % | `Þjóðskjalasafn Íslands` | Eitt einstakt gildi |
| `dc:contributor` | 100 % | 100 % | `ad libitum ehf` | Eitt einstakt gildi |
| `dc:publisher` | 100 % | 100 % | `Jarðir og fasteignir` | Eitt einstakt gildi |
| `dc:rights` | 100 % | 100 % | CC-BY 4.0 | Eitt einstakt gildi |
| `dc:language` | 100 % | 100 % | `is` | Eitt einstakt gildi |

Engin færsla ber tómt svið; engin `dc:subject` utan fasta gildisins `Bær`/`Bók`.

## Kortlagning í Leitir

Reglusettið heitir `JARDIR_XML_Processes` (19 reglur, Type XML). Útgáfan með
forskeytaklippingu, `JARDIR_XML_Processes-v2-forskeyti`, er 49 reglur.

| DC-reitur | PNX-svið | Hlutverk |
|---|---|---|
| `dc:title` | `dc.title` + `discovery.local1` | birting, leit |
| *(fast)* | `discovery.local5` = `JARDIR` | sía (gagnaveita) |
| *(fast)* | `dcterms.source` = `XDS` | umfangssía |
| `dc:type[@xml:lang='en']` = `Place` / `Register` | `discovery.resourceType` = `places` / `books` | sía, birting |
| sama | `discovery.local2` = `place` / `register` | sía |
| `dc:date` (nema strengurinn `None`) | `dc.date` | birting, leit |
| `dc:coverage` sem byrjar á `Hreppur:` | `discovery.local24` | sía |
| `dc:coverage` sem byrjar á `Sýsla:` | `discovery.local25` | sía |
| `dc:coverage` (öll gildi) | `dc.coverage` | leit |
| `dc:source` sem er ekki http | `discovery.local26` (Heimild) | birting |
| `dcterms:spatial` | `discovery.local27` | birting |
| `dc:identifier` sem byrjar á http | `dcterms.source` + `dc.identifier` | tengill heim |
| `dc:relation` (SMB-slóð) | `discovery.local31` | birting |
| `dc:subject` | `dc.subject` | leit |
| `dc:language` · `dc:publisher` · `dc:rights` | sömu svið | birting |

Vísvitandi ekki varpað: `dc:creator` og `dc:contributor` (eitt gildi á öllum
7.999 færslum, myndu fylla höfunda-síuna `lds49`) og `dc:description` (orðrétt
eins og titillinn á 100 % bæja).

## Þekkt frávik

1. **Bókarslóð vísar á bæ.** Allar 133 bækurnar bera
   `https://jardir.skjalasafn.is/baer/{bok-id}` í `dc:identifier` og `dc:source`;
   0 af 133 bera `/bok/`-slóð. `/baer/1` er bærinn Eiði, `/bok/1` er
   Landamerkjabók Árnessýslu — báðar skila 200. Tengill úr leitarviðmóti opnar
   því ranga færslu á öllum bókum.
2. **`dc:date` er strengurinn `None`** á 5.448 bæjum (69,3 %) og 119 bókum
   (89,5 %). Þetta er texti, ekki nullgildi, og hvert kerfi sem les færsluna les
   hann sem ártal.
3. **Þriggja stafa ártöl** á tveimur færslum: `baer:1081` = `922/1923` og
   `bok:22` = `922/1958`. Hvernig vísirinn les þau er ómælt.
4. **`resumptionToken` lekur milli setta.** `set=type:baer` skilar 80 skömmtum;
   skammtur 79 er blandaður (66 bæir + 34 bækur) og skammtur 80 aðeins bækur.
   Sama mynstur öfugt á `type:bok`. Sá sem gengur settið til enda og treystir
   settinu fær ranga heild.
5. **`era:*` sett auglýst en tóm.** `ListSets` auglýsir `era:18c`, `era:19c` og
   `era:20c`; `ListRecords` á þau skilar `noRecordsMatch`. Engir hausar bera
   `era:`-setSpec.
6. **Hnit með víxluðum ásum** á einni færslu: `baer:2036` ber
   `POINT(64.027633 -20.216834)`. Hin 6.542 hnitin eru `POINT(lengd breidd)` með
   lengd −25…−13 og breidd 63…67. Þetta er eina hnitið af 6.543 sem fellur utan
   Íslands.
7. **`dc:creator` = Þjóðskjalasafn Íslands og `dc:contributor` = ad libitum ehf**
   á öllum 7.999 færslum. Þetta er upprunamerking, ekki höfundur, og gefur
   höfunda-síu með einum flokki.
8. **Endapunkturinn stenst ekki POST-kröfuna.** `POST` á auglýstu slóðina
   (`/oai`) skilar 301 og meginmál beiðninnar fellur niður í endurvísuninni;
   svarið verður `badVerb` (474 bæti) á meðan `/oai/` skilar réttu svari
   (767 bæti). OAI-PMH 2.0 kafli 3.1.1.3 krefst þess að gagnaveita styðji bæði
   GET og POST. Skiptir máli fyrir uppskerubúnað sem skiptir yfir í POST þegar
   `resumptionToken` verður of langt fyrir fyrirspurnarstreng.
9. **`Identify` ber engan `adminEmail`.** OAI-PMH 2.0 krefst a.m.k. eins.
   Formlegt frávik; stöðvar engan uppskerubúnað.
10. **Sókn vantar** miðað við sama auðkenni í SMB (athugað á Eiði, Skarðsá og
    Bakka), og ártöl eru jarðamatsár en ekki manntalsbil (Eiði: 1921/1921 hér á
    móti 1703/1915 í SMB). Færslur verða því ekki sameinaðar á titli og ártali —
    tengingin er `dc:relation` og sama númer.

Athugasemd: að bjóða aðeins `oai_dc` er **ekki** frávik — það er skyldusniðið.
Afleiðingin er sú ein að stjórnsýslustig berast sem textaforskeyti í `dc:coverage`.

## Hvað við gerum við þau

- **Bókarslóðin** er leiðrétt í okkar eigin upphleðsluskrá (`-bokslod-`-skrárnar):
  `/baer/{bok-id}` er skrifað sem `/bok/{id}` í bæði `dc:identifier` og
  `dc:source` á bókunum 133. Bæirnir eru ósnertir. Þegar upprunakerfið lagar
  slóðina verður leiðréttingin no-op og bækurnar lesnar inn ofan í þær fyrri
  (yfirskrifast á auðkenni).
- **`dc:date` = `None`** er síað út í reglunni
  (`jardir dc:date skip literal None`, `[not(text()='None')]`). Færslan fær þá
  ekkert ártal frekar en rangt ártal.
- **Forskeyti** (`Hreppur: `, `Sýsla: `) eru klippt í reglunni **eftir** að hún
  hefur ratað á forskeytinu — reglurnar rata á því og það verður að vera kyrrt í
  upphleðsluskránni. Ein regla á hverja ítrun; 24 ítranir á hrepp og 8 á sýslu,
  því 96 af 133 bókum bera fleiri en fimm hreppa og ein ber 19.
- **Settaleki og tóm sett** eru sniðgengin með því að lesa inn síaðar skrár
  (skráarinnlestur) í stað þess að ganga lifandi sett til enda.
- **Bæir og bækur fara á einn import-prófíl** (`JARDIR`): hver einasta færsla ber
  nákvæmlega eina http-slóð í `dc:identifier`, svo ein Delivery-regex
  (`https://jardir.skjalasafn.is/.*`) nær báðum tegundum.
- **Villuskráin** (atriði 1–9) er tekin saman fyrir gagnaeigandann. Ekkert af
  atriðunum stöðvar innlestur; leiðréttingar okkar megin falla út þegar þau
  eru löguð við upptök.

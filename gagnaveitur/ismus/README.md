# Ísmús og Sagnagrunnur

Þjóðfræðisafn Stofnunar Árna Magnússonar í íslenskum fræðum: hljóðritasafnið
(SÁM-númer) og Sagnagrunnur — skráðar íslenskar þjóðsögur. Endapunkturinn var
smíðaður fyrir evrópska verkefnið ISEBEL (`search.isebel.eu`).

## Endapunktur

| | |
|---|---|
| baseURL | `https://ismus.is/oai_pmh/` |
| repositoryName | Sagnagrunnur OAI 2.0 Data Provider |
| adminEmail | skráð ✅ |
| protocolVersion | 2.0 |
| metadataPrefix | **`isebel`** eingöngu — `oai_dc` skilar `cannotDisseminateFormat` |
| Sett | engin (`noSetHierarchy`) |
| granularity | `YYYY-MM-DDThh:mm:ssZ` |
| deletedRecord | `transient` |
| earliestDatestamp | 2023-09-19T15:52:47Z |
| completeListSize | **22.729** |
| Mælt | 16.9.2026, full uppskera |

`isebel`-sniðið er ríkara en Dublin Core: það ber hlutverk á fólki og stöðum,
hnit á stöðum og heildartexta sögunnar.

## Umfang

Mælt 16.9.2026 — 22.658 færslur sóttar og þáttaðar af 22.729.

| | Færslur | Með texta |
|---|---:|---:|
| Hljóðrit (`/tjodfraedi/hljodrit/`) | 12.005 | 12.004 |
| Sagnir (`/tjodfraedi/sagnir/`) | 10.653 | 5.957 |
| **Alls** | **22.658** | **17.961 (79 %)** |

Textalengd — sagnirnar bera söguna sjálfa, ekki útdrátt:

| | Miðgildi | 90. hundraðshluti | Hámark |
|---|---:|---:|---:|
| Sagnir | 520 stafir | 1.282 | 8.695 |
| Hljóðrit | 120 stafir | 458 | 3.889 |

ISEBEL-vísirinn hefur 17.961 færslur úr þessu safni — nákvæmlega þær sem bera
texta. Endapunkturinn gefur 4.768 færslum meira.

## Reitir sem berast

| ISEBEL-reitur | Þekja | Dæmi | Athugasemd |
|---|---:|---|---|
| `dc:identifier` | 100 % | `is.sagnagrunnur.SG_1510` | varanlegt |
| `isebel:purl` | 100 % | `https://ismus.is/tjodfraedi/sagnir/1510` | tengill heim |
| `dc:title` | 100 % | `Séra Högni Sigurðsson` | 2 færslur án titils |
| `dc:type` | 100 % | `legend` | **alltaf sama gildi**, líka á hljóðritum |
| `isebel:contents` | 100 % | heildartexti sögunnar | 79 % bera raunverulegan texta |
| `isebel:keywords` | ~98 % | `Priests/Ministers` · `Æviatriði` | 80.484 tilvik, 586 ólík orð, 95 % á ensku |
| `isebel:persons` | ~97 % | `Jón Árnason` + hlutverk | 3.506 ólík nöfn |
| `isebel:places` | ~90 % | `Stafafell` + hnit + hlutverk | 16.642 ólík staðanöfn, ~79 % með hnit |
| `xml:lang` | 100 % | `is` | rétt sett |
| dagsetning | **0 %** | — | ekkert dagsetningarsvið í sniðinu |

**Hlutverk eru merkt — það gerir engin önnur mæld gagnaveita.**

| Fólk | Staðir |
|---|---|
| `collector` · `skrasetjari` | `narration` — þar sem sagan gerist |
| `informant` · `heimildarmadur` · `sendandi` | `recording` — þar sem hún var hljóðrituð |

## Kortlagning í Leitir

Reglusett `ISMUS_XML_Processes` (19 reglur). Gögnin fara fyrst gegnum smið sem
umbreytir ISEBEL í gullið Dublin Core.

| Gullið DC | PNX-svið | Hlutverk |
|---|---|---|
| `dc:title` | `dc.title`, `discovery.local1` | birting, leit |
| `dc:type[@xml:lang='en']` | `discovery.local2`, `resourceType` | sía |
| `dc:description` | `dc.description` | **heildartexti — leit og birting** |
| `dc:subject[@xml:lang='is'][xsi:type=mshl:flokkur]` | `dc.subject`, `discovery.local93` | **efnissía** (18 flokkar) |
| `dc:subject` (efnisorð, is + en) | `dc.subject` | leit |
| `dc:coverage` (sögustaður) | `dc.coverage`, `discovery.local22` | **staðarsía** |
| `dcterms:spatial` `POINT(…)` | `discovery.local27` | kort |
| `dcterms:spatial` (upptökustaður) | `dc.coverage` | leit — **ekki sía** |
| `dc:creator` / `dc:contributor` | `dc.creator` / `dc.contributor`, `discovery.local49` | fólk |
| `dcterms:bibliographicCitation` | `discovery.local75` | hlutverk, birting |
| `dc:identifier` (http) | `dc.identifier`, `dcterms.source` | tengill heim |
| (fast) | `discovery.local5` = `ISMUS` | gagnaveitusía |

## Þekkt frávik

1. **71 færsla er ógilt XML og fellir `ListRecords`.** Textinn inni í
   `<![CDATA[ … ]]>` inniheldur sjálfur `]]>` (og í einu tilviki stýritákn),
   svo CDATA-hlutinn lokast of snemma. Þjónninn svarar PHP fatal error
   (`DOMDocument::importNode(): … null given`). Villan er á línu 8 í 69 af 71
   tilvikum. Hlutfall: 0,31 %. Afleiðing: `ListRecords` skilar fyrstu 100
   færslum og deyr; færslurnar 22.600 sem á eftir koma eru óaðgengilegar
   á þeirri leið.
2. **`from` og `until` eru hunsuð.** Beiðni um eina sekúndu skilar
   `completeListSize="22729"`, þ.e. öllu safninu. Engin stigvaxandi uppskera
   möguleg — hver uppfærsla verður full uppskera.
3. **`oai_dc` vantar** þótt `isebel`-skemað vísi sjálft á `oai_dc.xsd`.
   `oai_dc` er skyldusnið OAI-PMH 2.0; án þess kemst enginn almennur safnari inn.
4. **Ekkert dagsetningarsvið.** 0 % þekja. Engin tímasía og engin tímaröðun.
   Ártölin eru þó til í textanum: 3.342 færslur (21 % þeirra sem hafa texta)
   nefna a.m.k. eitt fjögurra stafa ártal.
5. **`dc:type` er `legend` á öllum færslum**, líka 12.005 hljóðritunum.
   Aðgreining fæst aðeins úr slóðinni (`/sagnir/` vs `/hljodrit/`).
6. **Efnisorðin eru 95 % á ensku.** 586 ólík orð; 77 þeirra eru á íslensku.
   Ensku orðin eru þýðingar sem gerðar voru fyrir ISEBEL.
7. **Ellefu efnisorð eiga tvö auðkenni.** 597 auðkenni bera 586 ólíka
   merkimiða — t.d. `elves` = `1000005` (1.888 tilvik) og `24` (61 tilvik),
   `weather` = `1000076` og `1000906`. Ekkert auðkenni ber tvo merkimiða, svo
   auðkennin eru nothæf sem lyklar; tvítökin þarf bara að sameina.
8. **Upptökustaðir og sögustaðir eru í sama lista** (aðgreindir með hlutverki).
   Algengustu upptökustaðirnir eru Hrafnista, Elliheimilið Grund og heimilisföng
   í Reykjavík. Færu þeir óaðgreindir í staðarsíu myndu þeir tróna yfir
   íslenskum þjóðsögum.

**Það sem er gert vel og er sjaldgæft:** varanleg auðkenni á fólki, stöðum og
efnisorðum · hlutverk á bæði fólki og stöðum · hnit á ~79 % staða · heildartexti.

## Hvað við gerum við þau

| Frávik | Viðbrögð |
|---|---|
| 1 — brotnar færslur | `ListRecords` sniðgengið: `ListIdentifiers` (228 síður) + `GetRecord` á hverja færslu. 22.729 fyrirspurnir, 6 samhliða, ~30 mín. Brotnu 71 einfaldlega vantar |
| 2 — `from`/`until` | full uppskera í hvert sinn; forskriftin er endurræsanleg svo hún heldur áfram þar sem frá var horfið |
| 3 — `oai_dc` | við lesum `isebel` beint og umbreytum sjálf |
| 4 — dagsetningar | ekkert sett í `dc:date`. Ártöl úr texta koma síðar í `dcterms:temporal`, **merkt sem vélgreind** |
| 5 — `dc:type` | tegund leidd af `isebel:purl` → `Sögn`/`Hljóðrit` |
| 6 — enskan | íslensk þýðing á öllum 586 orðunum + kortlagning í 18 sameiginlega efnisflokka. Frumgildið varðveitt í `dc:subject[@xml:lang='en']` |
| 7 — tvítekin auðkenni | kortlagning okkar er á merkimiða, svo tvítökin skipta ekki máli |
| 8 — staðahlutverk | sögustaðir fara í staðarsíuna, upptökustaðir aðeins í leit og birtingu |
| stýritákn og `]]>` | síuð burt í smiðnum áður en skrifað er |

## Tengt

- [Hverju eiga gagnaveitur að skila?](../../oai-pmh/LEIDBEININGAR.md)
- [Efnisflokkarnir 18](../../efnisord/FLOKKAR.md) · [orðaforði Ísmús](../../efnisord/ismus-efnisord.tsv)

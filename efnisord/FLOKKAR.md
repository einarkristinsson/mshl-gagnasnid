# Efnisflokkarnir — sameiginlega efnissían

**Vandinn:** hver gagnaveita á sinn orðaforða. Ísmús á 586 efnisorð, Sarpur
sín eigin, Handrit stýrðan lista, SMB eitt orð (`Bær`). Þau mætast hvergi, og
sía með mörg hundruð gildum er ónothæf hvort sem er.

**Lausnin er tvö lög.**

| Lag | Fjöldi gilda | Hvar það birtist |
|---|---|---|
| **Efnisflokkur** — sameiginlegur | 18 | **sían sem fólk smellir á** (`local93`) |
| **Efnisorð** — orðaforði veitunnar | hundruð | leitanlegt, sést á spjaldinu (`dc.subject`) |

Frumgildi veitunnar er alltaf varðveitt. Flokkurinn er viðbót, ekki skipti.

---

## Flokkarnir 18

Tölurnar eru færslur úr Ísmús/Sagnagrunni sem lenda í hverjum flokki
(mælt 16.9.2026 á 22.658 færslum; ein færsla getur borið marga flokka).

| Flokkur | Ísmús | Dæmi um efnisorð sem lenda þar |
|---|---:|---|
| Þjóðtrú og fyrirboðar | 6.700 | Draumar · Fyrirboðar · Feigðarboð · Fylgjur |
| Draugar og afturgöngur | 5.522 | Draugar · Nafnkenndir draugar · Reimleikar · Sædraugar |
| Ævi og fjölskylda | 4.711 | Slys · Fæðingar · Brúðkaup · Barnadauði |
| Kirkja og kristni | 4.463 | Prestar · Messa · Kirkjur · Bænir |
| Náttúra og dýr | 3.880 | Veður · Hestar · Húsdýr · Fuglar |
| Staðir og örnefni | 3.789 | Örnefnasögur · Hellar · Eyjar · Fossar |
| Kveðskapur og sagnalist | 3.727 | Kvæði · Rímur · Sagnamenn · Kvöldvökur |
| Fólk og mannlýsingar | 3.716 | Mannlýsingar · Aflraunamenn · Utangarðsfólk |
| Galdur og kraftaskáld | 3.459 | Galdur · Kraftaskáld · Álög · Sendingar |
| Atvinna og verkmenning | 3.193 | Smiðir · Póstar · Verslun · Vegagerð |
| Huldufólk | 3.008 | Álfar og huldufólk · Álfabyggðir · Álfahefnd |
| Sjósókn og sjávarfang | 2.678 | Sjósókn · Bátar og skip · Formenn · Hvalreki |
| Samfélag og stjórnsýsla | 2.547 | Yfirvöld · Vesturfarar · Sakamenn · Alþingi |
| Heimili og daglegt líf | 2.511 | Matur og drykkur · Klæðnaður · Húsakostur |
| Tröll og forynjur | 1.969 | Tröll · Skessur · Skrímsli og furðudýr |
| Búskapur og sveitastörf | 1.892 | Búskaparhættir · Göngur og réttir · Sel og selstöður |
| Hátíðir og tímatal | 791 | Jól · Þorri · Góa · Sumardagurinn fyrsti |
| Leikir og skemmtun | 670 | Leikir · Dans · Gátur · Glíma |

Flokkarnir eru **ekki** tæmandi kerfi yfir íslenska menningu. Þeir eru
smíðaðir svo sían hafi 18 gildi en ekki 586, og svo gildin séu þau sem fólk
þekkir. Hvert efnisorð fær nákvæmlega einn flokk.

---

## Hvernig þetta lítur út í færslunni

```xml
<!-- sían: fáir, sameiginlegir flokkar -->
<dc:subject xml:lang="is" xsi:type="mshl:flokkur">Huldufólk</dc:subject>
<dc:subject xml:lang="is" xsi:type="mshl:flokkur">Búskapur og sveitastörf</dc:subject>

<!-- efnisorð veitunnar, þýdd -->
<dc:subject xml:lang="is">Álfabyggðir</dc:subject>
<dc:subject xml:lang="is">Búskaparhættir álfa</dc:subject>

<!-- frumgildið, varðveitt -->
<dc:subject xml:lang="en">elven settlements</dc:subject>
<dc:subject xml:lang="en">elven farming ways</dc:subject>
```

---

## Kortlagningarskrár

| Skrá | Gagnaveita | Línur |
|---|---|---:|
| [`ismus-efnisord.tsv`](ismus-efnisord.tsv) | Ísmús og Sagnagrunnur | 586 |

Snið: `#enska ⇥ islenska ⇥ flokkur ⇥ id`

```
elves	Álfar og huldufólk	Huldufólk	1000005
Named ghosts	Nafnkenndir draugar	Draugar og afturgöngur	1000011
```

`id` er auðkenni orðsins hjá veitunni. Það er ástæðan fyrir því að þessi tafla
er þess virði: merkimiðar breytast, auðkenni eiga ekki að gera það. Þess vegna
biðjum við gagnaveitur um **varanlegt auðkenni á hvert efnisorð**.

## Viðhald

1. Ný gagnaveita → ný `<veita>-efnisord.tsv`, sömu 18 flokkar.
2. Nýtt efnisorð hjá veitu sem er þegar kortlögð → ný lína. Orð sem vantar
   fer óflokkað í gegn; það glatast ekki, það kemst bara ekki í síuna.
3. **Flokkunum sjálfum er ekki fjölgað nema að vel athuguðu máli.** Nítján
   flokkar eru ekki betri en átján; sextíu eru verri en engir.

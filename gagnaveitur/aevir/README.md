# Ævir lærðra manna

Æviskrár lærðra Íslendinga í 66 bindum, varðveittar hjá Þjóðskjalasafni Íslands
og myndaðar þar. Þjóðskjalasafn Íslands á gögnin.

## Endapunktur

**Þessi gagnaveita skilar ekki OAI-PMH.** Gögnin bárust sem eitt skjal.

| Atriði | Gildi |
|---|---|
| Afhendingarsnið | Excel-skjal (`.xlsx`) frá Þjóðskjalasafni Íslands |
| Efni skjalsins | 2.801 lærður maður + 66 bindi |
| Afhendingardagur | ekki skráð |
| Unnið úr skjalinu | 4.9.2026, endurbyggt 10.9.2026 |
| Myndbirting bindanna | `https://skjalamyndir.skjalasafn.is/IS-THI-0043-2019-087-A-A-00NN-01` |
| Skjalaskrá | `https://skjalaskrar.skjalasafn.is/detail.aspx?ID=…` |

Skjalinu er breytt í Dublin Core á `try_A`-sniði (bert `<ListRecords>`, engin
`<?xml?>`-lína, ekkert `xmlns` á rótinni) og lesið inn sem skrá. Tvær skrár
verða til: menn og bindi.

Sniðið fylgir gullna sniðinu að þremur atriðum: hrein gildi með `xsi:type`
(starfsheiti og staður fá eigin flokkun í stað textaforskeytis), óvissa er
varðveitt (vélrænt ártal í `dc:date` **og** upprunalegur strengur í
`dcterms:temporal`), og engin stofnun fer í `dc:creator`.

## Umfang

| | Fjöldi |
|---|---:|
| Menn | **2.801** |
| Bindi | **66** |
| Samtals færslur | **2.867** |
| Einkvæm mannanöfn | 1.702 |
| Nöfn sem eru líka í SMB | 1.311 nöfn = 2.402 færslur (**86 %**) |
| Menn með virkan tengil í myndbirtingu | 1.395 (48 %) |
| Bindi með virkan tengil | 33 af 66 |
| Lesið inn í Leitir | 2 prófunarfærslur (staða 11.9.2026) |

Innlestur er undirbúinn en ekki framkvæmdur. Tillagan er að lesa gagnaveituna
inn í eigið umfang utan samleitarinnar þar til hún hefur verið skoðuð.

## Reitir sem berast

Talið með `xmllint` á raungögnunum 10.9.2026. Menn n = 2.801, bindi n = 66.

| Reitur | Menn | Bindi | Dæmi um gildi | Athugasemd |
|---|---:|---:|---|---|
| `dc:identifier` (auðkenni) | 2.801 | 66 | `oai:aevir.skjalasafn.is:madur:is-0043-…-bls-3-4` | Viðskiptalykill: ÞÍ-tilvísun + blaðsíða |
| `dc:identifier` (ÞÍ-tilvísun) | 2.801 | — | `IS-ÞÍ-0043-2019-087-A-A-0001-01/bls.3-4` | Byrjar á `IS-` |
| `dc:identifier` (slóð) | 2.801 | 66 | `https://skjalamyndir.skjalasafn.is/IS-THI-…-0001-01` | Bætt við í v2 svo Delivery hitti |
| `dc:title` | 2.801 | 66 | `Álfur Gíslason` · `Æfir lærðra manna. 1. bindi` | `xml:lang="is"` |
| `dc:type` | 2.801 | 66 | `Einstaklingur`/`Person` · `Bindi`/`Volume` | Par `@is`+`@en` |
| `dc:subject` `xsi:type="mshl:starf"` | 2.801 | 0 | `prestur` · `stúdent` | Starfsheiti, hreint gildi |
| `dc:coverage` `xsi:type="mshl:stadur"` | 2.793 | 0 | `Kaldaðarnesi` · `frá Melum` | Staður, **í þágufalli** |
| `dc:date` | 2.801 | 0 | `1696/1733` · `1683` | Vélrænt ártal eða bil |
| `dcterms:temporal` | 2.801 | 0 | `um 1696 - 1733` · `óvíst - 1683` | Upprunalegi strengurinn með óvissu |
| `dcterms:isPartOf` | 2.801 | — | `Æfir lærðra manna. 1. bindi, Álfur-Arngrímur.` | Bindið sem færslan er í |
| `dcterms:bibliographicCitation` | 2.801 | — | `Æfir lærðra manna. 1. bindi …, bls. 3-4` | Tilvitnun |
| `dc:relation` | 2.801 | 66 | `oai:aevir.skjalasafn.is:bindi:001` | Menn → bindi; bindi → skjalaskrá |
| `dcterms:source` | 2.801 | 66 | `https://skjalamyndir.skjalasafn.is/…` | Fyrir síun dauðra tengla í v2 |
| `dc:publisher` | 2.801 | 66 | `Ævir lærðra manna` | Fast gildi |
| `dcterms:provenance` | 2.801 | 66 | `Þjóðskjalasafn Íslands` | Fast gildi |
| `dc:description` | — | 66 | `Nöfn í bindinu: Álfur-Arngrímur.` | Aðeins á bindum |
| `dc:language` | 2.801 | 66 | `is` | Fast gildi |
| `dc:creator` / `dc:contributor` | 0 | 0 | — | Vísvitandi engin — stofnun er ekki höfundur |
| `dcterms:spatial` | 0 | 0 | — | Engin hnit |

## Kortlagning í Leitir

Reglusettið heitir `AEVIR_XML_Processes` (23 reglur, Type XML).

| Reitur | PNX-svið | Hlutverk |
|---|---|---|
| `dc:title` | `dc.title` + `discovery.local1` | birting, leit |
| *(fast)* | `discovery.local5` = `AEVIR` | sía (gagnaveita) |
| *(fast)* | `dcterms.source` = `XDS` | umfangssía |
| `dc:type[@xml:lang='en']` = `Person` | `discovery.resourceType` = `people`, `discovery.local2` = `person` | sía, birting |
| `dc:type[@xml:lang='en']` = `Volume` | `discovery.resourceType` = `books`, `discovery.local2` = `volume` | sía, birting |
| `dc:subject` `xsi:type="mshl:starf"` | `discovery.local29` + `dc.subject` | sía, leit |
| `dc:coverage` `xsi:type="mshl:stadur"` | `discovery.local22` + `dc.coverage` | sía, leit |
| `dcterms:temporal` | `discovery.local31` | birting |
| `dcterms:isPartOf` | `discovery.local35` | birting |
| `dcterms:bibliographicCitation` | `discovery.local75` | birting |
| `dcterms:provenance` | `discovery.local44` | birting |
| `dc:identifier` sem byrjar á http | `dc.identifier` + `dcterms.source` | tengill heim |
| `dc:identifier` sem byrjar á `IS-` | `dc.identifier` | birting |
| `dcterms:source` sem byrjar á http | `dcterms.source` | tengill heim |
| `dc:date` · `dc:description` · `dc:language` · `dc:publisher` | sömu svið | birting, leit |

Sniðið er hið sama og `SMB_XML_Processes` og `JARDIR_XML_Processes` nota, svo
gagnaveiturnar deili sviðum og síum.

## Þekkt frávik

1. **Helmingur tengla er dauður.** Mælt 10.9.2026: bindi 1–33 skila HTTP 200 en
   bindi 34–66 skila 302 og lenda á forsíðu myndbirtingarinnar. 1.406 af 2.801
   mönnum og 33 af 66 bindum vísa í þau bindi. Virkur tengill er því á 48 %
   einstaklinga.
2. **Slóðin var ekki í `dc:identifier`** í fyrstu útgáfu skránna, aðeins í
   `dcterms:source`. Hvort `dcterms:source` sé tækt sem Source Tag í Delivery er
   óstaðfest; bregðist það fær færslan tóma slóð og merkið `inkingParameter1`.
3. **Staður er í þágufalli** (`Skálholti`, `Hólum í Hjaltadal`,
   `Vestmannaeyjum`, `Þingeyrum`). Í síu les það skringilega og sameinast ekki
   nefnifallsmyndum úr öðrum gagnaveitum.
4. **`local29` (starf) og `local44` (uppruni) eru ekki til í uppsetningu
   viðmótsins** — þær reglur gera ekkert eins og stendur.
5. **`local31` ber tímabil hér en slóð hjá SMB og Jarðir.** Hausinn sem
   notandinn sér er sameiginlegur, svo hann getur ekki passað báðum.
6. **FRBR-samruni.** 86 % Ævir-manna bera nafn sem er líka í SMB, og þeir bera
   ártal — það sem samrunareglan hópar á. Algeng nöfn (`Jón Jónsson`: 81 færsla
   hér, 3.062 í SMB) eru ólíkir menn. Bælingarreglan náði aðeins yfir tvær
   gagnaveitur þegar þetta var mælt.
7. **Ný gagnaveita fer ekki sjálfkrafa í neitt umfang.** Mælt 10.9.2026: tvær
   færslur sem fóru inn án villu voru ósýnilegar í öllum umföngum í 20+ mínútur.
   Það er ekki bilun heldur skref sem þarf að stíga.
8. **Formin `xsi:type="mshl:starf"` og `xsi:type="mshl:stadur"` eru óprófuð í
   reglukerfinu.** Þau hitta rétt í `xmllint` á raungögnunum; hvort reglukerfið
   þýði þau kemur ekki í ljós fyrr en reglusettið er vistað.

## Hvað við gerum við þau

- **Dauðir tenglar eru felldir út við smíði upphleðsluskrárinnar.** `dcterms:source`
  er sleppt á bindum 34–66 og á mönnunum í þeim bindum. Færsla án tengils er
  betri en tengill sem lendir á forsíðu. Mælingin liggur í `AEVIR-bindi-tenglar-2026-09-10.tsv`
  og leiðréttingin fellur út þegar gagnaeigandinn opnar bindin.
- **Slóðin er afrituð í `dc:identifier`** svo Delivery geti lesið hana úr sama
  sviði og hjá hinum gagnaveitunum. Fyrri útgáfur skránna eru ekki notaðar.
- **Starfsheitið fer líka í `dc:subject`**, svo það glatist ekki þótt
  `local29` sé ekki til í viðmótinu.
- **Gagnaveitan er lesin inn í eigið umfang** utan samleitarinnar þar til hún
  hefur verið skoðuð.
- **Bælingarreglan** er útvíkkuð yfir þessa gagnaveitu áður en lesið er inn, svo
  samnefndir menn renni ekki saman við SMB-fólk.
- **Þágufallið** verður ekki leyst okkar megin í þessum áfanga. Á meðan fer
  staðurinn í `local22` en ekki í sýslusíurnar, svo hann mengar þær ekki.

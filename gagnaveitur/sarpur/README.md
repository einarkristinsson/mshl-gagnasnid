# Sarpur

Sameiginlegt skráningarkerfi íslenskra menningarminjasafna. Hvert safn á sínar
færslur og heiti þess stendur í `dc:publisher` (`Þjóðminjasafn Íslands
(Sarpur.is)`, `Minjasafn Austurlands (Sarpur.is)` o.s.frv.). Kerfið og
OAI-endapunkturinn eru hýst hjá Zetcom.

## Endapunktur

| Atriði | Gildi |
|---|---|
| `baseURL` | `https://rosetta-icelandsarpur.ciim.zetcom.group/oai` |
| `metadataPrefix` | `oai_dc` |
| Sett | ekki mælt (uppskeran er sótt án `set`-síu) |
| `completeListSize` | ekki mælt |
| Dagsetning mælingar | ekki skráð |

**Endapunkturinn er skjalfestur sem bilaður uppruna megin: aðeins
`ListIdentifiers` virkar áreiðanlega** (skráð 18.8.2026). Þess vegna eru gögnin
ekki sótt beint í Leitir heldur lesin inn sem skrár.

**Afhendingin.** Niðurhalari (í `leidarljos/dc-template/sources/sarpur/`) gengur
`ListRecords` með `resumptionToken` og skrifar allt að 10.000 færslur í hverja
XML-skrá á OAI-sniði, tilbúnar til innlestrar. Niðurhalarinn styður endurræsingu
úr stöðuskrá — það er forsenda, því tokenið rennur út í löngum keyrslum. Sarpur
er þegar gagnaveita í Gegni og var ekki uppskorinn upp á nýtt í þessum áfanga.

## Umfang

| | Fjöldi |
|---|---:|
| Færslur í Leitir undir Sarpi (mælt 14.9.2026, `q=?*`) | **787.346** |
| Hlutmengi mælt 9.9.2026 á `lds05=dsSarpur` | 319.784 |
| — þar af munir | 116.958 |
| — myndir | 172.296 |
| — annað | 27.730 |
| — bækur | 2.800 |

Tvö úrtök liggja að baki reitagreiningunni hér á eftir:

| Úrtak | Færslur | Hvað það er |
|---|---:|---|
| Mannamyndaúrtak | 3.000 (6 skrár) | Eingöngu ljósmyndir Þjóðminjasafnsins úr Mannamyndasafni |
| Gripaúrtak, mælt 1.9.2026 | 10.000 | Eingöngu `base_type:object` — munir, myndlist, ljósmyndir. Engin örnefni, þjóðhættir eða mannamyndaskrár |

Hvorugt úrtakið lýsir Sarpi öllum. Tölur hér eru merktar því úrtaki sem þær
koma úr.

## Reitir sem berast

Þekja í mannamyndaúrtakinu (n = 3.000), nema annað sé tekið fram.

| DC-reitur | Þekja | Dæmi um gildi | Athugasemd |
|---|---:|---|---|
| `dc:title` | 100 % | `Karlmaður` · `Hópmynd, óskilgreinanleg` | 1.157 ólík gildi. Í gripaúrtakinu aðeins **32,2 %**, og 32,7 % þeirra eru staðgenglar (`(Nafnlaus)`, `Án titils`) → raunverulegir titlar 21,7 % |
| `dc:type` | 100 % | `Photography` · `Ljósmyndir` · `Mannamyndir` | Allt að 3 gildi; ensk og íslensk heiti í sama sviði |
| `dc:publisher` | 100 % | `Þjóðminjasafn Íslands (Sarpur.is)` | Varðveislustofnun |
| `dc:relation` | 100 % | `Mannamyndasafn (Mms)` | Safn-/skrárheiti, ekki tengill |
| `dc:format` | 100 % | `Stærð aðfangs: 9 x 6 cm` · `Þurrnegatíf Gler` | Allt að 3 gildi; 317 ólík. Gripaúrtak: 89,9 % |
| `dc:language` | 100 % | `is` | Eitt gildi |
| `dc:subject` | 100 % | `Karlmaður` · `Prestur` · `Póstkort` | Allt að 17 gildi, 542 ólík. Gripaúrtak: 82,1 % |
| `dc:creator` | 93 % | `Sigfús Eymundsson (25.5.1837 - 20.10.1911)` | 712 ólík gildi; æviár inni í nafnastrengnum á 86,5 % |
| `dc:contributor` | 58 % | `Matthías Þórðarson (30.10.1877 - 29.12.1961)` | Allt að 33 gildi á færslu |
| `dc:coverage` | 35 % | `Staður: Möðruvellir 1, 601-Akureyri, Hörgársveit` | Einn samsettur strengur. **Gripaúrtak: 0 %** |
| `dc:date` | 26 % | `1920 - 1930` · `30.10.1957` · `01.01.1897` | 236 ólík gildi. Gripaúrtak: sjö ólík form, 41,2 % vélrænt þáttanleg |
| `dc:description` | ekki mælt í mannamyndaúrtaki | — | Gripaúrtak: 74,2 % |
| `dc:identifier` | ekki mælt í mannamyndaúrtaki | `ÁBS-13680 (Safnnúmer A)` + `https://sarpur.is/…/item/<id>/` | Tvö gildi: safnnúmer og slóð |
| `dc:rights` | sást ekki | — | Ekkert leyfissvið í úrtökunum |
| `dcterms:spatial` | sást ekki | — | Engin hnit |

## Kortlagning í Leitir

Sarpur keyrir **þrjú reglusett í röð** í Alma. Þau eru eldri en þetta verkefni og
voru afrituð 4.6.2026; þeim hefur ekki verið breytt.

| Reglusett | Hlutverk |
|---|---|
| `sarpur_xml_to_dc` | Grunnur: afritar hvern `dc:*`-reit beint í `dc.*` (13 reglur) |
| `Sarpur_multi_title` | Titill (1 regla) |
| `nyr_sarpur_normalization` | Tegund, gagnaveita, tenglar, höfundar (6 reglur) |

| Uppruni | PNX-svið | Hlutverk |
|---|---|---|
| `dc:title` | `dc.title` + `discovery.local1` | birting, leit |
| *(fast)* | `discovery.local5` = `dsSarpur` | sía (gagnaveita) |
| *(fast)* | `dcterms.source` = `XDS` | umfangssía |
| `dc:type[1]` | `discovery.resourceType` (`images`, `books`, `artifacts`, `other`) | sía, birting |
| sama | `discovery.local2` (`image`, `object`, `coin`, `ruin`, `artwork`, `house`, `book`, `drawing`, `rock`, `ethnology`, `archeologicalFind`) | sía |
| `dc:identifier` sem byrjar á http | `dcterms.source` | tengill heim |
| `dc:relation` sem byrjar á `https://sarpur.is/multimedia` | `dcterms.source` | smámynd |
| `dc:creator` (svigar um æviár fjarlægðir) | `dc.creator` | birting, leit, sía (`lds49`) |
| `dc:type` · `dc:contributor` · `dc:publisher` · `dc:date` · `dc:language` · `dc:identifier` · `dc:description` · `dc:subject` · `dc:format` · `dc:coverage` · `dc:relation` · `dc:rights` · `dc:source` | sömu `dc.*`-svið | birting, leit |

Sarpur afritar **ekki** `dc:subject` í `discovery.local3`, ólíkt hinum
gagnaveitunum.

## Þekkt frávik

1. **Afritið af `nyr_sarpur_normalization` í verkefnisskránni stemmir ekki við
   lifandi regluna.** Mælt 9.9.2026: lifandi regla skilar 116.958 munum, en
   afritið hefur enga vörpun fyrir `Munir`/`Artifact` og myndi skila **0** munum
   og um 144.688 færslum í `other`. Fleiri línur gætu vantað — það sést ekki af
   disknum. Að líma afritið yfir myndi færa 116.958 muni í ranga tegund.
2. **Staður berst ekki.** `dc:coverage` er 0 % í gripaúrtakinu og engin hnit
   fylgja. Staður er til í gögnunum en aðeins sem prósi inni í lýsingum
   (um 9,6 % færslna). Þetta er eina raunverulega gagnaeyðan í settinu —
   skráningarverk, ekki vörpunarverk.
3. **Titill er ekki áreiðanlegur.** 32,2 % færslna í gripaúrtakinu bera titil, og
   þar af eru 32,7 % staðgenglar. Safngripir heita einfaldlega ekki neitt:
   ljósmyndir 0 %, mannamyndir 0 %, fornleifar 0 %, munir 9 %, en leirlist 100 %.
4. **`dc:date` er á sjö ólíkum formum** (`1800 - 1950`, `= 1985`, `01.01.1907`,
   `Um 1950` …); 41,2 % eru vélrænt þáttanleg. Tíma-sía þvert á gagnaveitur er
   því ekki byggjanleg á þessu sviði eins og það stendur.
5. **`dc:creator` ber ekki alltaf höfund.** Af 904 `Artifact`-færslum með bæði
   ártal og dagsettan höfund eru 55 (6,1 %) með „höfund" fæddan meira en 10 árum
   eftir að hluturinn varð til — sviðið ber þar gefanda eða finnanda. Á myndlist
   ber sama svið raunverulegan listamann (100 %). 6,1 % er gólf, ekki tíðni.
6. **Æviár eru inni í nafnastrengnum** á 86,5 % höfunda
   (`Eva Harne Ragnarsdóttir (14.7.1922 - 12.06.2019)`).
7. **`dc:relation` afritar `setSpec`** — safnheiti, ekki tengil — og
   `dc:identifier` blandar saman safnnúmeri og slóð í endurteknu sviði.
8. **Endapunkturinn er bilaður uppruna megin**: aðeins `ListIdentifiers` virkar
   áreiðanlega.

## Hvað við gerum við þau

- **Skráarinnlestur** úr heildaruppskeru í stað lifandi OAI-uppskeru. Bilaði
  endapunkturinn kemur ekki við sögu þegar lesin er skrá.
- **Lifandi reglunni er ekki skipt út.** Breytingar á `local5` (og annað sem
  kann að þurfa) eru gerðar með því að breyta viðkomandi línu beint í lifandi
  reglunni; afritið í verkefnisskránni er merkt með viðvörun efst svo enginn
  límdi það yfir lifandi textann.
- **Æviársvigar** eru hreinsaðir af `dc:creator` í reglunni með reglulegri
  segð, svo höfunda-sían verði læsileg.
- **Heiti gagnaveitunnar** (`dsSarpur` → `Sarpur`) er sett sem þýðing á
  `lds05`-gildinu. Það er hrein stilling: engin gögn snert, ekkert endurinnlestur,
  afturkræft.
- **Staður, titill, dagsetningar og höfundarflokkun** verða ekki leyst okkar
  megin. Þau fara á beiðnalista til gagnaeigandans; staður er þar dýrasta
  beiðnin því hann krefst skráningar en ekki vörpunar.

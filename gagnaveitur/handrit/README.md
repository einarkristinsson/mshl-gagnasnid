# Handrit.is

Lýsigögn um íslensk handrit í vörslu Landsbókasafns Íslands – Háskólabókasafns,
Stofnunar Árna Magnússonar og fleiri safna. Landsbókasafn afhenti gögnin.

## Endapunktur

**Þessi gagnaveita skilar ekki OAI-PMH.** Gögnin bárust sem heildarútflutningur
í JSON.

| Atriði | Gildi |
|---|---|
| Afhendingarsnið | JSON (`handrit-export.json`, úr `handrit-export-full.zip`) |
| Fjöldi færslna í afhendingunni | **17.937** |
| Afhent | 6.–7.7.2026 |
| Lýsigagnasnið | Dublin Core + DCMI Terms + EDM + `handrit:`-nafnrými |
| Tengill á færslu | `https://handrit.is/manuscript/view/is/<id>` — á **100 %** færslna |
| Frumgögn | TEI P5 á GitHub (`Handrit/Manuscripts`, uppfært daglega) — **ekki notuð** |
| Lifandi OAI-endapunktur hjá handrit.is | ekki mælt |

Afhendingunni fylgdi skjölun á sniðinu frá gagnaeigandanum (field dictionary);
hún er kanónísk heimild um merkingu sviðanna. Útflutningurinn er þegar á
DC/EDM-formi, svo lítil þáttun þarf. Fyrir innlestur er hann skrifaður út á
`try_A`-sniði (bert `<ListRecords>`, engin `<?xml?>`-lína, ekkert `xmlns` á
rótinni) og lesinn inn sem skrá.

> Ein gildra í afhendingunni: tengillinn merktur „full" í fylgibréfinu vísaði á
> lítið úrtak. Nota ber `handrit-export-full.zip` beint.

## Umfang

| | Fjöldi |
|---|---:|
| Handrit í afhendingunni | **17.937** |
| Í Leitir (mælt 14.9.2026) | **17.937** |
| Færslur með fólk skráð | 97 % |
| Einstök mannanöfn (mælt 15.7.2026) | 7.742 |
| Einstök persónuauðkenni (mælt 1.9.2026) | 11.752 |
| Færslur með stafrænar myndir | 4.334 (24 %) |
| Færslur með `dcterms:hasPart` | 17.562 (97,9 %) |
| Hlutar samtals / einstök verkaheiti | 50.819 / **27.610** |

Fólk er flokkað eftir hlutverki. Tilvik, mælt á öllu settinu 15.7.2026:
`other` 38.508 · `authors` 26.754 · `scribes` 11.609 · `provenance` 10.221 ·
`acquisition` 8.868 · `additions` 1.494 · `accMaterial` 1.426 · `origin` 1.219 ·
`translators` 382 · `colophon` 126 · `editors` 17.

## Reitir sem berast

Þekja mæld á öllu settinu (n = 17.937), 15.7. og 1.9.2026.

| Reitur | Þekja | Dæmi um gildi | Athugasemd |
|---|---:|---|---|
| `dc:identifier` | 100 % | `oai:handrit.is:AM02-0104` · `AM 104 fol.` · slóð | Þrjú gildi: auðkenni, safnmark og tengill |
| `dc:title` | 99 % | `Kristni sögu` | Fleiri en einn titill mögulegur (aðal-, samræmdur, tilgreindur) |
| `dc:type` | 100 % | `Handrit` / `Manuscript` | Fast par `@is`+`@en` |
| `dc:subject` | 93,5 % | `Fornrit` · `Biskupasögur` · `Landnám` | Stýrður orðaforði |
| `dcterms:medium` | 99 % | `chart` · `perg` · `mixed` · `Skrift: kanzlei` | Efni og skrift |
| `dcterms:created` | 90 % | `1632/1672` | **Vélrænt þáttanlegt**, sama skástriksform og SMB notar |
| `dc:date` | 66,2 % | `second half of the seventeenth century` | Enskur prósi |
| `dc:language` | 95,1 % | `is` | Tungumál textans, getur verið fleiri en eitt |
| `dc:creator` | 48,6 % | `Björn Jónsson` | Höfundar verkanna |
| `dc:contributor` | 52 % | `Ásgeir Jónsson` | Skrifarar, ritstjórar, þýðendur |
| `dcterms:spatial` | 90 % | `Ísland` · `Villingaholt in southern Iceland` | Frjáls texti, ekki hnit. 284 einstakir strengir |
| `dcterms:relation` `xsi:type="mshl:folk"` | 97,1 % | `Ásgeir Jónsson` með `mshl:role="Skrifari"` | Fólk með hlutverki og varanlegu auðkenni |
| `dcterms:hasPart` | 97,9 % | `Lausavísa um Búa Esjufóstra` | Verkin innan hvers handrits |
| `dcterms:temporal` | — | `17. öld` | Aldursflokkun, `xsi:type="mshl:timabil"` |
| `edm:isShownAt` | 100 % | `https://handrit.is/manuscript/view/is/AM02-0104` | Einn hreinn tengill |
| `dc:rights` | **0 %** | — | Ekkert réttindasvið á neinni færslu |

## Kortlagning í Leitir

Reglusettið heitir `HANDRIT_XML_Processes` (17 reglur, Type XML). Það varpar
**aðeins hreinum `dc:*`-kjarna** og snertir ekkert auðgað svið, svo gagnaveitan
birtist með sömu svið og hinar.

| DC-reitur | PNX-svið | Hlutverk |
|---|---|---|
| `dc:title` | `dc.title` + `discovery.local1` | birting, leit |
| *(fast)* | `discovery.local5` = `HANDRIT` | sía (gagnaveita) |
| *(fast)* | `dcterms.source` = `XDS` | umfangssía |
| `dc:type[@xml:lang='en']` = `Manuscript` | `discovery.resourceType` = `manuscripts` | sía, birting |
| sama | `discovery.local2` = `manuscript` | sía |
| `dc:subject` | `dc.subject` + `discovery.local3` | leit, sía |
| `dc:identifier` sem byrjar á http | `dcterms.source` + `dc.identifier` | tengill heim |
| `dc:creator` · `dc:contributor` | `dc.creator` · `dc.contributor` | birting, leit, sía (`lds49`) |
| `dc:type` · `dc:publisher` · `dc:date` · `dc:language` · `dc:description` · `dc:rights` | sömu svið | birting, leit |

Vísvitandi ekki varpað: `dcterms:medium`, `dcterms:created`, `dcterms:spatial`,
`dcterms:temporal`, `dcterms:relation` og `dcterms:hasPart`. Ólíkt SMB eru
`dc:creator` og `dc:contributor` **raunverulegt fólk** hér og eru því varpaðar.

## Þekkt frávik

1. **`dcterms:hasPart` er hvergi varpað.** 27.610 einstök verkaheiti á 17.562
   handritum (97,9 %) eru ósýnileg í leit. Mælt 2.9.2026: leitarorðið „Skarðsá"
   kemur 158 sinnum fyrir í `dcterms:hasPart` í skránni en leitin skilar 6
   handritum. Handrit.is er safn af verkum, ekki aðeins kódexum, og verkaheitin
   eru það sem fólk slær inn.
2. **`dc:rights` er 0 %** á öllum 17.937 færslunum. Efnið er birt opið, svo þetta
   er vörpunargloppa, en eins og gögnin standa er safnið ómerkt réttindalega.
3. **`dc:date` er enskur prósi** á 66,2 % færslna á meðan vélrænt þáttanlegt
   gildi er þegar til í `dcterms:created` á 90 %.
4. **`dcterms:spatial` er frjáls texti**, 284 einstakir strengir fyrir að mestu
   einn stað: `Ísland` 13.215 · `Íslandi` 936 · `Iceland` 552 · `Íslandi.` 91.
   Tvö tungumál, tvær beygingar og einn punktur. Sama svið ber hnit hjá SMB, svo
   gagnaveiturnar rekast á í því.
5. **`dc:creator` er 48,6 %** þótt hlutverkamerkt fólk með auðkennum sé á 97,1 %
   færslna. Vörpunareyða uppruna megin, ekki gagnaeyða.
6. **Eldra reglusett má ekki nota.** `HANDRIT_XML_Processes_v2.drl` setur
   `local5 = "Handrit-GOLD"`, skilur eftir sýnilegt þróunarmerki í `local75` og
   varpar `edm:provider` í `local49`, sem er virk höfunda-sía — nafn gagnaveitunnar
   lendir þá meðal alvöru höfunda.
7. **Tenglar okkar megin voru ónýtir.** Mælt 15.9.2026: 131 af 250 færslum
   (52 %) báru tómt `serviceUrl` og merkið `inkingParameter1`. Orsök: eitt `$`
   í Link Template á import-prófílnum í stað tveggja.
8. **Skriflegt samþykki gagnaeigandans fyrir birtingu liggur ekki fyrir**, aðeins
   munnlegt. Prófunarumhverfið er lokaður sandkassi, en þetta þarf að liggja
   fyrir áður en lengra er haldið en að sýna niðurstöðuna.

## Hvað við gerum við þau

- **Skráarinnlestur** á `try_A`-sniði; Data Source Code `HANDRIT` (óbreytanlegur
  eftir stofnun) og Delivery-regex `https://handrit.is/manuscript/view/.*`, sem
  allar 17.937 færslurnar passa við.
- **Ný regla var skrifuð** í stað eldra reglusettsins svo hvorki þróunarmerki né
  nafn gagnaveitunnar birtist notandanum. Hún sniðgengur öll auðguð svið og
  notar sömu svið og hinar gagnaveiturnar, svo síur virki þvert á þær.
- **Link Template** leiðrétt í `$$LinkingParameter1` og færslurnar lesnar aftur
  inn. Þar til það er gert á ekki að smella á handritsfærslu í sýningu.
- **`dcterms:hasPart`** þarf eina reglu í leitanlegt svið. Valið stendur milli
  `dc.description`, eigin staðbundins sviðs og leitarrýmisins beint; ákvörðunin
  bíður staðfestingar frá gagnaeigandanum á því hvaða hlutverki sviðinu var ætlað.
- **`dcterms:created`, `dcterms:spatial` og hlutverkamerkt fólk** eru efniviður
  næsta áfanga, ekki þessa innlestrar. Beiðnir um þau fara á gagnaeigandann:
  nota `dcterms:created` sem dagsetningu, samræma staðarnöfn og setja `xsi:type`
  á `dcterms:spatial` svo það rekist ekki á hnit annarra gagnaveitna.
- **Íslenskt heiti á tegundinni** er sett sem þýðing (`mediatype.manuscript` →
  *Handrit*), ekki með breytingu á gögnunum.

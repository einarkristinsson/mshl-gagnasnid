# Hverju eiga gagnaveitur að skila?

**Leiðbeiningar um OAI-PMH og Dublin Core fyrir samþætta leitargátt**
Útgáfa 1.0 · 16. september 2026 · Miðstöð stafrænna hugvísinda og lista

Þetta skjal er ætlað þeim sem reka gagnasafn og vilja að efnið þeirra sé
leitanlegt í samleit með öðrum íslenskum söfnum. Það lýsir tvennu: hvernig
afhendingin á að virka (OAI-PMH) og hvaða reitir þurfa að fylgja (Dublin Core).

Allt sem hér er sýnt kemur úr þeim OAI veitum sem þegar eru aðgengilegar—
Frávik merkt:
🔴 hafa gerst.

---

## 0. Í stuttu máli

Sex reitir og einn endapunktur. Ef ekkert annað næst, þá þetta:

| Reitur | Dæmi | Af hverju |
|---|---|---|
| `dc:title` | `Skarðsá` | það sem stendur á spjaldinu |
| `dc:identifier` (slóð) | `https://safn.is/hlutur/123` | tengillinn heim í kerfið ykkar |
| `dc:type` (par `@is` + `@en`) | `Bær` / `Place` | hvers konar hlutur þetta er |
| `dc:subject` | `Draugar` | efnið — það sem tengir söfn saman |
| `dc:coverage` eða `dcterms:spatial` | `Eyjafjarðarsýsla` | staðurinn — hitt sem tengir söfn saman |
| `dc:date` | `1703/1910` | tíminn |

Og endapunktur á `https://…/oai` sem svarar OAI-PMH 2.0.

**Tvö svið bera samleitina uppi: EFNI og STAÐUR.** Titlar eru sjaldan eins
milli safna, en „Skarðsá" sem staður og „Draugar" sem efni eru það. Án
þessara tveggja verða söfnin þrjú aðskilin listar í sama viðmóti, ekki ein leit.

---

## 1. OAI-PMH — afhendingin

### 1.1 Það sem verður að virka

| Krafa | Athugun |
|---|---|
| `Identify` skilar `repositoryName`, `baseURL`, `adminEmail`, `earliestDatestamp`, `granularity` | `?verb=Identify` |
| `baseURL` í svarinu er **nákvæmlega** sú slóð sem virkar | afrita hana og prófa |
| Bæði **GET og POST** virka á þeirri slóð | staðallinn, kafli 3.1.1.3 |
| `ListMetadataFormats` auglýsir `oai_dc` | skyldusniðið |
| `ListIdentifiers`, `ListRecords`, `GetRecord` virka öll | öll fjögur, ekki bara sum |
| `resumptionToken` gengur alla leið á enda | telja færslur og bera saman við `completeListSize` |
| `from` / `until` sía raunverulega | biðja um eina sekúndu og sjá hvort talan lækkar |
| Villur koma sem OAI-villukóðar | `badVerb`, `idDoesNotExist` — ekki HTML |

### 1.2 Frávik — allar mældar í raunkerfum

🔴 **Ein skemmd færsla fellir alla uppskeruna.**
Færsla með ólokuðu `CDATA` eða stýritákni felldi `ListRecords` í miðri annarri
síðu. Færslurnar 22.600 sem á eftir komu voru óaðgengilegar þar til farið var
framhjá með `ListIdentifiers` + `GetRecord` — 22.729 fyrirspurnir í stað 228.
*Lagfæring:* sannreyna XML við útgáfu og sleppa/merkja skemmdum færslum í stað
þess að láta þjóninn hrynja á þeim.

🔴 **`from`/`until` er hunsað.**
Beiðni um eina sekúndu skilaði `completeListSize` fyrir allt safnið. Þá er ekki
hægt að sækja aðeins það sem breyttist — hver uppfærsla verður full uppskera.

🔴 **Auglýsta slóðin stenst ekki POST.**
`Identify` auglýsti `/oai` (án skástriks). GET þangað fór í 301 á `/oai/` og
hélt fyrirspurnarstrengnum — í lagi. POST fór líka í 301, en meginmál beiðninnar
féll niður og svarið varð `badVerb`.

🔴 **`resumptionToken` lekur milli setta.**
Ganga um `set=type:baer` skilaði bókum á síðustu tveimur síðunum. Sá sem treystir
settinu fær rangt mengi.

🔴 **Sett eru auglýst en tóm.**
`ListSets` auglýsti `era:19c`; `ListRecords` á því skilaði `noRecordsMatch`.

🔴 **`adminEmail` vantar.**
Þá er enginn til að skrifa þegar eitthvað bilar. Staðallinn krefst þess.

### 1.3 Umfang og stöðugleiki

- **Varanleg auðkenni.** `oai:safn.is:hlutur:123` má aldrei fá nýja merkingu.
  Ef auðkenni breytast við hverja endurhleðslu safnast tvítök hjá okkur.
- **Eyddar færslur.** `deletedRecord: persistent` er best — þá vitum við hvað á
  að hverfa. `transient` eða `no` þýðir að við verðum að lesa allt upp á nýtt.
- **Dagstimplar sem breytast.** `datestamp` á að breytast þegar færslan breytist,
  ekki við hverja endurbyggingu.

---

## 2. Dublin Core — reitirnir

**M** = skylda · **R** = ráðlagt · **O** = valkvæmt

| Reitur | | Fjöldi | Regla |
|---|---|---|---|
| `dc:title` | **M** | 1 | `xml:lang="is"`. Aldrei tómur |
| `dc:identifier` (slóð) | **M** | 1 | varanleg slóð í ykkar kerfi — verður tengillinn „Skoða hjá útgefanda" |
| `dc:identifier` (auðkenni) | R | 0..1 | safnmark eða OAI-auðkenni, mannlesanlegt |
| `dc:identifier` (smámynd) | **R** | 0..1 | bein myndslóð — það sem gerir færsluna að mynd en ekki gráum kassa í niðurstöðulistanum |
| `dc:type` | **M** | 2 | **par**: `@is` og `@en`. Enska gildið stýrir flokkuninni |
| `dc:subject` | **M** | 1..n | efnisorð, hreint gildi, `@is` ef íslenskt |
| `dc:coverage` / `dcterms:spatial` | **R** | 0..n | staður, hreint gildi án forskeytis |
| `dc:date` | R | 0..1 | **EDTF**: `1887` eða `1703/1910`. Sjá 2.2 |
| `dc:description` | R | 0..1 | lausamálslýsing eða heildartexti (sjá kafla 5) |
| `dc:creator` | R | 0..n | **manneskja eða stofnun sem bjó hlutinn til** |
| `dc:contributor` | O | 0..n | aðrir sem koma við sögu |
| `dc:publisher` | R | 1 | safnið/útgefandinn eins og það á að birtast |
| `dc:language` | R | 1 | ISO-kóði, `is` |
| `dc:rights` | **R** | 0..1 | leyfisslóð, t.d. `https://creativecommons.org/licenses/by/4.0/` |
| `dcterms:spatial` (hnit) | O | 0..n | `xsi:type="dcterms:Point"`, `POINT(lengd breidd)` |
| `dc:relation` | O | 0..n | slóð á skylda færslu |
| `dc:source` | O | 0..n | heimild. **Aldrei slóð** — slóðir fara í `dc:identifier` |

### 2.1 Hrein gildi — engin forskeyti í texta

❌ `<dc:coverage>Sýsla: Rangárvallasýsla</dc:coverage>`
✅ `<dcterms:spatial xsi:type="mshl:sysla">Rangárvallasýsla</dcterms:spatial>`

Forskeyti í gildinu rata beint í síuna og þá stendur þar
„Sýsla: Rangárvallasýsla" — sem er ólæsilegt og sameinast ekki gildum frá
öðrum söfnum. Flokkunin á heima í eigind (attribute), ekki í textanum.

Sömu reglu fylgir nafnfall: **staðanöfn í nefnifalli**. *Skálholt*, ekki
*Skálholti*. Þágufallsmyndir sameinast ekki nefnifallsmyndum í síu.

### 2.2 Dagsetningar — EDTF

| Það sem sást | Á að vera |
|---|---|
| `1920 - 1925` | `1920/1925` |
| `01.01.1945 - 01.01.1950` | `1945/1950` |
| `um 1696 - 1733` | `dc:date` = `1696/1733` **og** `dcterms:temporal` = `um 1696 - 1733` |
| `None` | reitnum sleppt |

Óvissan er upplýsingar, ekki sóðaskapur — geymið hana, en látið vélræna formið
fylgja með svo hægt sé að raða og sía.

### 2.4 Smámyndin — hvernig myndin kemst í niðurstöðulistann

Færsla með mynd er margfalt gagnlegri en færsla án hennar, og þetta er sá
reitur sem oftast gleymist. **Ef þið eigið mynd af hlutnum, sendið slóðina á
hana með.**

Sarpur gerir þetta og það virkar: **önnur `dc:identifier`-lína með beinni
myndslóð**, aðgreind frá síðuslóðinni á slóðamynstrinu.

```xml
<dc:identifier>https://sarpur.is/en/collection/item/1906282/</dc:identifier>
<dc:identifier>https://sarpur.is/multimedia/1/multimedia-2259821.large.jpg</dc:identifier>
```

Okkar megin les leitarvísirinn þær í sitt hvorn reitinn með tveimur regex-um
á sama `dc:identifier`:

| Linking Parameter | Regex | Skilar |
|---|---|---|
| **1** — tengill | `https://safn\.is/hlutur/.*` | „Skoða hjá útgefanda" |
| **2** — smámynd | `https://safn\.is/.*\.jpg` | myndin á spjaldinu |

Þrjú skilyrði, öll einföld:

- **Bein slóð** á myndskrána sjálfa — endar á `.jpg`, `.png` eða `.webp`.
  Ekki slóð á síðu sem birtir myndina.
- **Opin** án innskráningar, án `Referer`-kröfu og án tímabundins auðkennis.
- **Aðgreinanleg með regex** frá síðuslóðinni. Ólíkt slóðamynstur dugar
  (`/multimedia/` vs `/collection/`), eða bara skráarendingin.

Stærðin skiptir minna máli en aðgengið — leitarvísirinn skalar myndina.
Ef þið eigið bæði smámynd og fulla mynd, sendið **smámyndina**; hún er það
sem birtist í listanum og hún hleðst hraðar.

Ef mynd er ekki til er reitnum einfaldlega sleppt. Hann er ráðlagður, ekki skylda.

### 2.5 Staðanöfn — nefnifall, hnit, eða auðkenni

Þetta er reiturinn sem veldur mestum vandræðum í íslenskum gögnum, og
ástæðan er beyging. Sía er bókstafsjöfnuður: **`Skálholti` sameinast aldrei
`Skálholt`.** Mælt í leitarvísinum 16.9.2026: `Skálholt` skilar 3.032
færslum, `Skálholti` 937 — tvö aðskilin mengi um sama stað.

Við biðjum um eitt af þrennu. **Það efsta sem þið getið skilað.**

| | Hvað | Af hverju |
|---|---|---|
| **1. Best** | **auðkenni staðarins** — t.d. örnefnanúmer eða ykkar eigið varanlega auðkenni | beyging og stafsetning hætta að skipta máli |
| **2. Næstbest** | **hnit** `POINT(lengd breidd)` | leysa bæði beygingu OG stafsetningu. Mælt: `Breiðabólstaður` og `Breiðabólsstaður` reyndust **0,00 km** frá hvor öðrum — nafnapörun féll, hnitin ekki |
| **3. Lágmark** | **nafnið í nefnifalli** — `Þingvellir`, ekki `Þingvöllum` | sameinast öðrum söfnum í síunni |

**Ef heimildin ykkar ber þágufall er það í lagi — skilið því.** Í sögulegum
texta *er* þágufallið heimildin („prestur á Kaldaðarnesi") og við ætlumst
ekki til að þið endurskrifið hana. Sendið þá beygðu myndina og **látið
fylgja hnit eða auðkenni** ef þau eru til.

Okkar megin afbeygjum við það sem við getum: forskrift flettir beygðri mynd
upp í 11.471 bæjarnafni úr Sögulegu mann- og bæjatali. Mælt á Ævum lærðra
manna: **7 % pössuðu óafbeygð, 67 % eftir afbeygingu.** Það sem stóð eftir
var stafsetningarmunur og staðir sem eru ekki bæir — hvorugt leysist með
fleiri málfræðireglum.

**Sendið hvort tveggja ef þið eigið það:** upprunalegu myndina eins og hún
stendur í heimildinni, og nefnifallið. Þá glatast ekkert og sían virkar.

```xml
<dc:coverage xml:lang="is">Kaldaðarnes</dc:coverage>
<dcterms:spatial xsi:type="dcterms:Point">POINT(-20.925 63.925)</dcterms:spatial>
<dcterms:bibliographicCitation xml:lang="is">prestur á Kaldaðarnesi</dcterms:bibliographicCitation>
```

### 2.3 Hreinsun við útgáfu — skylda

- Aldrei strenginn `None`, `null`, `N/A` eða `-` sem gildi. Sleppið reitnum.
- Aldrei tóman reit: `<dc:format></dc:format>` ber engar upplýsingar.
- Aldrei færslu með haus en tómu `<oai_dc:dc/>`.
- Aldrei stýritákn (`\x00`–`\x1f` nema tab/línuskil) — þau brjóta XML hjá
  öllum sem lesa.
- Aldrei `]]>` inni í `CDATA`.
- UTF-8, engin BOM.
- Hnit: `POINT(lengd breidd)` — ekki öfugt. Á Íslandi er lengd neikvæð
  (−25 til −13) og breidd jákvæð (63 til 67). Ein færsla af 6.543 var öfug og
  lenti í Indlandshafi.

---

## 3. Leitaratriðin — það sem við viljum geta spurt um

Hvert atriði er spurning sem notandi spyr. Aftan við hverja er reiturinn sem
svarar henni.

| Spurningin | Reiturinn | Staða í dag |
|---|---|---|
| **Hvað heitir það?** | `dc:title` | ✅ alls staðar |
| **Hvar var það?** | `dcterms:spatial` / `dc:coverage` | ⚠️ ólíkt byggt milli safna |
| **Hvenær?** | `dc:date` (EDTF) | 🔴 ósamræmt; vantar alveg í sumum |
| **Hver kemur við sögu?** | `dc:creator` / `dc:contributor` + hlutverk | ⚠️ hlutverk oftast ósýnileg |
| **Hvers konar hlutur?** | `dc:type` (`@en` stýrir) | ✅ þegar parið fylgir |
| **Um hvað fjallar það?** | `dc:subject` | 🔴 hvert safn með sinn orðaforða |
| **Úr hvaða safni?** | sett í innlestri | ✅ |
| **Hvað stendur í því?** | `dc:description` (heildartexti) | 🔴 aðeins eitt safn skilar honum |

Þrjú síðustu atriðin eru það sem greinir samleit frá þremur aðskildum leitum.

---

## 4. Efnisorð og flokkar — tvö lög

Þetta er eini hluti skjalsins sem biður um meira en staðlað Dublin Core, og
ástæðan er einföld: **orðaforði með hundruðum gilda er ónothæfur sem sía.**

Við viljum tvennt frá hverri gagnaveitu:

**Lag 1 — efnisorð veitunnar.** Ykkar eigin orðaforði, óbreyttur. Hann er
leitanlegur og birtist á spjaldinu.

```xml
<dc:subject xml:lang="is" xsi:type="mshl:efnisord">Huldufólk</dc:subject>
```

**Lag 2 — sameiginlegur efnisflokkur.** Gróf flokkun með ~20 gildum sem öll
söfn deila. Þetta er sían sem fólk smellir á.

```xml
<dc:subject xml:lang="is" xsi:type="mshl:flokkur">Þjóðtrú</dc:subject>
```

Ef þið treystið ykkur ekki til að flokka sjálf, þá skilið lagi 1 og við
kortleggjum í lag 2 — en þá þarf **varanlegt auðkenni á hvert efnisorð**:

```xml
<dc:subject xml:lang="en" xsi:type="mshl:efnisord"
            mshl:id="1000005">elves</dc:subject>
```

Auðkennið er það sem gerir kortlagninguna varanlega. Merkimiðar breytast,
auðkenni eiga ekki að gera það. Ísmús gerir þetta rétt í dag — hvert efnisorð
ber `id="1000005"` — og þess vegna er hægt að þýða orðaforða þeirra einu sinni
og vera búinn.

**Hlutverk fylgi fólki og stöðum.** `Jón Árnason` einn og sér segir ekki hvort
maðurinn sagði söguna eða skrifaði hana niður. Hlutverkið á að fylgja:

```xml
<dc:contributor mshl:role="heimildarmaður">Mikkalína Friðriksdóttir</dc:contributor>
<dc:creator     mshl:role="skrásetjari">Arngrímur Fr. Bjarnason</dc:creator>
```

Sama gildir um staði: staðurinn sem sagan **gerist á** og staðurinn sem hún var
**skráð á** eru ekki sami hluturinn. Annar á heima í staðarsíunni, hinn ekki —
elliheimili í Reykjavík er ekki sögustaður.

---

## 5. Heildartexti

Ef safnið geymir texta — sögu, uppskrift, bréf, lýsingu — þá er hann
verðmætasti hluti afhendingarinnar. Þá fyrst er hægt að leita **í efninu**
en ekki bara í lýsigögnunum um það.

| | Regla |
|---|---|
| **Hvar** | `dc:description` fyrir texta undir ~2.000 stöfum; `dcterms:tableOfContents` eða eigið svið fyrir lengri |
| **Snið** | hreinn texti. Ekki HTML, ekki `<br>`, ekki `&nbsp;` |
| **Línuskil** | mega fylgja, en ekki harðbrotnar línur í miðjum setningum |
| **Tungumál** | `xml:lang` á að vera rétt |
| **Vélþýðingar** | ef þær eru til, þá í eigin reit og merktar sem slíkar — aldrei ofan í frumtextann |
| **Tómt** | ef textinn er ekki til, sleppið reitnum. Ekki `<content></content>` |

---

## 6. Þegar Dublin Core dugar ekki

Meginreglan: **eins mikið og hægt er í stöðluðu Dublin Core; aðlaganir ofan á,
aldrei í staðinn.**

Þrjár leiðir, í forgangsröð:

1. **`dcterms`** — `dcterms:spatial`, `dcterms:temporal`, `dcterms:isPartOf`,
   `dcterms:provenance`, `dcterms:bibliographicCitation`. Staðlað og ókeypis.
2. **`xsi:type`-eigind á staðlaða reiti** — flokkun án þess að brjóta sniðið.
   Sá sem les venjulegt `oai_dc` fær gildið; sá sem skilur eigindina fær
   flokkunina líka.
3. **Eigið `metadataPrefix`** við hlið `oai_dc` — t.d. ISEBEL-snið Ísmús eða
   MARC. Þá fáum við ríkari gögn, **en `oai_dc` verður samt að vera til**.

Það sem á **ekki** að gera: setja flokkun í textann (`Sýsla: …`), pakka mörgum
upplýsingum í einn streng (`Heimili: Skálholt, Skálholtssókn, Biskupstungnahreppur,
Árnessýsla`), eða skilgreina eigin reiti inni í `oai_dc`-nafnrýminu.

---

## 7. Gátlisti fyrir afhendingu

Endapunkturinn:

- [ ] `Identify` svarar og `baseURL` þar virkar orðrétt
- [ ] `adminEmail` er til staðar
- [ ] GET og POST virka bæði
- [ ] `ListMetadataFormats` auglýsir `oai_dc`
- [ ] `ListRecords` gengur á enda og talan stemmir við `completeListSize`
- [ ] `from`/`until` sía raunverulega
- [ ] Auglýst sett eru ekki tóm og leka ekki hvert í annað
- [ ] Ein skemmd færsla fellir ekki heildina

Færslurnar:

- [ ] `dc:title`, `dc:identifier` (slóð), `dc:type` (par) á öllum færslum
- [ ] `dc:subject` og staðarreitur á öllum sem geta borið þá
- [ ] Engin `None`, engir tómir reitir, engin stýritákn
- [ ] Dagsetningar á EDTF
- [ ] Hnit `POINT(lengd breidd)`, öll innan raunhæfra marka
- [ ] Staðanöfn í nefnifalli — eða beygð mynd með hnitum eða auðkenni. Án forskeytis
- [ ] Slóðirnar svara 200 — ekki 302 á forsíðu
- [ ] Smámyndaslóð með þar sem mynd er til — bein, opin, aðgreinanleg með regex
- [ ] `dc:rights` segir hvað má

---

## 8. Hvað gerum við við þetta

Gögnin fara í gegnum normaliseringarreglur inn í Gegni og verða leitanleg í
Leitir.is við hliðina á öðrum söfnum. Hver færsla ber tengil heim í kerfið
ykkar — við geymum lýsigögnin, ekki hlutina sjálfa, og umferðin endar hjá ykkur.

Ef eitthvað í þessu skjali er óframkvæmanlegt hjá ykkur skiptir mestu að við
vitum af því. Það er hægt að vinna með gögn sem vantar reiti; það er miklu
erfiðara að vinna með gögn þar sem reitur er til en þýðir eitthvað annað en
hann segist þýða.

---

*Mælt á Sarpi, Sögulegu mann- og bæjatali, Handriti.is, jarðaskrá Þjóðskjalasafns,
Ævum lærðra manna og Ísmús/Sagnagrunni, maí–september 2026.*

# Gullna sniðið

**Kanónískt `oai_dc`-snið fyrir samleit íslenskra menningarsafna**
Útgáfa 1.0 · 16. september 2026 · Miðstöð stafrænna hugvísinda og lista

Kröfur til afhendingarinnar sjálfrar — endapunktur, uppskera, gátlisti — eru í
[`../oai-pmh/LEIDBEININGAR.md`](../oai-pmh/LEIDBEININGAR.md). Þetta skjal lýsir
sniðinu sem gögnin eiga að vera komin á þegar þau fara inn í leitarvísinn.
Útfærslan — hvaða PNX-svið hver reitur lendir í — er í
[`svid-og-eigindir.md`](svid-og-eigindir.md); heilar færslur í [`daemi/`](daemi/).

## 1. Hvað þetta er

Eitt snið sem öll söfn eru þýdd yfir í. Hvert safn heldur sínum gögnum og sínu
viðmóti; við sækjum lýsigögnin og samræmum þau. Ástæðan er ekki snyrtimennska:
sía og leit virka aðeins **þvert á söfn** ef sömu upplýsingar liggja í sama
reit með sama lagi á gildinu. Sniðið er staðlað Dublin Core með `dcterms`-viðbót
og `xsi:type`-eigindum — aldrei eigin reitir inni í `oai_dc`-nafnrýminu.

## 2. Reitatafla

**M** = skylda · **R** = ráðlagt · **O** = valkvæmt.
Fjöldi: `1` nákvæmlega eitt · `0..1` núll eða eitt · `1..n` eitt eða fleiri ·
`0..n` núll eða fleiri.

| Reitur | Skylda | Fjöldi | Tungumál | Regla |
|---|---|---|---|---|
| `dc:title` | **M** | 1 | `xml:lang="is"` | Aðaltitill. Aldrei tómur |
| `dc:identifier` (slóð) | **M** | 1 | — | Varanleg slóð í upprunakerfi; verður tengillinn heim |
| `dc:identifier` (auðkenni) | R | 0..1 | — | Safnmark eða OAI-auðkenni, mannlesanlegt |
| `dc:type` | **M** | 2 (par) | **bæði** `@is` og `@en` | Hvers konar hlutur. Enska gildið stýrir flokkuninni |
| `dc:subject` | **M** | 1..n | `@is` (`@en` má fylgja) | Efni. Samleitarlykill #1. Hreint gildi |
| `dc:subject` (efnisflokkur) | R | 0..n | `@is` | `xsi:type="mshl:flokkur"` — grófa sían, sjá kafla 4 í LEIDBEININGAR |
| `dcterms:spatial` eða `dc:coverage` (staður) | R | 0..n | `@is` | Staður. Samleitarlykill #2. Stig í `xsi:type`, ekki í textanum |
| `dcterms:spatial` (hnit) | O | 0..1 | — | `xsi:type="dcterms:Point"`, `POINT(lengd breidd)`. Aldrei `None` |
| `dc:date` | R | 0..1 | — | EDTF: `1887` eða `1703/1920` |
| `dcterms:temporal` | O | 0..n | `@is` | Tímabil eins og það stendur í heimild (`mshl:manntal`, `mshl:timabil`, `mshl:um`) |
| `dc:description` | R | 0..1 | `@is` | Lausamálslýsing eða heildartexti. Hreinn texti, ekkert HTML |
| `dc:creator` | R | 0..n | — | Manneskja eða stofnun sem bjó hlutinn til. Hlutverk í `mshl:role` |
| `dc:contributor` | O | 0..n | — | Aðrir sem koma við sögu. Hlutverk í `mshl:role` |
| `dc:publisher` | R | 1 | `@is` | Safnið eins og það á að birtast |
| `dc:language` | R | 1 | — | ISO-kóði, `is` |
| `dc:rights` | R | 0..1 | — | Leyfisslóð, t.d. `https://creativecommons.org/licenses/by/4.0/` |
| `dcterms:relation` | O | 0..n | — | Slóð á skylda færslu, eða nafn með `xsi:type="mshl:folk"` |
| `dcterms:isPartOf` | O | 0..1 | `@is` | Yfirheild — bindi, safn, skrá |
| `dcterms:hasPart` | O | 0..n | `@is` | Undireiningar; `xsi:type="mshl:verk"` fyrir verk í handriti |
| `dcterms:provenance` | O | 0..1 | `@is` | Varðveislustofnun |
| `dcterms:bibliographicCitation` | O | 0..1 | `@is` | Læsileg tilvísun; einnig notuð fyrir hlutverkastreng fólks |
| `dc:source` | O | 0..n | — | Heimild. **Aldrei slóð** — slóðir fara í `dc:identifier` |
| `dc:format` | O | 0..n | `@is` | Efni eða mál. Aldrei tómur |

Færsla án **M**-reits telst ekki gullsamhæf. Reitur sem er til en ber ekkert
gildi er verri en reitur sem vantar — sjá kafla 6.

## 3. Annótað dæmi

Raunfærsla úr [`../../leidarljos/dc-template/gold/test-record-baer-1250-v2.xml`](../../leidarljos/dc-template/gold/test-record-baer-1250-v2.xml),
stytt á tveimur stöðum.

```xml
<oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
           xmlns:dc="http://purl.org/dc/elements/1.1/"
           xmlns:dcterms="http://purl.org/dc/terms/"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xmlns:mshl="https://mshl.is/terms#">
  <dc:identifier>oai:smb.mshl.is:baer:1250</dc:identifier>      <!-- R  auðkenni -->
  <dc:identifier>https://smb.mshl.is/baer/1250</dc:identifier>  <!-- M  tengill heim -->
  <dc:title xml:lang="is">Drangshlíð</dc:title>                 <!-- M  alltaf @is -->
  <dc:type xml:lang="is">Bær</dc:type>                          <!-- M  parið: @is -->
  <dc:type xml:lang="en">Place</dc:type>                        <!-- M  og @en, sem stýrir -->
  <dc:subject xml:lang="is">Bær</dc:subject>                    <!-- M  samleitarlykill #1 -->
  <!-- samleitarlykill #2: eitt stig á reit, hreint gildi, stigið í eigindinni -->
  <dcterms:spatial xsi:type="mshl:sokn" xml:lang="is">Eyvindarhólasókn</dcterms:spatial>
  <dcterms:spatial xsi:type="mshl:sokn" xml:lang="is">Skógasókn</dcterms:spatial>
  <dcterms:spatial xsi:type="mshl:hreppur" xml:lang="is">Austur-Eyjafjallahreppur</dcterms:spatial>
  <dcterms:spatial xsi:type="mshl:sysla" xml:lang="is">Rangárvallasýsla</dcterms:spatial>
  <!-- hnit: lengd á undan breidd; á Íslandi er lengdin neikvæð -->
  <dcterms:spatial xsi:type="dcterms:Point">POINT(-19.5519958640946 63.5259866407141)</dcterms:spatial>
  <dcterms:temporal>1703/1920</dcterms:temporal>                <!-- vélrænt bil -->
  <dcterms:temporal xsi:type="mshl:manntal" xml:lang="is">1703</dcterms:temporal>
  <dcterms:temporal xsi:type="mshl:manntal" xml:lang="is">1729</dcterms:temporal>
  <!-- … 18 manntalsár til viðbótar, hvert á sínum reit, hrein ártöl … -->
  <dc:date>1703/1920</dc:date>                                  <!-- R  EDTF -->
  <dc:description xml:lang="is">Drangshlíð í Sögulegu mann- og bæjatali</dc:description>
  <dc:language>is</dc:language>                                 <!-- R -->
  <dc:publisher xml:lang="is">Sögulegt mann- og bæjatal (SMB)</dc:publisher>
  <dc:rights>https://creativecommons.org/licenses/by/4.0/</dc:rights>
  <!-- creator/contributor viljandi sleppt: staðir hafa engan höfund -->
</oai_dc:dc>
```

## 4. Tveir samleitarlyklar: EFNI og STAÐUR

Titlar sameinast ekki milli safna. „Skólastóll“ og „SÁM 88/1559 EF“ eiga ekkert
sameiginlegt þótt hluturinn sé frá sama bæ. Tvennt sameinast:

**EFNI — `dc:subject`.** Það sem hluturinn fjallar um, ekki það sem hann er.
Ljósmynd af bæ og bærinn sjálfur bera bæði efnið `Bær`; þjóðsaga og hljóðrit
bera bæði `Huldufólk`. Þess vegna er `dc:subject` skylda þótt gildið endurtaki
titilinn.

**STAÐUR — `dcterms:spatial` / `dc:coverage`.** Örnefni eru stöðug í gegnum aldir
og þvert á söfn. Hnitin gera kort mögulegt; nafnið gerir síuna mögulega.

Þess vegna standa og falla samleitin með þessum tveimur. Öll hin sviðin gera
færsluna læsilega; þessi tvö gera hana **samleitanlega**. Færsla sem ber hvorugt
er fullgild Dublin Core-færsla og um leið ósýnileg í samleitinni.

## 5. Tvö lög á tegund

Tegundin er skráð tvisvar, viljandi. `resourceType` er naumur, fastur
Primo-flokkur sem stýrir íkonum og efstu síunni; `local2` ber ríku
menningarflokkunina. Bæði eru leidd af enska `dc:type`-gildinu.

| Gagnaveita | `dc:type` `@en` | `local2` (rík tegund) | `resourceType` (Primo-flokkur) |
|---|---|---|---|
| SMB, Jarðaskrá | `Place` | `place` | `places` |
| SMB, Ævir lærðra manna | `Person` | `person` | `people` |
| Ævir lærðra manna | `Volume` | `volume` | `books` |
| Jarðaskrá | `Register` | `register` | `books` |
| Handrit.is | `Manuscript` | `manuscript` | `manuscripts` |
| Ísmús og Sagnagrunnur | `Legend` | `legend` | `other` |
| Ísmús og Sagnagrunnur | `SoundRecording` | `recording` | `audio` |
| Sarpur | `Photography`, `Drawing`, `Art` | `image`, `drawing`, `artwork` | `images` |
| Sarpur | `Book / Archive` | `book` | `books` |
| Sarpur | `Artifact`, `Coin`, `House`, `Archaeology Remain`, `Mineralogy / Petrology`, `Archaeology`, `Folk Customs Response` | `object`, `coin`, `house`, `ruin`, `rock`, `archeologicalFind`, `ethnology` | `other` |

Gildi sem hittir ekki á neitt fellur í `other` í báðum lögum. Það þýðir að ný
tegund týnist ekki, en hún sameinast heldur engu — orðaforðinn þarf yfirferð
þegar gagnaveita bætist við.

## 6. Hreinlætisreglur

Fullur gátlisti er í [`../oai-pmh/GATLISTI.md`](../oai-pmh/GATLISTI.md). Það sem
sniðið krefst umfram staðlað XML:

- **Engin `None`.** Hvorki `null`, `N/A` né `-`. Reitnum er sleppt í staðinn.
- **Engir tómir reitir.** `<dc:format></dc:format>` ber engar upplýsingar.
  Engin færsla með haus en tómu `<oai_dc:dc/>`.
- **Engin stýritákn** (`\x00`–`\x1f` nema tab og línuskil) og ekkert `]]>`
  inni í `CDATA`. Hvort tveggja fellir uppskeruna hjá öllum sem lesa.
- **Hnit á sniðinu `POINT(lengd breidd)`** — lengdin fyrst. Á Íslandi er lengd
  neikvæð og breidd jákvæð.
- **Staðanöfn í nefnifalli.** *Skálholt*, ekki *Skálholti*; þágufallsmyndir
  sameinast ekki nefnifallsmyndum í síu.
- **Engin forskeyti í gildum.** `Rangárvallasýsla`, ekki `Sýsla: Rangárvallasýsla`.
  Flokkunin á heima í `xsi:type`-eigindinni. Forskeytið rataði beint í síuna og
  kostaði auk þess eina normaliseringarreglu á hverja vísitölu — sjá
  [`svid-og-eigindir.md`](svid-og-eigindir.md).
- **UTF-8, engin BOM.** Skráin skal standast `xmllint --noout`.

## 7. Það sem er enn óákveðið

Fjögur atriði eru **ekki ákveðin**. Reglusett mega ekki treysta á neina
tiltekna lausn á þeim.

**7.1 Staðarbyggingin er ólík milli safna.** SMB-bæir bera hreint stigveldi
(sókn, hreppur, sýsla); SMB-einstaklingar bera öll stigin í einum streng;
Sarpur ber eitt heimilisfang í einum streng; Ísmús ber flöt örnefni án stigs;
Ævir ber staðarnafn í þágufalli. Þetta þarf að lenda í **sama** staðarsviði til
að sían virki þvert á söfn. Tvær leiðir hafa verið nefndar — þátta strengina í
stigveldið, eða halda einu flötu staðarnafnssviði sem allir fæða. **Óákveðið.**

**7.2 EDTF-samræming.** Sniðið krefst EDTF, en gagnaveiturnar eru ekki komnar
þangað: SMB og Jarðaskrá skila bili, Sarpur skilar frjálsu sniði
(`1920 - 1925`, `01.01.1945 - 01.01.1950`), og Ísmús hefur **ekkert**
dagsetningarsvið í sínu sniði. Tíma-sía og tímaröðun bíða þess að þetta
samræmist. **Óákveðið hvenær og hjá hverjum umbreytingin er gerð.**

**7.3 Orðaforði `resourceType`.** Taflan í kafla 5 er samsett úr gildandi
reglusettum, ekki úr stýrðri skrá sem allir kortleggja í. Sama fyrirbæri getur
enn lent á tveimur gildum (bær í Sarpi og bær í SMB eiga sömu tegund en ólík
íslensk heiti). Hvort `place` og `person` eigi að vera eigin Primo-flokkar eða
falla í `other` er sömuleiðis óútkljáð. **Óákveðið.**

**7.4 Númer local-sviðanna.** MSHL-blokkin 36–44 var skilgreind í júlí 2026 en
er horfin úr Alma NZ (staðfest 1.9.2026). Gögnin eru á meðan í sviðum sem bera
villandi samsteypu-merkimiða. Hvaða svið verða endanleg heimkynni staðarstiganna
er **óákveðið** — sjá [`svid-og-eigindir.md`](svid-og-eigindir.md).

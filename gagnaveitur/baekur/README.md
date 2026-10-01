# Bækur.is

Stafrænar bækur Landsbókasafns Íslands – Háskólabókasafns: prentaðar bækur
frá 16. öld til okkar daga, myndaðar síðu fyrir síðu. Bækur.is á opna OAI-PMH
gagnaveitu. Í henni er hver færsla **ein bók**. Við færum bækurnar í gullna
sniðið, bjóðum þær sem sýnisveitu og lesum þær inn í Alma.

## Afhending

| | |
|---|---|
| Endapunktur | `https://baekur.is/oai` — án skástriks |
| `baseURL` í `Identify` | `http://baekur.is/oai`, sem vísar með 301 á https. POST svarar 403 |
| Snið | `edm` (notað hér) og `oai_dc` |
| Sett | engin |
| Eyddar færslur | `deletedRecord=no` |
| `earliestDatestamp` | `1540-01-01T00:00:00Z` — elsta útgáfuárið, ekki elsti dagstimpillinn (hann er frá 2011) |
| `adminEmail` | kristinn@landsbokasafn.is |
| Umfang | 2.984 bækur, 25 á síðu, 120 síður með `resumptionToken`. Um 10 mínútur með 1 s bið milli síðna |
| Umbreyting | [`byggja_baekur_dc.py`](byggja_baekur_dc.py) — sækir, umbreytir, sannprófar |
| Afurð | [`BAEKUR-tryA.xml`](BAEKUR-tryA.xml) — 2.984 færslur, 6,2 MB, fyrir `Upload File/s` í Alma |
| Reglusett | [`BAEKUR_XML_Processes.drl`](BAEKUR_XML_Processes.drl) — 19 reglur |
| Innlestur | [`PLAYBOOK-innlestur.md`](PLAYBOOK-innlestur.md) |
| Sýnisveita | `https://oai.kann.is/baekur` eftir næstu uppsetningu Gáttagægis |

Allar tölur mældar 1.10.2026.

**Hvers vegna `edm` en ekki `oai_dc`?** `oai_dc` setur höfund og ár í einn
streng („Jón Þorkelsson Vídalín 1666 - 1720“), útgáfuárið á ensku („Published
in 1750“) og tungumálið á ISO 639-2. Þar er hvorki land, mynd, réttindi né
tilvísun í Bókaskrá. `edm` ber þetta allt, hvert í sínum reit.

## Umfang

| | Bækur |
|---|---:|
| Allar | 2.984 |
| Með útgáfuári | 2.979 |
| Með efnisorðum frá Bækur.is | 2.448 |
| Með höfundi (manneskju) | 2.474 |
| Með stofnun | 326 |
| Með samræmdum titli (verki) | 295 |
| Án fólks, stofnunar og verks | 224 |
| Með útgáfulandi | 2.679 |

Útgáfuár: 16. öld 29 · 17. öld 210 · 18. öld 696 · 19. öld 1.472 ·
20. öld 550 · 21. öld 22.

Tungumál: íslenska 2.093 · danska 435 · latína 177 · enska 95 · sænska 68 ·
þýska 58 · franska 25 · norska 21 · hollenska 5 · gríska 2 · norskt bókmál,
eistneska, finnska, grænlenska og ítalska 1 hver.

## Kortlagning í gullna sniðið

| Gullið DC | Úr Bækur.is (`edm`) | Athugasemd |
|---|---|---|
| `dc:identifier` (slóð) | `edm:isShownAt` `http://baekur.is/bok/<uuid>/<nafn>` | fer út sem `https://baekur.is/bok/<uuid>`; sjá „Slóðirnar“ |
| `dc:identifier` (smámynd) | `edm:object` `http://baekur.is/cover/<uuid>` | fer út sem `https://baekur.is/cover/tbn/<uuid>`; sjá „Slóðirnar“ |
| `dc:identifier` (auðkenni) | OAI-auðkennið `oai:baekur.is:books/<uuid>` | kemur á eftir slóðunum |
| `dc:title` `@is` | `dc:title` | ISBD-tákn aftast tekin af (23 titlar): „Íslenzk list =“ → „Íslenzk list“. Alltaf `@is` eins og gullna sniðið krefst, líka á dönskum og latneskum titlum |
| `dc:type` (par) | fast: `Bók` `@is` + `Text` `@en` | `Book` og `TEXT` úr heimildinni falla niður. `Text` → `local2` book, `resourceType` books |
| `dc:date` | `dc:date` | ártal, EDTF. Fimm bækur án árs |
| `dc:subject` `@is` | `dc:subject` `@is` | óbreytt, í íslenskri stafrófsröð. Fast `Bækur` bætist aftast á allar |
| `dcterms:spatial` `xsi:type="mshl:land"` `mshl:role="útgáfustaður"` `@is` | `dcterms:spatial` (LoC-landakóði + GeoNames) | aðeins þar sem bæði segja sama land; sjá „Landið“ |
| `dc:creator` `mshl:role="höfundur"` | `dc:creator` → `edm:Agent` (manneskja) | „Hallgrímur Pétursson (1614-1674)“ þegar bæði ár eru skráð; sjá „Fólk, stofnanir og verk“ |
| `dcterms:bibliographicCitation` `@is` | sama | „Hallgrímur Pétursson (1614-1674) (höfundur)“ — fyrir hlutverkasíuna (`local75`), eins og hjá RÚV |
| `dc:contributor` | `dc:creator` → `edm:Agent` (stofnun) | án hlutverks og án ára |
| `dcterms:hasPart` `xsi:type="mshl:verk"` `@is` | `dc:creator` → `edm:Agent` (samræmdur titill) | „Eddukvæði.“ → „Eddukvæði“ |
| `dcterms:extent` `@is` | `dcterms:extent` „730 p.“ | „730 síður í stafrænu eintaki“; sjá „Umfangið“ |
| `dc:language` | `dc:language` | ISO 639-1 þegar í heimildinni |
| `dc:publisher` `@is` | fast | Landsbókasafn Íslands – Háskólabókasafn (`edm:dataProvider` er á ensku) |
| `dc:rights` (tvisvar) | `edm:rights` | heitið á íslensku `@is` og slóð yfirlýsingarinnar; sjá „Réttindin“ |
| `dcterms:isReferencedBy` (par) | `dcterms:isReferencedBy` | „Bókaskrá Landsbókasafns“ + `https://bokaskra.landsbokasafn.is/search?s_any=<MMS-auðkenni>` (http → https) |
| `datestamp` | `datestamp` | óbreyttur, svo `from`/`until` virka í sýnisveitunni |
| `setSpec` | fast `source:baekur` | |
| — | `edm:type`, `edm:Place`, `edm:WebResource`, `edm:provider` | falla niður. Landið er lesið úr `dcterms:spatial` |

### Slóðirnar

**Slóðin heim.** `https://baekur.is/bok/<uuid>` svarar 200. Í heimildinni fylgir
nafnhluti (`/bok/<uuid>/Biblia`) og `http://`, sem vísar með 301 á https.
Bækur.is gefur sjálf slóðina án nafnhlutans sem `url` í schema.org-lýsingu
bókarsíðunnar. Hún breytist ekki þótt titli sé breytt. Mælt á 24 bókum af
handahófi: allar svara 200.

**Smámyndin.** Þrjár slóðir komu til greina:

| Slóð | Hvað hún er | Mat |
|---|---|---|
| `https://baekur.is/cover/<uuid>` (`edm:object`) | 302 á mynd í fullri stærð, 2.468 × 3.132 px, 280 kB | of stór fyrir niðurstöðulista |
| `https://baekur.is/cover/tbn/<uuid>` | 302 á smámynd, 200 px á breidd, 4–14 kB | **valin** |
| `https://baekur.is/skra/JPG/<n>` | myndskráin sjálf, svarar 200 | `<n>` er innra skráarnúmer og breytist ef bókin er mynduð aftur |

`/cover/tbn/<uuid>` er `thumbnailUrl` bókarsíðunnar og sama slóð og Bókaskrá
Landsbókasafns notar fyrir smámyndir. Hún byggir á sama auðkenni og bókin.
Gallinn er að hún endar ekki á `.jpg` og svarar 302. Vafri eltir 302 þegar
hann sækir mynd; hvort Primo gerir það er óstaðfest. Gáttagægir sá hana ekki
sem mynd fyrr en athugun F07 var látin þekkja `/cover/` (sérstök breyting á
Gáttagægi sem bíður samþykkis). Mælt á 24 bókum: allar smámyndir skila `image/jpeg`.
Myndin er af fyrstu blaðsíðu bókarinnar, ekki bandinu.

### Fólk, stofnanir og verk

Bækur.is setur alla sem tengjast bók í `dc:creator` og merkir þá alla
„Höfundur“ á bókarsíðunni. Í straumnum eru 1.644 slíkir „höfundar“ á 2.760
bókum. Þeir eru af þrennu tagi:

| | Ólík nöfn | Bækur | Dæmi | Í gullna sniðinu |
|---|---:|---:|---|---|
| Manneskjur | 1.305 | 2.474 | Hallgrímur Pétursson, „Luther, Martin“ | `dc:creator` + hlutverk + `bibliographicCitation` |
| Stofnanir, lönd og sýningar | 68 | 326 | Ísland (198 bækur, flestar tilskipanir), Hið íslenska bókmenntafélag, Septembersýningin | `dc:contributor` |
| Samræmdir titlar | 123 | 295 | Eddukvæði, Sálmabók, Biblían, Graduale, Njáls saga | `dcterms:hasPart` `mshl:verk` |

Flokkunin er vélræn, í þessari röð:

1. **Stofnun** ef nafnið er á lista (Ísland, Danmörk …) eða ber orð eins og
   félag, safn, sjóður, nefnd, skóli eða sýning.
2. **Manneskja** ef æviár eru skráð eða nafnið er öfugt með kommu
   („Luther, Martin,“).
3. **Verk** ef nafnið er saga, þáttur, kvæði eða lögbók, eða endar á punkti
   („Eddukvæði.“, „Graduale.“).
4. Annars **manneskja** („Jón Einarsson“, „Laozi“).

Forritið prentar allar stofnanir og öll verk við hverja keyrslu. Nöfnin 407
sem bera engin æviár voru lesin yfir 1.10.2026.

„Ísland“ er höfundur laga og tilskipana, eins og í Gegni. Það lendir því í
fólkssíunni (`local49`) með 198 bækur. „Biblían“ er ekki höfundur Biblíunnar;
hún verður verk sem bókin geymir.

**Æviár** fylgja nafninu aðeins þegar bæði fæðingar- og dánarár eru skráð:
1.088 manneskjur af 1.644 „höfundum“, 4.196 af 4.669 tengingum manneskja við
bók. Fæðingarár eitt og sér fer ekki út. 139 manneskjur hafa aðeins
fæðingarár, flestar fæddar eftir 1930 og sumar líklega á lífi. Sama regla og
hjá RÚV. Æviárin greina líka að nafna: Hallgrímur Pétursson (1614-1674) á 73
bækur, Hallgrímur Pétursson (1875-1937) eina.

**Greinarmerki** úr bókfræðifærslunni falla af: „Luther, Martin,“ →
„Luther, Martin“ (380 nöfn enda á kommu). Punktur aftast helst á manneskjum,
því hann er oft upphafsstafur („Ferrall, J. S.“).

**Hlutverkið „höfundur“ er ekki alltaf rétt.** Straumurinn segir ekki hver
skrifaði, hver þýddi og hver prentaði. Við förum eftir bókarsíðunni.
Guðmundur Jónsson Skagfjörð er „höfundur“ 132 bóka og 124 þeirra bera efnisorð
prentsmiðju (Leirárprent, Viðeyjarprent …). Marteinn Arnoddsson á 57 bækur,
allar merktar Hólaprenti. Þeir eru líklega prentarar. Sjá spurningu 4.

### Landið

Bækur.is gefur útgáfulandið tvisvar á hverri bók: sem landakóða Library of
Congress (MARC: `ic`, `dk` …) og sem GeoNames-auðkenni. Við skráum landið
aðeins þegar bæði segja sama land.

| | Bækur |
|---|---:|
| Bæði segja sama land | 2.679 |
| LoC `null` (296) eða `xx` (5): landið óþekkt, en GeoNames segir Ísland | 301 |
| LoC `ge`, `meu` og `sk`, en GeoNames segir Ísland | 3 |
| LoC `sc` og GeoNames Saint-Barthélemy: ferðasaga frá 1881, líklega rangur kóði | 1 |

Löndin: Ísland 1.376 · Danmörk 987 · Þýskaland 80 · Svíþjóð 71 · Bretland 69 ·
Noregur 36 · Frakkland 20 · Bandaríkin 10 · Holland 7 · Kanada 6 · Finnland 5 ·
Sviss 3 · Austurríki 3 · Ítalía 2 · Pólland 2 · Írland 2. England (`enk`),
Skotland (`stk`) og Bretland (`xxk`) verða öll „Bretland“, eins og í GeoNames.

**Hvers vegna ekki Ísland á 301 bók?** Þar sem landakóðann vantar setur
Bækur.is GeoNames-auðkenni Íslands. Bækurnar 296 með `null` fá heldur enga
`edm:Place`-einingu. Ísland er þar sjálfgefið gildi, ekki upplýsing. Með því
yrðu 1.680 bækur íslenskar að útgáfu en ekki 1.376.

**Útgáfuland, ekki sögustaður.** Landakóðinn er útgáfuland bókarinnar
(MARC 008). Bók prentuð í Kaupmannahöfn fær „Danmörk“, hvað sem hún fjallar
um. Þess vegna ber reiturinn `mshl:role="útgáfustaður"`. Stigið er í
`xsi:type="mshl:land"`, nýrri eigind sem bætist við
[`svid-og-eigindir.md`](../../snidmat/svid-og-eigindir.md). Í Leitum lendir
landið samt í sömu staðarsíu (`local22`) og sögustaðir annarra safna.

**Prentsmiðjur benda á stað, en við bætum honum ekki við.** 747 bækur bera
efnisorð prentsmiðju: Hólaprent 354, Viðeyjarprent 209, Leirárprent 75,
Hrappseyjarprent 53, Skálholtsprent 43, Beitistaðaprent 13, Núpufellsprent 2.
Hólaprent þýðir að bókin var prentuð á Hólum í Hjaltadal. Við setjum samt
ekki „Hólar“ í staðarreit; það væri okkar ályktun, ekki gögn Bækur.is. Það má
gera sem sérstaka, skráða reglu (prentsmiðja → prentstaður) ef þess er óskað.
Bókaskrá Landsbókasafns sýnir þegar „Bækur eftir útgáfustað“ með hnitum; sjá
spurningu 5.

### Umfangið

„730 p.“ er fjöldi mynda í stafræna eintakinu, ekki blaðsíðutal bókarinnar.
Biblía frá 1859 ber „1122 p.“ í straumnum, en bókarsíðan segir „Blaðsíður
1118“. Munurinn er band, saurblöð, kjölur og litaspjald. Við skrifum því
„730 síður í stafrænu eintaki“ en ekki „730 bls.“, sem yrði lesið sem
blaðsíðutal prentuðu bókarinnar. Tala sem endar á 1 fær eintölu: „21 síða“, en „11 síður“.

### Réttindin

| `edm:rights` | Bækur | Í gullna sniðinu |
|---|---:|---|
| `http://rightsstatements.org/page/InC/1.0/` | 2.982 | „Höfundarréttur í gildi“ + `http://rightsstatements.org/vocab/InC/1.0/` |
| `https://creativecommons.org/publicdomain/mark/1.0/` | 2 | „Almenningseign“ + sama slóð |

`page`-slóðin er síða ætluð fólki. `vocab`-slóðin er auðkenni yfirlýsingarinnar
og vísar á síðuna.

**InC er nær örugglega sjálfgefið gildi.** 2.406 bækur prentaðar fyrir 1900 eru
merktar „höfundarréttur í gildi“, 935 þeirra fyrir 1800. Þar á meðal eru
sálmar Hallgríms Péturssonar (d. 1674). Aðeins tvær bækur eru merktar
almenningseign: Stúlka eftir Júlíönu Jónsdóttur (1876) og Kviðlingar eftir
Káin (1920). Við flytjum yfirlýsinguna óbreytta, því Bækur.is á hana. Sjá
spurningu 1.

## Mælt með Gáttagægi

Sama athugun á endapunkti Bækur.is og á sýnisveitunni (1.10.2026).
Gáttagægir prófar `oai_dc`-snið endapunktsins; `edm`, sem við notum, er ríkara.

| | `https://baekur.is/oai` | Sýnisveitan |
|---|---:|---:|
| Villur | 6 | 0 |
| Aðvaranir | 3 | 0 |
| Ábendingar | 4 | 1 |
| Stóðst | 28 | 42 |
| Sleppt | 4 | 2 |

Sýnisveitan er mæld með F07-breytingunni á Gáttagægi. Án hennar: 2 ábendingar
og 41 stóðst, því smámyndin sést þá ekki.

Það sem sýnisveitan lagar:

| Athugun | Bækur.is | Sýnisveitan |
|---|---|---|
| E02 `baseURL` virkar orðrétt | auglýst `http://` svarar 301 | ✅ |
| E03 GET og POST | POST svarar 403 | ✅ |
| H01 gilt XML | 403-svarið við POST er HTML | ✅ |
| F03 slóðin svarar 200 | `http://` svarar 301 | ✅ `https://baekur.is/bok/<uuid>` |
| F04 `dc:type` sem par | `text` án `xml:lang` | ✅ `Bók` / `Text` |
| F05 `dc:subject` | 73 % í sýninu | ✅ á öllum |
| F06 staðarreitur | enginn | ✅ útgáfuland á 2.679 bókum |
| F08 `dc:rights` | vantar | ✅ |
| F10 `dc:publisher` | vantar | ✅ |
| F07 smámynd | engin | ✅ `/cover/tbn/<uuid>` |
| G07 hlutverk fylgja fólki | ekkert | ✅ `höfundur` |
| E06 `deletedRecord` | `no` | ✅ `persistent` |

Það sem eftir stendur:

| Athugun | Alvarleiki | Hvers vegna |
|---|---|---|
| G06 auðkenni efnisorða | ábending | efnisorð Bækur.is bera ekkert auðkenni |

## Það sem er veikt

- **Staðurinn er aðeins land.** Útgáfustaðurinn sjálfur (Hólar, Viðey,
  Kaupmannahöfn) er ekki í straumnum, og 305 bækur fá ekkert land.
- **Réttindin eru sjálfgefin.** „Höfundarréttur í gildi“ á 2.982 bókum, líka
  á bókum frá 16. öld.
- **Hlutverk vantar.** Höfundur, þýðandi, útgefandi og prentari eru allir
  „höfundar“.
- **Engin varanleg auðkenni fólks.** `http://baekur.is/rdf/agent/<n>` er innra
  númer Bækur.is, án tengingar við VIAF, ISNI eða nafnmyndaskrá Gegnis. Nafnar
  án æviára renna saman í síunni.
- **Samræmdir titlar sem höfundar.** Við færum þá í `dcterms:hasPart`. Hvort
  Primo leitar í þeim reit er óstaðfest.
- **Engin lýsing og enginn útgefandi bókarinnar.** `dc:publisher` er
  Landsbókasafn sem gagnaveita, ekki forlagið eða prentsmiðjan.
- **Engin sett.** Ekki er hægt að sækja eftir öld, tungumáli eða prentsmiðju.

## Spurningar til Kristins Sigurðssonar

1. **Réttindi.** 2.982 af 2.984 bókum eru merktar „In Copyright“, líka bækur
   frá 16.–19. öld. Er það sjálfgefið gildi? Má setja almenningseign (PDM) eftir
   útgáfuári eða dánarári höfundar, eins og á Stúlku og Kviðlingum?
2. **Endapunkturinn.** Getur `Identify` auglýst `https://baekur.is/oai` og
   endapunkturinn tekið við POST (nú 403)? Og getur `earliestDatestamp` verið
   elsti dagstimpillinn en ekki elsta útgáfuárið (1540)?
3. **Auðkenni fólks.** Getur `edm:Agent` borið `owl:sameAs` á VIAF, ISNI eða
   nafnmyndafærslu í Gegni? Þá renna nafnar ekki saman og fólk sameinast milli
   safna.
4. **Hlutverk og samræmdir titlar.** Getur straumurinn greint höfund,
   þýðanda, útgefanda og prentara (MARC `$e`/`$4`)? Og skilað samræmdum titlum
   (Eddukvæði, Biblían) sem titlum en ekki höfundum?
5. **Útgáfustaður.** Bókaskrá sýnir „Bækur eftir útgáfustað“ með hnitum. Getur
   `edm`-sniðið borið útgáfustaðinn með GeoNames-auðkenni? Og hvers vegna fær
   bók án landakóða GeoNames-auðkenni Íslands?
6. **Sett.** Væri hægt að bjóða sett, t.d. eftir öld, tungumáli eða
   prentsmiðju?

## Smíða aftur

```bash
/usr/bin/python3 gagnaveitur/baekur/byggja_baekur_dc.py                # sækir og skrifar báðar skrárnar
/usr/bin/python3 gagnaveitur/baekur/byggja_baekur_dc.py --vista hratt/ # sama, og vistar hráu síðurnar
/usr/bin/python3 gagnaveitur/baekur/byggja_baekur_dc.py hratt/         # úr vistuðum síðum, án nets
/usr/bin/python3 -m unittest discover -s gagnaveitur/baekur            # prófanir umbreytingarinnar
```

Umbreytingin prentar allar stofnanir og öll verk sem hún finnur, löndin, og
hvert ósamræmi milli landakóða og GeoNames. Bækur.is skilar efnisorðum hverrar
bókar í nýrri röð við hverja uppskeru; þau eru því röðuð, og tvær uppskerur
1.10.2026 gáfu nákvæmlega sömu skrá.

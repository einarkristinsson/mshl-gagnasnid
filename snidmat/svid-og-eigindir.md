# Svið og eigindir

**Fyrir þann sem útfærir normaliseringu og birtingu.**
Útgáfa 1.0 · 16. september 2026

Sniðið sjálft er í [`GULLNA-SNIDID.md`](GULLNA-SNIDID.md); kröfur til
afhendingarinnar í [`../oai-pmh/LEIDBEININGAR.md`](../oai-pmh/LEIDBEININGAR.md).
Hér er hitt: hvaða PNX-svið hver reitur lendir í, hvaða svið eru raunverulega til,
hvaða merkimiða þarf að setja og hvaða forsendur reglur mega treysta á.

## 1. Gullið DC → PNX

Fylla skal **staðlaða PNX-reiti** alltaf og bæta local-sviði við þar sem þarf
sérstaka síu eða sérstakan birtingarreit.

| Gullið DC | PNX-svið | localNN | Hlutverk | Gagnaveitur sem nota |
|---|---|---|---|---|
| `dc:title` | `dc.title` + `discovery.local1` | local1 | birting, leit | allar |
| `dc:type` (bæði gildi) | `dc.type` | — | birting | allar |
| `dc:type` `@en` | `discovery.resourceType` | — | **sía**, birting | allar |
| `dc:type` `@en` | `discovery.local2` | local2 | **sía**, birting | allar |
| `dc:subject` | `dc.subject` | — | leit | allar |
| `dc:subject` `@is` | `discovery.local93` | local93 | **sía** | Handrit, Ísmús, gullna reglusettið |
| `dc:subject` | `discovery.local3` | local3 | **sía** | SMB (úrelt númer — sjá kafla 2) |
| `dc:subject[@xsi:type='mshl:starf']` | `discovery.local29` | local29 | — | Ævir — **svið ekki til, no-op** |
| `dcterms:spatial` (ekki POINT) | `dc.coverage` + `discovery.local22` | local22 | **sía**, birting | Handrit, Ævir, gullna reglusettið |
| `dc:coverage` (sögustaður) | `dc.coverage` + `discovery.local22` | local22 | **sía**, birting | Ísmús |
| `dc:coverage` `Sókn:` | `discovery.local23` | local23 | **sía**, birting | SMB |
| `dc:coverage` `Hreppur:` | `discovery.local24` | local24 | **sía**, birting | SMB, Jarðaskrá — **árekstur, sjá kafla 2** |
| `dc:coverage` `Sýsla:` | `discovery.local25` | local25 | **sía**, birting | SMB, Jarðaskrá |
| `dcterms:spatial[@xsi:type='mshl:sysla\|hreppur\|sokn\|baer']`, `dcterms:temporal[@xsi:type='mshl:manntal']` | `discovery.local36–40` | local36–40 | **sía** | gullna reglusettið — **svið ekki til, no-op** |
| `dcterms:spatial[@xsi:type='dcterms:Point']` | `discovery.local27` | local27 | birting (kort) | SMB, Jarðaskrá, Ísmús |
| `dc:source` (ekki `http`) | `discovery.local26` | local26 | birting | SMB, Jarðaskrá |
| `dcterms:temporal` | `dc.coverage` + `discovery.local31` | local31 | birting | Ævir, Handrit (`mshl:timabil`) |
| `dc:relation` (`http`) | `discovery.local31` | local31 | birting (tengill) | SMB — **rekst á `dcterms:temporal` hjá Handriti og Ævum** |
| `dcterms:relation` (`http`), `dcterms:isPartOf` | `dcterms.isPartOf` + `discovery.local35` | local35 | birting (tengill) | gullna reglusettið, Ævir (Handrit fyllir aðeins `dcterms.isPartOf`) |
| `dcterms:relation[@xsi:type='mshl:folk']`, `dcterms:hasPart[@xsi:type='mshl:verk']`, `edm:dataProvider` | `discovery.local42–44` | local42–44 | **sía** | Handrit, Ævir — **svið ekki til, no-op** |
| `dc:creator`, `dc:contributor` | `dc.creator`, `dc.contributor` + `discovery.local49` | local49 | birting, leit | Ísmús (Handrit setur `edm:provider` í local49) |
| `dcterms:bibliographicCitation` | `discovery.local75` | local75 | birting | Ævir, Ísmús |
| `dc:identifier` (`http`) | `dc.identifier` + `dcterms.source` | — | tengill heim | allar |
| (sett í reglu) gagnaveita | `discovery.local5` | local5 | **sía**, birting | allar |
| (sett í reglu) `XDS` | `dcterms.source` | — | umfangssía, ekki birt | allar ytri gagnaveitur |
| `dc:date` | `dc.date` | — | birting, leit | allar |
| `dc:description` | `dc.description` | — | birting, **heildartextaleit** | allar |
| `dc:publisher`, `dc:language`, `dc:rights` | `dc.publisher`, `dc.language`, `dc.rights` | — | birting (tungumál einnig sía) | allar |

## 2. Hvaða local-svið eru raunverulega til í Alma NZ

Útflutningur úr NZ 1.9.2026 —
[`../../leidarljos/dc-template/alma/displayFieldsList-NZ-2026-09-01.csv`](../../leidarljos/dc-template/alma/displayFieldsList-NZ-2026-09-01.csv)
— telur 41 svið, þar af 37 `local_field_NN`. Svið sem er ekki á þessum lista er
ekki til: regla sem skrifar í það þýðist hreint og gerir ekki neitt.

| Svið | Global merkimiði | Okkar notkun |
|---|---|---|
| local_field_01 | Full Title | Titill |
| local_field_02 | Granular Resource Type | Tegund |
| local_field_03 | Imprint | Efni (SMB) — **villandi merkimiði** |
| local_field_05 | Data Source | Gagnaveita |
| local_field_22 | Location | Staður (hrein gildi) |
| local_field_23 | Age | Sókn — **villandi merkimiði** |
| local_field_24 | Museum | Hreppur — **árekstur, sjá að neðan** |
| local_field_25 | Accession number | Sýsla — **villandi merkimiði** |
| local_field_26 | Sub-directory | Heimild — **villandi merkimiði** |
| local_field_27 | Size | Hnit — **villandi merkimiði** |
| local_field_31 | Period | Tímabil (Handrit, Ævir) og tenglar (SMB) |
| local_field_35 | Reference | Tengsl |
| local_field_49 | Creators | Fólk (íslenskt heiti ekki staðfest) |
| local_field_75 | Note | Athugasemd (íslenskt heiti ekki staðfest) |
| local_field_93 | Subject | Efni |

> 🔴 **Sviðin 36–44 eru horfin.** Þau voru skilgreind í Alma NZ 17. júlí 2026 sem
> MSHL-blokk (Sýsla, Hreppur, Sókn, Bær, Manntal, Hnit, Fólk, Verk, Safn), en
> **lifðu ekki sumarhreinsun sandkassans**. Útflutningurinn 1.9.2026 sýnir
> ekkert svið á bilinu 36–44 — staðfest. Reglur sem skrifa í þau eru því
> **skaðlaus no-op**: þær þýðast, keyra og skila engu. Endurskilgreining
> („Define a Local Field“ í NZ) er óunnið verk.

> 🔴 **`local_field_24` er í notkun hjá annarri gagnaveitu.** Mæling á lifandi
> vísi 1.9.2026 sýndi að Ljósmyndasafn Reykjavíkur fyllir `lds24` með nafni
> varðveislustofnunar á 100 % færslna — rétt miðað við global-heitið *Museum*.
> Yrði `lds24` gert að hreppasíu birtist stofnunin þar sem stærsta gildið.
> Ákvörðunin fyrir demó 2.9 var að virkja `lds23`, `lds25` og `lds26` en
> **sleppa `lds24`**: tveir staðarfacetar í stað þriggja, enginn árekstur.

## 3. Merkimiðar sem þarf að setja

Alma → Configuration → Discovery → Display Configuration → Labels. **Tveir kóðar
á hvert svið**: einn fyrir fulla birtingu og einn fyrir síuheitið; báða má lesa
úr viðmótinu með `&debugLabels=true` aftan við Leitir-slóðina. View-sértæki
kóðinn (`354ILC_NETWORK:MSHL_UNION.fulldisplay.lds##`) er notaður þegar hann er
í boði, því `default.` snertir öll view.

| Svið | Íslenskt heiti | Birtingarkóði | Síukóði |
|---|---|---|---|
| lds36 | Sýsla | `default.fulldisplay.lds36` | `nui.facets.lds36` |
| lds37 | Hreppur | `default.fulldisplay.lds37` | `nui.facets.lds37` |
| lds38 | Sókn | `default.fulldisplay.lds38` | `nui.facets.lds38` |
| lds39 | Bær | `default.fulldisplay.lds39` | `nui.facets.lds39` |
| lds40 | Manntal | `default.fulldisplay.lds40` | `nui.facets.lds40` |
| lds41 | Hnit | `default.fulldisplay.lds41` | (ekki sía) |
| lds42 | Fólk | `default.fulldisplay.lds42` | `nui.facets.lds42` |
| lds43 | Verk | `default.fulldisplay.lds43` | `nui.facets.lds43` |
| lds44 | Safn | `default.fulldisplay.lds44` | `nui.facets.lds44` |

Taflan bíður þess að sviðin 36–44 verði endurskilgreind (kafli 2). Sviðin sem eru
í notkun í dag — 03, 23, 25, 26, 27 — bera villandi global-heiti og þurfa
view-sértækan íslenskan merkimiða á sömu tvo kóða. Merkimiðar sjást strax;
**síugildi geta tekið nokkra daga** vegna skyndiminnis.

## 4. `xsi:type`-eigindir

Flokkunin er borin af eigindinni, ekki af textanum — þannig helst gildið hreint
og sameinast gildum frá öðrum söfnum. Nafnrýmið er `xmlns:mshl="https://mshl.is/terms#"`.

| Eigind | Á reit | Merking |
|---|---|---|
| `mshl:sysla` | `dcterms:spatial` | Sýsla |
| `mshl:hreppur` | `dcterms:spatial` | Hreppur |
| `mshl:sokn` | `dcterms:spatial` | Sókn |
| `mshl:baer` | `dcterms:spatial` | Bær — neðsta stig staðarstigveldisins |
| `mshl:stadur` | `dc:coverage` | Staður án stigs (Ævir: starfsstaður) |
| `mshl:manntal` | `dcterms:temporal` | Manntalsár, hreint ártal án orðsins „Manntal“ |
| `mshl:folk` | `dcterms:relation` | Nafn manneskju, hreint; hlutverkið í `mshl:role` |
| `mshl:verk` | `dcterms:hasPart` | Verk í handriti, hreint heiti án forskeytis |
| `mshl:starf` | `dc:subject` | Starf eða embætti manneskju |
| `mshl:flokkur` | `dc:subject` | Sameiginlegur efnisflokkur — grófa sían |
| `dcterms:Point` | `dcterms:spatial` | WKT-hnit, `POINT(lengd breidd)` |

Til viðbótar koma `mshl:role` (hlutverk með fólki og stöðum), `mshl:id` (varanlegt
auðkenni efnisorðs) og `mshl:efnisord` (efnisorð gagnaveitunnar sjálfrar) — sjá
kafla 4 í [`../oai-pmh/LEIDBEININGAR.md`](../oai-pmh/LEIDBEININGAR.md).

## 5. ⚠️ Varnaðarorð um forsendur í reglum

Forsendur sem eru **staðfestar í Alma** og reglusett mega treysta á:

```
[@xml:lang='is']   [@xml:lang='en']
starts-with(text(),'http')   starts-with(text(),'POINT')
not(starts-with(text(),'http'))
```

Forsendan `@*[local-name()='type']='mshl:…'` er hins vegar **óstaðfest**.
Hún hittir rétt í `xmllint` á raungögnum — mælt á 2.801
Ævir-færslum hitti `mshl:starf` á 2.801 og `mshl:stadur` á 2.793 — en **ekki er
vitað hvort Alma þýðir hana**. Hún féll á Ævum 10.9.2026, og nýjasta reglusettið
(Ísmús) forðast hana viljandi.

**Afleiðing fyrir útfærslu:** reglusett eiga að nota staðfestu formin hvar sem því
verður við komið og hafa varaleið fyrir hin. Ísmús-settið sýnir mynstrið: allar
aðgreiningar eru gerðar á `@xml:lang` eða `starts-with`, og eina reglan sem er háð
eigind hefur skráða varaleið — falli hún er henni breytt í `[@xml:lang='is']` og
sían ber þá bæði flokka og efnisorð í stað flokka einna.

## 6. Endurteknir reitir með forskeyti kosta eina reglu á vísitölu

Regluvélin getur ekki lykkjað. Beri reitur forskeyti sem þarf að fjarlægja, og
sé reiturinn endurtekinn, þarf **eina reglu fyrir hverja vísitölu** —
`[1]`, `[2]`, `[3]` … upp að hæsta fjölda sem mælist í gögnunum.

| Gagnaveita | Reitur | Reglur |
|---|---|---|
| Jarðaskrá | `dc:coverage` `Hreppur:` | **24** |
| Jarðaskrá | `dc:coverage` `Sýsla:` | **8** |
| SMB | `dc:coverage` `Sókn:` / `Hreppur:` / `Sýsla:` | 8 + 8 + 6 = **22** |
| SMB | `dc:coverage` `Heimili:` (fjögur stig í einum streng) | **48** |

Grunnreglusett SMB telur 22 reglur; með forskeyta- og Heimili-reglunum fer það
í **89**. Slíkt reglusett þýðist, en það er ólesanlegt, það brotnar þegar ein
færsla ber 25. hreppinn, og hverja nýja gagnaveitu þarf að mæla upp á nýtt til
að finna réttan fjölda.

Þess vegna eru hrein gildi ekki fegurðarmál. Berist
`<dcterms:spatial xsi:type="mshl:hreppur">Staðarhreppur</dcterms:spatial>`
í stað `<dc:coverage>Hreppur: Staðarhreppur</dc:coverage>` fara Jarðir úr
32 reglum í eina — óháð því hve oft reiturinn endurtekur sig.

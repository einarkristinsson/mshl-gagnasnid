# Gátlisti fyrir afhendingu

Til að haka í áður en gagnaveita er afhent. Ítarlegar skýringar á hverju
atriði eru í [LEIDBEININGAR.md](LEIDBEININGAR.md).

**Gáttagægir keyrir þennan lista sjálfvirkt** — límdu inn slóð endapunktsins
og fáðu stóðst/villu-skýrslu. Sjá [`../verkfaeri/gattagaegir/`](../verkfaeri/gattagaegir/).

## Endapunktur

- [ ] `Identify` svarar og `baseURL` þar virkar orðrétt
- [ ] `adminEmail` er til staðar
- [ ] GET **og** POST virka bæði á þeirri slóð
- [ ] `ListMetadataFormats` auglýsir `oai_dc`
- [ ] `ListIdentifiers`, `ListRecords` og `GetRecord` virka öll
- [ ] `ListRecords` gengur á enda og talan stemmir við `completeListSize`
- [ ] Ein skemmd færsla fellir ekki heildina
- [ ] `from`/`until` sía raunverulega — biddu um eina sekúndu og sjáðu hvort talan lækkar
- [ ] Auglýst sett eru ekki tóm og leka ekki hvert í annað
- [ ] Villur koma sem OAI-villukóðar, ekki HTML eða PHP-villa

## Færslur

- [ ] `dc:title` á öllum, aldrei tómur
- [ ] `dc:identifier` með varanlegri slóð sem svarar 200 (ekki 302 á forsíðu)
- [ ] `dc:type` sem par: `@is` og `@en`
- [ ] `dc:subject` á öllum sem geta borið það
- [ ] Staðarreitur (`dc:coverage` eða `dcterms:spatial`) á öllum sem geta borið hann
- [ ] **Smámyndaslóð** með þar sem mynd er til — bein (`.jpg`/`.png`), opin án innskráningar, aðgreinanleg frá síðuslóðinni með regex
- [ ] `dc:rights` segir hvað má
- [ ] `dc:language` með ISO-kóða

## Hreinleiki

- [ ] Engin `None`, `null`, `N/A` eða `-` sem gildi — reitnum sleppt í staðinn
- [ ] Engir tómir reitir
- [ ] Engin færsla með haus en tómu `<oai_dc:dc/>`
- [ ] Engin stýritákn (`\x00`–`\x1f` nema tab og línuskil)
- [ ] Ekkert `]]>` inni í `CDATA`
- [ ] UTF-8, engin BOM
- [ ] Skráin er gilt XML — keyrð gegnum `xmllint --noout`

## Gildi

- [ ] Dagsetningar á EDTF (`1887` eða `1703/1910`)
- [ ] Staðanöfn í **nefnifalli** (`Skálholt`, ekki `Skálholti`) — eða **hnit/auðkenni** með ef heimildin ber beygða mynd
- [ ] Engin forskeyti í gildum (`Rangárvallasýsla`, ekki `Sýsla: Rangárvallasýsla`)
- [ ] Hnit á sniðinu `POINT(lengd breidd)` — á Íslandi er lengd neikvæð
- [ ] Öll hnit innan raunhæfra marka
- [ ] Efnisorð bera varanlegt auðkenni
- [ ] Hlutverk fylgja fólki og stöðum þar sem þau eiga við
- [ ] Heildartexti er hreinn texti — ekkert HTML, réttur `xml:lang`
- [ ] Vélþýðingar eru í eigin reit og merktar sem slíkar

## Áður en þú sendir

- [ ] Sótt full uppskera og talin færslur — stemmir hún?
- [ ] Opnað tíu færslur af handahófi og lesið þær
- [ ] Smellt á tíu slóðir — svara þær allar?

# MSHL – Samþætt persónuauðkenni þvert á söfn
## Umræðuskjal fyrir teymið

### Kjarninn í einni setningu

Verðmæti MSHL felst ekki í stærri leitarglugga heldur í **áreiðanlegu persónuauðkennaneti**. Afurðin er varanlegt persónuauðkenni (PID) sem gerir notanda kleift að finna *einn* tiltekinn einstakling og sækja svo allt sem tengist honum þvert á öll ~25 söfnin. Kerfið er **auðkennaþjónusta, ekki gagnavöruhús**: hvert safn er áfram ábyrgt fyrir sínu efni, MSHL er einungis ábyrgt fyrir því *hver er hver*.

### Grundvallarforsenda: enginn ókeypis hádegismatur

Alma og Primo/Leitir gera **enga „töfravinnu"** við auðkenni. Discovery *skráir í vísi (index)* það sem við gefum því — nákvæmlega eins og við gefum það. Öll greindarvinnan (útdráttur úr texta, aðgreining einstaklinga, líkindamöt, samtenging) fer fram **hjá okkur, áður en gögnin fara í Alma/Primo**. Primo speglar niðurstöðuna í facet; það reiknar hana ekki.

Eina raunverulega „auðgunin" sem Primo bætir við: þegar færsla er tengd nafnmyndarfærslu (authority record) skráir Primo bæði forgangsheiti (1XX) og aukaheiti/tilvísanir (4XX) í vísinn — þannig finnst færslan þótt leitað sé með annarri stafsetningu. Þetta víkkar *leitarorð*; það sameinar **aldrei** einstaklinga sjálfkrafa.

---

## Þrennt sem verður að halda aðskildu

1. **Viðmiðunargrunnur (reference spine)** – afvímaður (deduplicated) persónugrunnur til að miða við (helst Íslendingabók; annars byggður úr lýsigögnum safnanna).
2. **Nefningar í heimildum (source mentions)** – óreiðukenndar persónutilvísanir þvert á 25 söfnin, án lykla. Þetta er það sem við höfum.
3. **Staðhæfingatafla (assertion table)** – vörpunin `nefning → PID`, byggð nefningu fyrir nefningu. **Þetta er afurðin.** Allt annað er lagnavinna.

---

## Hönnunarreglur sem ekki verður hvikað frá

- **Kennitala er gagnslaus hér** – hún er of ný fyrir efnið. Sérhver söguleg samtenging byggist á lýsigögnum (nafn + dagsetningar + staður + faðir), aldrei á auðkennisnúmeri.
- **Föðurnöfn eru árekstrar, ekki ættarnöfn.** „Jón Sigurðsson" felur í sér nafn föðurins – sterkasta ókeypis vísbendingin sem við höfum. Föðurakkeruð grófsíun (blocking) er efsta þrepið.
- **`óleyst` og `óvíst` eru fyrsta flokks, varanleg og líklega meirihlutastaða.** Röng staðhæfing er verri en engin – hún spillir hljóðlaust allri samtengingu sem á henni byggir. Há nákvæmni með hóflegri þekju (recall) er betri en öfugt.
- **Ágiskanir haldast líkindabundnar fram að einu hliði.** Útdráttur *leggur til*, samtenging *raðar*, aðeins staðhæfingarþröskuldur (oft + manneskja) breytir ágiskun í staðreynd.
- **PID = ógegnsær fastur kjarni (`mshl:p:{ULID}`) + einnota læsilegt heiti** (`Jón Sigurðsson (1811–1879) [Rafnseyri]`). Tengt er á ULID; heitið er endurgeranlegt viðmótsskraut, aldrei burðarvirki.
- **Frjáls texti = tvær ágiskanir í röð.** Berum bæði líkur á *einingu* (er þetta staður/persóna?) og líkur á *hlutverki* (fæðingarstaður? myndefni?) sem aðskildar rásir – „fæddur á X" er sterkur lykill, „myndaður á X" nánast gagnslaus fyrir auðkenni.
- **Stafsetning ≠ óvissa.** Sigurðsson/Sigurdsson er samræmingarregla (ákveðin). „Er þetta bæjarnafn eða ættarnafn?" er líkindamál. Aðskildar raðir, aðskildar lausnir.

---

## Útfærslukostir

| | **A – Dreifður lykill (mælt með)** | **B – Miðlægt, vinna, endurbirta** |
|---|---|---|
| Staðsetning efnis | verður áfram í hverju safni | afritað í miðlægan grunn (fork) |
| Endursamstillingarkostnaður | lágur (ýtum breyttum PID-tengingum) | hár (endurheimta + endurleysa við hverja breytingu) |
| Tenging við kerfin | laus (safn + staðarlykill + nafn) | þétt (við eigum 25 efnislíkön) |
| Stjórnskipulag | afhendum eigendum vörpunartöfluna | við verðum í reynd miðlægur eigandi (pólitískt þungt) |
| Niðurstaða | **burðarás kerfisins** | hætta á úreltri afritun; forðast sem aðalleið |

**Mælt er með kosti A.** MSHL verður miðlægt aðeins um *auðkennanetið* – eina hlutinn sem á að vera miðlægur. Hvert safn heldur forræði yfir eigin efni.

**Staðhæfingatafla (eignin sjálf):**
```
mshl_person_assertion
  pid              -- MSHL persónuauðkenni (ULID)
  source           -- 'sarpur' | 'gegnir' | ...
  source_local_id  -- fastur lykill færslu í heimakerfi (ALDREI titill)
  role             -- creator | subject | donor | mentioned | ...
  name_as_recorded -- strengurinn eins og hann birtist (rekjanleiki)
  p_extract        -- líkur á réttum útdrætti úr texta
  p_role           -- líkur á réttu hlutverki
  p_link           -- líkur á réttri samtengingu við PID
  p_joint          -- samsett líkindi; það sem þröskuldað er á
  rank             -- 1 = besta; geymum 2,3 fyrir yfirferð
  ib_id            -- Íslendingabókarlykill (krosstenging, ekki PID)
  method           -- 'father+given+year' | 'manual' | ...
  asserted_by / asserted_at
```
Samtengilykill: `(source, source_local_id, role)` – **aldrei titill.**

---

## Íslendingabók

Besta sögulega þekjan á Íslandi. **Biðjum um lykilinn, ekki efnið** – annaðhvort:

1. **Samtengiþjónusta (endpoint):** við sendum lýsigögn (nafn + dags + staður + faðir), fáum til baka IB-lykil eða „engin örugg samsvörun". Engin ættfræði fer út fyrir þeirra veggi – aðeins ógegnsær lykill.
2. **Útdráttur um látna eina:** IB-lykill + lágmarkslýsigögn (nafn, f./d. dags, fæðingarstaður, IB-lykill föður). Sögulegar persónur einar, sem sneiðir framhjá persónuvernd að mestu.

IB-lykill er geymdur sem **ytri krosstenging** á PID – nákvæmlega eins og VIAF – **aldrei sem PID sjálft.** Ef IB tekur ekki þátt stendur kerfið eftir sem áður á okkar eigin PID; yfirferðarröðin lengist bara. Föður-/foreldratengslin eru gullið: leyst föðurnafn þrengir leitarrýmið um margar stærðargráður.

---

## Nafnmyndarfærslur (authority records) í Alma

Nafnmyndarfærsla í Alma er MARC-authority (1XX forgangsheiti, 4XX aukaheiti/tilvísanir, 5XX sjá-einnig) sem tengist bókfræðifærslum með **auðkennistengingu (ID-based linking)** – kíkis-táknið birtist þegar tenging kemst á.

Hlutverk þeirra í MSHL:
- **Fyrir Alma-vistaðar færslur** fáum við MARC-authority + vafur (browse) í Primo + LOD-persónuspjöld ókeypis. Authority-MMS-lyklar verða þá einfaldlega enn ein `source` í staðhæfingatöflunni.
- **Mikilvægt: authority-tengingin er *afurð* upplausnarvinnunnar okkar, ekki uppspretta hennar.** Alma leysir ekki hver er hver – það neytir tengingar sem við höfum staðfest.

Tvö raunveruleg mörk sem teymið verður að vita:
- **Vafur (browse) virkar aðeins á Alma-vistuðum gögnum.** Ytri (harvested) söfnin eru leitanleg í Leitir en fá ekki fulla authority-meðhöndlun.
- **LOD-persónueiningar tengjast aðeins LCNAMES-nafnmyndum, aðeins á ensku.** Þunnt fyrir íslensk söguleg nöfn – okkar eigin PID vinnur raunverulega vinnuna; LOD-spjöldin eru bónus fyrir þekktustu einstaklingana.

---

## Við verðum að undirbúa öll svið sem á að skrá í vísi

Þetta er lykilatriði og oft vanmetið: **Primo skráir aðeins það sem er skilgreint sem svið og varpað gegnum samræmingarreglur (normalization rules).** Ekkert verður leitanlegt eða facet-hæft „af sjálfu sér". Undirbúningslisti:

1. **Velja MARC-svið fyrir PID (Alma-leiðin)** – t.d. 024 eða 9XX með ULID, eða undirsvið á 1XX. Verður að lifa af birtingu (publishing) og rekast ekki á neitt sem Landskerfi samræmir nú þegar.
2. **Velja DC-einingu fyrir PID (ytri leiðin)** – PID sprautað inn í DC/XML við heimtingu (harvest).
3. **Samræmingarregla sem lendir báðum leiðum í *einu* `mshl_pid` facet** – eitt facet, tvær áfyllingarleiðir.
4. **`mshl_role` sem sérstakt facet** – svo notandi geti síað „myndir *af* Jóni" vs. „myndir *eftir* Jón".
5. **Fjölgild svið (multi-valued)** – ein færsla getur nefnt marga (ljósmyndari + myndefni). Facet-sviðið verður að vera endurtekjanlegt svo færsla birtist undir *öllum* PID sem hún staðhæfir.
6. **Endurvísun (re-index)** – auðgun facet krefst yfirleitt endurvísunar; á landsvísu er það samræmd, tímasett aðgerð (sum stilling keyrð af Ex Libris Support). Því **söfnum við staðhæfingum í lotur** og ýtum í hópum – ekki dropatalið.

Ein setning fyrir hagaðila: **„MSHL leysir auðkenni framar í keðjunni og skrifar eitt samræmt PID-facet í vísi Primo – þverfagleg samtenging verður þá venjulegur facet-smellur, ekki ný leitartækni."**

---

## Svör við lykilspurningum

**1. Getum við notað Leitir (= Alma + Primo VE)?**
Já – sem vettvang fyrir geymslu, skráningu og discovery. Nei – sem upplausnarvél. Alma geymir authority + PID; Primo speglar PID í facet og víkkar leit með authority-tilvísunum. Hvorugt ákveður *hvaða* Jón nefning á við. Sú ákvörðun er okkar, framar í keðjunni.

**2. Getur ML búið til PID og spálíkan gefið „input → þetta PID, 90% viss"?**
ML á **ekki** að búa til PID (það er ákveðin aðgerð: eitt ULID á hvern leystan einstakling). Hlutverk ML er *spálíkanið*: gefa **raðaðan lista frambjóðenda með kvörðuðum líkindum**, og staðhæfa aðeins yfir þröskuldi. „90% viss" er aðeins marktækt ef líkanið er **kvarðað** gegn sannreyndu úrtaki (hér borgar IB-úrtak eða nokkur hundruð handleystar nefningar sig). Stórt mállíkan er frábært sem **tillögugjafi** (draga nöfn/staði/hlutverk úr íslenskum texta) en aldrei sem **dómari** – ákveðni burðarásinn (föðursíun, log-odds reikningur, þröskuldur) ræður því hvað er skrifað.

**3. Getum við gert loðnar samtengingar (`a.x =90%= b.x`)?**
Já – það er einmitt samtengingarþrepið, en heiðarlega útgáfan er ekki einn strengjasamanburður. `nafn ≈ nafn` eitt og sér er *frambjóðendaframleiðandi*, ekki samtenging (1000 Jónar passa allir 90% á nafn). Raunveruleg „loðin samtenging" er **fjölsviða líkindasamtenging** (Fellegi-Sunter / log-odds): hvert svið sem passar bætir vægi, ósamræmi dregur frá, vantandi svið eru hlutlaus göt, summan þröskulduð. Verkfæri: SQL loðin skilyrði (trigram/`pg_trgm`, Levenshtein, Jaro-Winkler) fyrir grófsíun; Python (`recordlinkage`, `splink`, `dedupe`) fyrir stigagjöf. **Athugum bilið (margin)** – efsti frambjóðandi mínus næsti: hátt stig + lítið bil = raunveruleg óvissa → yfirferð, aldrei sjálfvirk samtenging.

**4. Það sem ekki var spurt en mun mæta okkur:**
- **Staðir þurfa eigin upplausn, á undan fólki.** Leystur fæðingarstaður er einn sterkasti persónulykillinn og oftast fastur í frjálsum texta. Þarf örnefnagrunn (bær/sókn/sýsla).
- **Faðirinn er endurkvæmur** – oft þarf að leysa föðurinn áður en barnið er grófsíað. Lausn: leysa viðmiðunargrunninn **kynslóð fyrir kynslóð, elstu fyrst**.
- **Stafsetning ≠ óvissa** – aðskildar raðir (sjá reglur að ofan).

---

## Tillaga að fyrsta áfanga

**Þyrping nefninga innan/þvert á söfn (mention clustering)** – þjappa 1000 Jónum í ~40 frambjóðanda-einstaklinga út frá samliggjandi lýsigögnum þeirra, *áður* en nokkur IB-samtenging fer fram. Hæsta vogarafl, alfarið í okkar höndum, virkar með eða án Íslendingabókar. Breytir „1000 nefningum" í „~40 einstaklinga, 12 leysanlega". Allt í framhaldinu (IB-samtenging, staðhæfing, Leitir-facet) verður ódýrara þegar þetta er til.

---

## Viðbót 28.9.2026 · Safn RÚV: samtímafólk með eigin lykla

**Athugun Einars.** Gögn RÚV eru í raun eins og bókasafnsgögn. Þau hefðu gagn af bókfræðiskráningu og nafnmyndarfærslum fyrir fólk. Munurinn er sá að fólkið er oft samtímafólk og efnið nær ekki langt aftur í tímann, líklega til um 1968. Fólk í gögnum RÚV er oft þegar til í Leitir, sem höfundar bóka, tónlistar eða annars efnis. Hér erum við komin inn á áhugaverð svið.

**Mælt í sýnishornunum 14 frá RÚV.** Hér eru aðeins reitaheiti og fjöldi, engin gildi.

| Mæling | Niðurstaða |
| --- | --- |
| Persónutilvísanir | 107 |
| Einstaklingar | 81 |
| Með `PERSON_ID` (átta stafa hex-lykill) | 107 af 107 |
| Sama manneskja í fleiri en einni færslu | 8 einstaklingar, alltaf sami `PERSON_ID`, engin frávik |
| Með kennitölu (`PERSON_ALT_NAME`) | 91 af 107 |
| Ytri tilvísun (`PERSON_EXT_REF00`) | reiturinn er til en tómur í öllum |

### Hvað þetta þýðir fyrir hugmyndina

1. **RÚV á þegar sína eigin persónuskrá.** `PERSON_ID` er fastur lykill, einn á hverja manneskju þvert á færslur. RÚV er því ekki uppspretta óreiðukenndra nefninga (flokkur 2 að ofan) heldur gagnaveita með eigin lykli. Í staðhæfingatöflunni verður `source = 'ruv'` og `source_local_id = PERSON_ID`. Samtengingin verður þá á milli persónuskráa en ekki einstakra nefninga, sem er margfalt auðveldara.
2. **Reglan „kennitala er gagnslaus“ á ekki við RÚV.** Hún gildir um sögulegt efni. Hjá RÚV er kennitala skráð hjá flestum og er sterkasti lykill sem völ er á. Hún má samt aldrei fara út. Ef hún er notuð til samtengingar verður það að gerast innan veggja RÚV eða hjá aðila með heimild, og aðeins ógegnsær lykill kemur út. Þetta er sama mynstur og við Íslendingabók: biðjum um lykilinn, ekki efnið. Þetta þarf að ræða við persónuverndarfulltrúa, og það verður að rúmast innan vinnslusamnings.
3. **`PERSON_EXT_REF00` er tilbúinn staður fyrir krosstengingu.** Ef RÚV skráir þar nafnmyndarlykil úr Gegni eða MSHL-auðkenni skilar tengingin sér heim í safnkerfi RÚV. RÚV er að innleiða nýtt safnkerfi, og nú er rétti tíminn til að spyrja hvort það hafi slíkan reit.
4. **Tvær kynslóðir í sömu færslu.** Flytjendur, umsjónarmenn og tæknifólk eru samtímafólk. Höfundar texta og laga geta hins vegar verið sögulegir. Í sýnishornunum er textahöfundur fæddur 1928 í upptöku frá 1983. RÚV-gögnin snerta því bæði viðfangsefnin: samtímafólk með lyklum og sögulegt fólk án þeirra.
5. **Persónuvernd togar í tvær áttir.** Í DC-umbreytingunni fjarlægjum við fæðingarár lifandi fólks. Í Leitir birtast höfundar hins vegar oft með fæðingarári úr nafnmyndarfærslu. Ef manneskja úr RÚV-gögnum er tengd nafnmyndarfærslu birtist fæðingarárið í gegnum tenginguna. Það þarf skýra reglu um hvort það sé í lagi.
6. **Tímaramminn er óstaðfestur.** „Frá um 1968“ er mat Einars. Elsta upptakan í sýnishornunum er frá 1983. Spyrjum RÚV hvernig efnið dreifist á áratugi.

**Næsta mæling.** Keyrum nöfnin 81 gegn Leitir og teljum hve mörg finnast sem höfundar eða í nafnmyndaskrá Gegnis. Það gefur tölu fyrir styrkumsóknina 29.10. Sjá einnig [gagnaveitur/RUV/README.md](gagnaveitur/RUV/README.md).

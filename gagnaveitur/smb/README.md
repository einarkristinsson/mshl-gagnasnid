# Sögulegt mann- og bæjatal (SMB)

Gagnasafn um bæi og fólk á Íslandi, byggt á manntölum og jarðabókum. Miðstöð
stafrænna hugvísinda og lista gefur út; gagnasafnið er unnið af ad libitum ehf.

## Endapunktur

| Atriði | Gildi |
|---|---|
| `baseURL` sem `Identify` auglýsir | `https://smb.mshl.is/oai` (án skástriks) |
| Slóð sem virkar | `https://smb.mshl.is/oai/` (með skástriki) |
| `metadataPrefix` | `oai_dc` |
| Sett | `type:baer` · `type:einstaklingur` · `type:m:einstaklingur` · `source:smb` (auk `era:`-setta) |
| `completeListSize` | `type:baer` 17.371 · `type:einstaklingur` 223.795 · `type:m:einstaklingur` 982.488 · `source:smb` 1.223.654 |
| Mælt | 26.–28.8.2026 (lifandi `ListRecords`, fyrsta síða hvers setts) |

Innlestur í Leitir fer fram með **skráarinnlestri** (Upload File/s) en ekki með
lifandi OAI-uppskeru. Ástæðan er skjalfest: uppskerujobb gegn auglýstu slóðinni
féll á `Premature end of file` (26.8.2026) og seinna jobb sat í `Initialization`
með 0 % skráa (27.8.2026). Uppskeran sjálf er sótt utan Alma og lesin inn sem
skrár á `try_A`-sniði (bert `<ListRecords>`, engin `<?xml?>`-lína, ekkert
`xmlns` á rótinni).

## Umfang

| | Fjöldi |
|---|---:|
| Bæir (`type:baer`) | **17.371** |
| Einstaklingar (`type:einstaklingur`) | **223.795** |
| Manntalsfærslur (`type:m:einstaklingur`) | **982.488** hjá uppruna, **315.734** sóttar |
| Allt settið `source:smb` | **1.223.654** |
| Í `smb.db` eftir uppskeru | 556.900 |
| Lesið inn í Leitir (mælt 14.9.2026) | **241.212** |
| Þar af fólk / staðir (mælt 9.9.2026) | 223.828 / 17.384 |

Talan 241.212 er 17.371 bæir + 223.795 einstaklingar + 46 eldri prófunarfærslur.
Manntalsfærslurnar (`type:m:einstaklingur`) eru **ekki** lesnar inn; uppskera
þeirra stöðvaðist á HTTP-timeout 1.7.2026.

## Reitir sem berast

Þekja mæld 25.6.2026 á hreinsuðum úrtökum: 100 bæir og 200 einstaklingar.

| DC-reitur | Bæir | Einstaklingar | Dæmi um gildi | Athugasemd |
|---|---:|---:|---|---|
| `dc:title` | 100 % | 100 % | `Eiði` · `Guðrún Jónsdóttir` | `xml:lang="is"`, 1× |
| `dc:type` | 100 % | 100 % | `Bær`/`Place` · `Einstaklingur`/`Person` | Par `@is`+`@en`, 2× |
| `dc:subject` | 100 % | 100 % | `Bær` · `Einstaklingur` | Eitt gildi; tegundarmerki, ekki efni |
| `dc:identifier` | 100 % | 100 % | `oai:smb.mshl.is:baer:1` + `https://smb.mshl.is/baer/1` | 2×: OAI-auðkenni og slóð |
| `dc:coverage` | 100 % | 98 % | Bær: `Sókn: Eyrarsókn`, `Hreppur: …`, `Sýsla: …` · Fólk: `Heimili: Skálholt, Skálholtssókn, Biskupstungnahreppur, Árnessýsla` | Allt að 5 gildi á bæ, 2 á mann. **Ólík bygging** eftir tegund |
| `dc:date` | 100 % | 100 % | `1703/1910` · `1660` | Bær: EDTF-bil. Maður: eitt ártal |
| `dc:source` | 100 % | 100 % | `1703: Manntal` · `1847: Jarðatal á Íslandi` + slóð | Allt að 17 gildi á bæ, 5 á mann. 116 ólík gildi í bæjaúrtakinu |
| `dcterms:spatial` | 100 % | 98 % | `POINT(-22.898 65.964)` | 55 af 100 bæjum bera strenginn `None` |
| `dc:relation` | tómt | 60 % | `oai:smb.mshl.is:m:einstaklingur:84321` | Allt að 7 á mann; auðkenni, ekki nöfn |
| `dc:creator` | 100 % | 100 % | `Miðstöð stafrænna hugvísinda og lista` | Eitt einstakt gildi |
| `dc:contributor` | 100 % | 100 % | `ad libitum ehf` | Eitt einstakt gildi |
| `dc:publisher` | 100 % | 100 % | `Sögulegt mann- og bæjatal` | Eitt einstakt gildi |
| `dc:description` | 100 % | — | `Eiði í Sögulegu mann- og bæjatali` | Leidd af titlinum |
| `dc:rights` | 100 % | 100 % | CC-BY 4.0 | Eitt einstakt gildi |
| `dc:language` | 100 % | 100 % | `is` | Eitt einstakt gildi |
| `dc:format` | tómt | — | `<dc:format></dc:format>` | Tómt svið á öllum bæjum í úrtakinu |

## Kortlagning í Leitir

Reglusettið heitir `SMB_XML_Processes` (22 reglur, Type XML). Útgáfan með
forskeytaklippingu og þáttun `Heimili:`-strengsins,
`SMB_XML_Processes-v2-forskeyti`, er 89 reglur.

| DC-reitur | PNX-svið | Hlutverk |
|---|---|---|
| `dc:title` | `dc.title` + `discovery.local1` | birting, leit |
| *(fast)* | `discovery.local5` = `SMB` | sía (gagnaveita) |
| *(fast)* | `dcterms.source` = `XDS` | umfangssía |
| `dc:type[@xml:lang='en']` = `Place` / `Person` | `discovery.resourceType` = `places` / `people` | sía, birting |
| sama | `discovery.local2` = `place` / `person` | sía |
| `dc:coverage` sem byrjar á `Sókn:` | `discovery.local23` | sía |
| `dc:coverage` sem byrjar á `Hreppur:` | `discovery.local24` | sía |
| `dc:coverage` sem byrjar á `Sýsla:` | `discovery.local25` | sía |
| `dc:coverage` sem byrjar á `Heimili:` (fólk) | þáttað í `local23` / `local24` / `local25` | sía (v2) |
| `dc:coverage` (öll gildi) | `dc.coverage` | leit |
| `dc:source` sem er ekki http | `discovery.local26` (Heimild) | birting |
| `dcterms:spatial` | `discovery.local27` | birting |
| `dc:identifier` sem byrjar á http | `dcterms.source` + `dc.identifier` | tengill heim |
| `dc:relation` sem byrjar á http | `discovery.local31` | birting |
| `dc:subject` | `dc.subject` + `discovery.local3` | leit, sía |
| `dc:type` · `dc:date` · `dc:description` · `dc:language` · `dc:publisher` · `dc:rights` | sömu svið | birting, leit |

Vísvitandi ekki varpað: `dc:creator` og `dc:contributor`. Bæir og manntalsfólk
hafa engan höfund, og gildin tvö eru föst á öllum færslum.

## Þekkt frávik

1. **`/oai` án skástriks skilar 301 með tómum bol.** Auglýsta slóðin í `Identify`
   er án skástriks. Þetta felldi uppskerujobbið 26.8.2026 með
   `Premature end of file`; slóðin með skástriki skilar 200 og réttu svari.
2. **HTTP-svarið ber ekki `charset=UTF-8`.** Gögnin eru rétt UTF-8 en hausinn
   segir aðeins `Content-Type: text/xml`, svo viðtakandi giskar á ISO-8859-1 og
   íslenskir stafir brenglast í birtingu (skráð 3.6.2026).
3. **`dc:source` er tvírætt.** Sama svið ber bæði heimildaskrá (`1703: Manntal`,
   allt að 17 gildi á bæ) og slóð færslunnar. Sviðið er því ekki nothæft beint
   sem tengill heim.
4. **`dc:date` er strengurinn `None`** á 611 af 17.371 bæjum (3,52 %, mælt
   1.9.2026). Þetta er texti sem fer í vísinn sem dagsetning.
5. **`dcterms:spatial` = `None`** á 55 af 100 bæjum í úrtakinu (25.6.2026). Á
   öllu settinu bera 91,9 % færslna raunhnit (mælt 1.9.2026).
6. **`dc:coverage` ber forskeyti** (`Sýsla: Ísafjarðarsýsla`), sem gefur óhrein
   síugildi. Staður er auk þess marggildur: af 1.000 bæjum bera 18,6 % fleiri en
   eina sókn, 21,9 % fleiri en einn hrepp og 23,9 % fleiri en eina sýslu (mælt
   1.9.2026). Eiði ber bæði `Ísafjarðarsýsla` og `Norður-Ísafjarðarsýsla`.
7. **Staðurinn er byggður á tvo ólíka vegu eftir færslutegund.** Bær gefur þrjú
   stök (`Sókn:` · `Hreppur:` · `Sýsla:`), maður gefur einn samsettan streng
   (`Heimili: bær, sókn, hreppur, sýsla`) — 63.967 eindir á 27.992 færslum,
   100 % með `Heimili:`. Afleiðing: 223.828 einstaklingar voru utan staðsíanna
   þar til strengurinn var þáttaður.
8. **Stofnanir í `dc:creator`/`dc:contributor`** á öllum færslum, eitt einstakt
   gildi hvort. Höfunda-sía á gagnaveitunni hefur nákvæmlega einn flokk.
9. **`dc:description` er leidd af titlinum** (`<titill> í Sögulegu mann- og
   bæjatali`) — 100 % þekja, engin upplýsing umfram titilinn.
10. **Tóm svið og tómar færslur.** `<dc:relation/>` og `<dc:format/>` eru tóm á
    öllum bæjum í úrtakinu, og um 12 % bæja voru tómar færslur án lýsigagna
    (skráð 3.6.2026).
11. **Settin leka.** `type:einstaklingur` og `type:m:einstaklingur` skiluðu um
    90 % bæjafærslum þegar þau voru mæld (25.6.2026) — `setSpec`-síun heldur ekki
    og þurfti að sía forritunarlega á `dc:type`.
12. **`dc:relation` ber tvennt ólíkt** hjá fólki: 748.474 tilvísanir í manneskjuna
    sjálfa í hverju manntali og 130.719 tengsl við aðrar manneskjur. Gildin eru
    auðkenni, ekki nöfn, svo ekki er hægt að leita að tengslum eftir nafni.

## Hvað við gerum við þau

- **Skráarinnlestur** í stað lifandi OAI, á tveimur prófílum með sitt hvora
  Delivery-regex: bæir (`https://smb.mshl.is/baer/.*`) og fólk
  (`…/einstaklingur/.*`). Fari skrá í rangan prófíl fær færslan engan tengil og
  villan sést hvergi í keyrsluskýrslunni, aðeins á færslusíðunni.
- **Tengillinn** er tekinn úr `dc:identifier` sem byrjar á `http`, ekki úr
  `dc:source`, svo tvíræðni sviðsins stöðvi okkur ekki.
- **Forskeyti** eru klippt í reglunni eftir að hún hefur ratað á þeim; fjöldi
  ítrana er settur eftir mældu hámarki (8 sóknir, 8 hreppar, 6 sýslur).
- **`Heimili:`-strengurinn** er þáttaður aftan frá í sömu svið og bæirnir nota,
  svo ein sýslusía nái bæði bæjum og fólki. Mælt á 129.447 stökum: 99,3 % bera
  fjóra hluta, 0,13 % skekkja þar sem bæjarnafn ber kommu.
- **`dc:creator`/`dc:contributor`** eru ekki varpaðar.
- **`dc:date` = `None`** er ekki síað í gildandi reglu (611 bæir berast óbreyttir);
  sían er til í reglusetti annarrar gagnaveitu og á eftir að flytjast hingað.
- **FRBR-samruni** fellir saman samnefnda einstaklinga (`Jón Jónsson` 193 í vísi
  á móti 3.050 í gagnagrunninum). Bælingarregla nær yfir þessa gagnaveitu.

# Safn RÚV

Útvarps-, sjónvarps- og tónlistarsafn Ríkisútvarpsins. Lýsigögnin koma úr
safnkerfi RÚV (CGI DIRA). RÚV á enga OAI-PMH veitu, svo afhendingin er
XML-útflutningur sem við umbreytum í gullna sniðið.

> RÚV er að hefja innleiðingu á nýju safnkerfi; útflutningurinn mun líta
> öðruvísi út í framtíðinni. Umbreytingin hér er fyrir sýnishornin.

## Afhending

| | |
|---|---|
| Form | ein XML-skrá á hverja færslu, rót `EXPORT/TAKE` |
| Sýnishorn | 14 skrár, 28.9.2026 (Bergþóra Ólöf Björgvinsdóttir, RÚV) |
| Skráarheiti | `<PARENT_ID>_<GENE_ID>.xml`; `00000000` = á ekkert foreldri |
| Kortlagning | [KORTLAGNING-RUV.md](KORTLAGNING-RUV.md), frá RÚV 25.9.2026 |
| OAI-PMH | ekkert — **sýnisveita** hýst í Gáttagægi: `/veitur/ruv/oai` |
| Færslusíða | `https://sagnatrog.kann.is/ruv/<GENE_ID>` — hýst í Gáttagægi, t.d. [Kastljós 4.7.2008](https://sagnatrog.kann.is/ruv/8270C1E3) |

## Umfang sýnishornanna

| Tegund | Foreldri | Börn | Stakt | `dc:type` |
|---|---:|---:|---:|---|
| Tónlist | 1 (upptaka) | 5 (lög) | — | Tónlistarupptaka, Lag / SoundRecording |
| Útvarp | — | — | 2 | Útvarpsþáttur / SoundRecording |
| Sjónvarp | 1 (þáttur) | 4 (innslög) | 1 | Sjónvarpsþáttur, Sjónvarpsinnslag / MovingImage |

## Kortlagning í gullna sniðið

| Gullið DC | Úr RÚV | Athugasemd |
|---|---|---|
| `dc:identifier` | færslusíða `https://sagnatrog.kann.is/ruv/<GENE_ID>` fyrst, síðan `oai:ruv.is:safn:<GENE_ID>` + safnnúmer (`GENE_CENTRAL_ARCHIVE00`) | RÚV á enga opna slóð á færslu; Sagnatrogið gefur hana |
| `dc:title` | `GENE_TITLE` | |
| `dc:type` (par) | `GENE_TYPE` + `GENE_FUNCTION` | foreldri og barn fá ólík heiti |
| `dc:date` | upptökudagur, annars fyrsta útsending, annars ár úr `GENE_PUB_TIME` | börn erfa dag foreldris |
| `dcterms:created` · `dcterms:issued` | upptökudagur · útsendingardagar (`TX_HISTORY`) | |
| `dc:subject` + `mshl:id` | `DESCRIPTORS/NAME` + `DESC_ID` | varanleg auðkenni efnisorða ✅ |
| `dc:subject` `ruv:dagskrarflokkur` | `GENE_PRG_TYPE` | Fréttir, Samfélagsmál, Skemmtiefni … |
| `dc:creator` · `dc:contributor` + `mshl:role` | `TAKE_PERSONS` + `PMAP_SUBFUNC` | 41 hlutverk á íslensku; höfundar, flytjendur, umsjón → creator |
| `dcterms:bibliographicCitation` | nafn (hlutverk; starf úr `PERSON_INFO`) | fyrir hlutverkasíuna í Leitir |
| `dcterms:isPartOf` · `dcterms:hasPart` | `PARENT_ID` ↔ `GENE_ID` | plata ↔ lög, þáttur ↔ innslög |
| `dc:description` | `BTX_USERTEXT10` | innri vinnulínur og kennitölur fjarlægðar |
| `dc:relation` | `https://www.ruv.is/um-ruv/safn-ruv` | beiðnasíða safnsins |
| `dc:source` · `dc:format` · `dcterms:extent` | `GENE_ARCHIVE00` · `GENE_REMARK` · `GENE_LENGTH` | frumeintak, miðill, lengd |

## Persónuvernd — þrjár reglur í umbreytingunni

1. **`PERSON_ALT_NAME` er kennitala** og er aldrei lesin.
2. **Kennitölur í frjálsum texta eru fjarlægðar.** Þær koma fyrir: lýsingartexti
   eins sjónvarpsþáttar í sýnishornunum bar framleiðsluskýrslu með kennitölum.
3. **Fæðingarár lifandi fólks fara ekki út.** Æviár birtast aðeins þegar
   dánarár er skráð. Það nær líka yfir börn sem koma fram í barnaefni.

Umbreytingin sannprófar sjálf að engin kennitala sé í úttakinu og skrifar
ekkert ef hún finnur eina.

## Mælt með Gáttagægi (28.9.2026)

40 athuganir standast. Tvennt vantar, og hvort tveggja er ákvörðun RÚV:

| | Hvað | Hvers vegna skiptir það máli |
|---|---|---|
| 🔴 villa | engin varanleg opin slóð á færslu | færslan getur ekki vísað heim; tengillinn fer á beiðnasíðu safnsins |
| ábending | engin opin smámynd | smámyndir eru til í safnkerfinu en ekki á opinni slóð |

Villan er leyst með færslusíðum Sagnatrogsins (í loftinu 28.9.2026). Hver
færsla hefur opna, varanlega slóð sem sýnir lýsinguna og vísar áfram á
beiðnasíðu Safns RÚV.

## Skörun við ruv.is (mælt 28.9.2026)

Leitin á ruv.is leitar í fréttagreinum, að mestu frá 2010 og síðar, ekki í
safninu. Spilari RÚV geymir aðeins nýlegt efni. Af sýnishornunum 14:

| Færslur | Á ruv.is |
|---|---|
| Sögur 2018 | sama myndskeið í [frétt 22.4.2018](https://www.ruv.is/frettir/menning-og-daegurmal/verdlaunaafhendingin-sogur-i-horpu), opin skrá og mynd |
| 3 innslög og lög | sama fólk í síðari fréttum, ekki sama efni |
| Morgunútvarpið 28.5.2024 | fréttir sama dag um sömu mál, ekki úr þættinum |
| Kastljós 2008, lög 1983, Fréttir kl. 11 | ekkert |

Myndskeið á ruv.is ber eigið númer. Ef safnkerfið veit hvaða myndskeið
tilheyrir hverri færslu fær allt birt efni opna slóð á efnið sjálft.

## Opið

- Hvað af lýsigögnum RÚV má birtast opinberlega? Spurt 24.9.2026, ósvarað.
- Hvernig verða foreldri og börn í nýja safnkerfinu?
- Veit safnkerfið hvaða myndskeið á ruv.is tilheyrir hverri færslu?

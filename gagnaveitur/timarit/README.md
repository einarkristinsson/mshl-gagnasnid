# Tímarit.is

Stafrænt safn blaða og tímarita hjá Landsbókasafni Íslands – Háskólabókasafni.
Tímarit.is á opna OAI-PMH gagnaveitu. Í henni er hver færsla **titill** —
blað eða tímarit — en ekki tölublað eða grein. Við færum titlana í gullna
sniðið, bjóðum þá sem sýnisveitu og lesum þá inn í Alma.

## Afhending

| | |
|---|---|
| Endapunktur | `https://timarit.is/oai` — án skástriks |
| `baseURL` í `Identify` | `http://timarit.is/oai`, sem vísar með 301 á https |
| Snið | aðeins `oai_dc` |
| Sett | engin |
| Eyddar færslur | `deletedRecord=no` |
| `adminEmail` | kristinn@landsbokasafn.is |
| Umfang | 2.011 titlar á einni síðu (1,8 MB), enginn `resumptionToken` |
| Umbreyting | [`byggja_timarit_dc.py`](byggja_timarit_dc.py) — sækir, umbreytir, sannprófar |
| Afurð | [`TIMARIT-tryA.xml`](TIMARIT-tryA.xml) — 2.011 færslur, 2,4 MB, fyrir `Upload File/s` í Alma |
| Reglusett | [`TIMARIT_XML_Processes.drl`](TIMARIT_XML_Processes.drl) — 14 reglur |
| Innlestur | [`PLAYBOOK-innlestur.md`](PLAYBOOK-innlestur.md) |
| Sýnisveita | `https://oai.kann.is/timarit` eftir næstu uppsetningu Gáttagægis |

Allar tölur mældar 29.9.2026.

## Umfang

| | Titlar |
|---|---:|
| Allir | 2.011 |
| Útgáfutími er bil (`Published from 1933 to 1948`) | 1.169 |
| Kom út eitt ár (`Published in 1852`) | 677 |
| Kemur enn út (`Published from 1949 to present`) | 165 |
| Með útgefanda | 449 (589 útgefendur alls) |
| Með íslenskri lýsingu umfram titilinn | 1.891 |

Tungumál: íslenska 1.952 · færeyska 20 · enska 18 · danska 14 · grænlenska 5 · þýska 2.

## Kortlagning í gullna sniðið

| Gullið DC | Úr Tímarit.is | Athugasemd |
|---|---|---|
| `dc:identifier` (slóð) | `dc:identifier` `http://timarit.is/publication/<n>` | fer út sem `https://…`; sjá „Slóðin heim“ |
| `dc:identifier` (auðkenni) | OAI-auðkennið `oai:timarit.is:publications/<n>` | kemur á eftir slóðinni |
| `dc:title` `@is` | `dc:title` | bil samræmd. Alltaf `@is` eins og gullna sniðið krefst, líka á færeyskum og dönskum titlum |
| `dc:type` (par) | fast: `Tímarit` `@is` + `Text` `@en` | `text` og `series` úr heimildinni falla niður. `Text` → `local2` journal, `resourceType` journals |
| `dc:date` | enska lýsingin | `1933/1948` · `1852` · `1949/..` (EDTF, opinn endi = kemur enn út) |
| `dc:description` `@is` | útgáfutíminn + íslenska lýsingin | sjá „Lýsingin“ |
| `dc:subject` | fast `Tímarit og blöð` `@is` + `Serials` `@en` úr heimildinni | gullna sniðið leyfir `@en` með. Aðeins `@is` fer í síuna (`local93`) |
| `dc:language` | `dc:language` | ISO 639-2 → 639-1: `isl`→`is`, `fao`→`fo`, `kal`→`kl`, `dan`→`da`, `eng`→`en`, `deu`→`de` |
| `dc:publisher` `@is` | `dc:publisher` | nafnið án ártala: „Niels Winther, 1852-1852“ → „Niels Winther“. Sama nafn aðeins einu sinni á titli |
| `dc:rights` `@is` | fast | „Lýsigögnin eru frá Tímarit.is, vef Landsbókasafns Íslands – Háskólabókasafns.“ |
| `datestamp` | `datestamp` | óbreyttur, svo `from`/`until` virka í sýnisveitunni |
| `setSpec` | fast `source:timarit` | |
| — | enska lýsingin sjálf | fer ekki út sem texti. Efni hennar er í `dc:date` og í íslensku setningunni |

**Slóðin heim.** `https://timarit.is/publication/<n>` svarar 302 og vísar á
fyrstu síðu titilsins (`/page/<n>`). `http://` vísar fyrst með 301 á https og
svo með 302. Mælt á fimm titlum (og tíu í Gáttagægi); https sparar eitt
stökk og endar á sömu síðu. Tengillinn virkar í vafra. Við fundum enga
titilsíðu sem svarar 200.

**Lýsingin.** Fremst kemur útgáfutíminn á íslensku: „Kom út 1933–1948.“,
„Kom út árið 1852.“ eða „Hefur komið út frá árinu 1949.“ Á eftir kemur lýsing
Tímarit.is óbreytt, að þrennu frátöldu:

- Henni er sleppt þegar hún er aðeins titillinn (115 titlar) eða „Lýsingu vantar“ (4).
- MARC-merki eins og `|b` og `|c` eru tekin út (70 lýsingar):
  „Reykjavík : |b Handbækur, |c 1967“ → „Reykjavík : Handbækur, 1967“.
- Bil og línuskil eru samræmd.

Einn titill hefur tóma íslenska lýsingu og fær aðeins útgáfutímann. Lýsingar
færeyskra blaða eru stundum á færeysku; merkingin `@is` úr heimildinni helst.

**Árin við útgefendur falla niður.** Þau segja hvenær útgefandinn gaf titilinn
út, ekki hvenær titillinn kom út. Í `dcterms:temporal` yrðu þau að tímabili
titilsins, og það eru þau ekki. Nafn án ártala sameinast líka milli
titla: 64 útgefendur eiga fleiri en einn titil. Árin sjást áfram á Tímarit.is.
Í leiðbeiningunum má `dc:publisher` vera „safnið eða útgefandinn“; hér er það
útgefandinn, því hann er þekktur.

## Mælt með Gáttagægi

Sama athugun á endapunkti Tímarit.is og á sýnisveitunni (29.9.2026).

| | `https://timarit.is/oai` | Sýnisveitan |
|---|---:|---:|
| Villur | 7 | 1 |
| Aðvaranir | 3 | 2 |
| Ábendingar | 3 | 2 |
| Stóðst | 27 | 37 |
| Sleppt | 5 | 3 |

Það sem sýnisveitan lagar:

| Athugun | Tímarit.is | Sýnisveitan |
|---|---|---|
| E02 `baseURL` virkar orðrétt | auglýst `http://` svarar 301 | ✅ |
| E03 GET og POST | POST svarar 403 | ✅ |
| E13 `from`/`until` sía | síunni er ekki beitt | ✅ |
| F04 `dc:type` sem par | `text` og `series` án `xml:lang` | ✅ `Tímarit` / `Text` |
| F08 `dc:rights` | vantar | ✅ |
| H06 engir tómir reitir | ein tóm lýsing | ✅ |

Það sem eftir stendur:

| Athugun | Alvarleiki | Hvers vegna |
|---|---|---|
| F03 slóðin svarar 200 | villa | titilslóðin svarar 302 á fyrstu síðu titilsins |
| F06 staðarreitur | aðvörun | straumurinn ber ekki útgáfustað |
| F10 `dc:publisher` | aðvörun | 1.562 titlar án útgefanda í heimildinni (173 af 300 í sýninu) |
| F07 smámynd | ábending | straumurinn ber enga mynd |
| G06 auðkenni efnisorða | ábending | „Tímarit og blöð“ er fast gildi frá okkur, ekki orð úr orðaforða |

## Það sem straumurinn gefur ekki

- **Engin tölublöð og engar greinar.** Leit í Leitir finnur blaðið, ekki efnið í því.
- **Ekkert fólk.** Hvorki ritstjórar né höfundar; útgefandi aðeins á 449 titlum.
- **Enginn staður.** Útgáfustaður er ekki í straumnum. Hann sést þó á titlalista
  Tímarit.is („Ísland 1919-1998“) og stendur stundum í lýsingunni
  („Reykjavík : Handbækur, 1967“).
- **Engin mynd.** Titlalistinn sýnir forsíðumynd hvers titils, en slóðin á hana
  er ekki í straumnum.
- **Engin efnisorð umfram „Serials“.** Sumar lýsingar eru í raun efnisorð
  („Stjórnmál. Verkalýðsmál.“). Þær eru ekki þáttaðar.

## Spurningar til Kristins Sigurðssonar

1. Er til OAI-gagnaveita eða API fyrir tölublöð eða greinar? Titlarnir einir
   segja lítið um efnið.
2. Getur OAI-færsla titils borið útgáfustað, slóð á forsíðumynd og slóð á
   titilsíðu sem svarar 200? Allt þetta er þegar á titlalistanum (`/titles`).
3. Getur `Identify` auglýst `https://timarit.is/oai` og endapunkturinn beitt
   `from`/`until`? Þá þarf ekki að sækja alla titlana við hverja uppfærslu.

## Smíða aftur

```bash
python3 gagnaveitur/timarit/byggja_timarit_dc.py              # sækir og skrifar báðar skrárnar
python3 gagnaveitur/timarit/byggja_timarit_dc.py hratt.xml    # úr vistuðu svari (--vista hratt.xml)
python3 -m unittest discover -s gagnaveitur/timarit           # prófanir umbreytingarinnar
```

Umbreytingin prentar öll mynstur í ensku lýsingunni sem hún þekkir ekki.
Þann 29.9.2026 voru þau engin.

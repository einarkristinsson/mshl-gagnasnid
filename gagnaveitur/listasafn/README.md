# Listasafn Íslands

Vefur Listasafns Íslands (listasafn.is) er byggður á efnisstjórnunarkerfinu
Prismic, og allt birt efni er opið í vefþjónustu þess. Þaðan lesum við
**sýningar** og **listamannasíður**, færum í gullna sniðið, bjóðum sem
sýnisveitu og lesum inn í Alma. Ekkert þarf að breyta hjá Listasafni.

## Afhending

| | |
|---|---|
| Heimild | `https://listasafn-islands.cdn.prismic.io/api/v2` — opin vefþjónusta Prismic (REST), íslenska útgáfan |
| OAI-PMH | ekkert hjá Listasafni — **sýnisveita** á <https://oai.kann.is/listasafn> eftir næstu uppsetningu |
| Tengiliður | Sigurður Gunnarsson, fagstjóri tækni og ljósmyndunar; þjónustuaðili vefsins er Kolibri |
| Umbreyting | [`byggja_listasafn_dc.py`](byggja_listasafn_dc.py) — sækir, umbreytir, sannprófar |
| Afurð | [`LISTASAFN-tryA.xml`](LISTASAFN-tryA.xml) — 128 færslur fyrir `Upload File/s` í Alma |
| Reglusett | [`LISTASAFN_XML_Processes.drl`](LISTASAFN_XML_Processes.drl) — 19 reglur |
| Innlestur | [`PLAYBOOK-innlestur.md`](PLAYBOOK-innlestur.md) |

Allar tölur mældar 1.10.2026.

## Umfang

| Prismic-tegund | Skjöl (is) | Í Sagnatroginu |
|---|---:|---|
| `exhibition` — sýning | 124 | ✅ ein færsla hver |
| `art_artist_page` — listamannasíða | 4 | ✅ Ásgrímur Jónsson, Einar Jónsson, Jóhannes Kjarval, Valtýr Pétursson |
| `artwork` — verk | 1.139 | ❌ aðeins titill og stundum mynd (21 %); hvorki listamaður né ártal |
| `event` — viðburður | 554 | ❌ viðburðir safnsins, ekki menningarefni í sjálfu sér |

## Kortlagning í gullna sniðið

| Gullið DC | Sýning | Listamaður | Athugasemd |
|---|---|---|---|
| `dc:identifier` (slóð) | `https://www.listasafn.is/list/syningar/<uid>/` | `…/list/listamenn/<uid>/` | íslenskir stafir í auðkenni hlutfallskóðaðir |
| `dc:identifier` (smámynd) | aðalmynd, 400 px frá myndþjónustu Prismic | sama | 128 af 128 |
| `dc:title` | `title` | `title` (nafn) | |
| `dcterms:alternative` | `artist` þegar hann er ekki nafn | — | 35 sýningar, t.d. „Samsýning“, „Íslensk grafík“ |
| `dc:type` (par) | Sýning / Event | Einstaklingur / Person | |
| `dc:date` | `start_date`/`end_date` (EDTF bil) | fæðingar- og dánarár | |
| `dc:creator` + `mshl:role` | `artist` þegar hann er nafn + listamannalisti sýningar | — | hlutverk „listamaður“; 234 ólík nöfn |
| `dcterms:bibliographicCitation` | „Nafn (listamaður)“ | — | fyrir hlutverkasíuna |
| `dc:subject` | „Myndlistarsýningar“ + efnisorð úr `keywords` | „Myndlistarmenn“ | aðeins orð með lágstaf fremst; nöfn og ártöl eru annars staðar |
| `dc:description` | textahlutar síðunnar | inngangur + meginmál | |
| `dc:coverage` | safnið (`museum`) | — | t.d. Listasafnið við Tjörnina, Safnahúsið |
| `dc:relation` | — | „Sarpur, aðili <nr>“ | Sarpsnúmer listamannsins |
| `dc:publisher` · `dc:language` · `dc:rights` | Listasafn Íslands · is · réttindayfirlýsing | sama | |

## Reglur um fólk

1. **Reiturinn `artist` verður höfundur aðeins ef hann lítur út eins og nöfn:**
   engin orð með lágstaf fremst og ekki „Samsýning“ eða „Safneignarsýning“.
   Annars verður hann undirtitill.
2. **Listamannalisti sýningar** er traustasta heimildin og bætist alltaf við.
3. **Fæðingarár lifandi listamanna fara ekki út.** Æviár birtast aðeins ef
   dánarár er skráð (sama regla og hjá RÚV). 94 fæðingarár fjarlægð.
4. **„Óþekktur listamaður“** er ekki manneskja og fer ekki í fólkssíuna.

## Mælt með Gáttagægi (1.10.2026, staðbundið)

**40 athuganir standast. Engar villur og engar viðvaranir.** Þrjár ábendingar:

| Ábending | Hvers vegna |
|---|---|
| G05 staðanafn í þágufalli | heiti safns, t.d. „Safnasafnið á Svalbarðseyri“ — rétt eins og það er |
| G06 efnisorð án auðkennis | efnisorð Listasafns eru frjáls orð án orðaforða |
| G09 `Event` óþekkt | leiðrétt í Gáttagægi: `Event` er DCMI-tegund |

## Fyrir rannsóknarhugmyndina um nafnmyndir

Sama manneskja birtist undir fleiri en einu nafni: „Edvard Munch“ og „Edward
Munch“, „Jóhannes Kjarval“ og „Jóhannes S. Kjarval“, „Valgerður Briem“ og
„Valgerður Þorsteinsdóttir Briem“. Listamannasíðurnar bera Sarpsnúmer, sem er
fast auðkenni til að tengja þessi afbrigði.

## Ákveðið

Vefþjónusta Prismic er opin og við lesum beint úr henni (Einar, 2.10.2026).

## Opið

1. Fá verkin listamann og ártal síðar? Þá væru þau mikils virði í samleit.
2. Bætast fleiri listamannasíður við? Sigurður nefndi 28.9 að listamönnum fjölgi.

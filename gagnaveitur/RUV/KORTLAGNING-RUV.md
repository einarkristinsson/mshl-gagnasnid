# RÚV — kortlagning safnakerfis → leitarsvið

Frá Bergþóru Ólöfu Björgvinsdóttur (RÚV), póstur 25.9.2026 kl. 10:20,
„Re: Vefgátt MSHL og RÚV — prufuskrá". Orðrétt, að frátalinni uppsetningu.

> Athugið að við erum að hefja innleiðingu á nýju safnakerfi svo gögnin munu
> líta öðruvísi út í framtíðinni.

## Svið

| Það sem við báðum um | Svið í útflutningi RÚV | Athugasemd |
|---|---|---|
| titill | `EXPORT>TAKE>GENERIC>GENE_TITLE` | |
| slóð á vefslóð, opin án innskráningar | ekki til | hægt að bóka tíma og óska eftir efni á www.ruv.is/safn |
| tegund | `EXPORT>TAKE>GENERIC>GENE_TYPE` | `TYPE$MUSIC#Music` = tónlist · `TYPE$GENERIC#Generic` = sjónvarp · `TYPE$WORD#Word` = útvarp |
| dagsetning | `EXPORT>TAKE>GENERIC>GENE_PUB_TIME` | útgáfudagsetning |
| lýsing eða útdráttur | `EXPORT>TAKE>BASIC_TEXT>BTX_USERTEXT10` | |
| efnisorð | `EXPORT>TAKE>DESCRIPTORS` | |
| fólk | `EXPORT>TAKE>TAKE_PERSONS` | |
| smámynd | ekki til | |

## Fólk (`TAKE_PERSONS`)

| Svið | Merking | Birta? |
|---|---|---|
| `PERSON_NAME` | nafn | já |
| `PERSON_ALT_NAME` | **kennitala** | 🔴 **ALDREI** — persónuupplýsingar, síað út í umbreytingu |
| `PMAP_SUBFUNC` | hlutverk/starf, `PERSON_FUNC$<KÓÐI>` | já, íslenskt heiti úr töflunni hér að neðan |

## Foreldri og börn

Efni stendur annaðhvort eitt og sér eða á foreldri; skrá er til fyrir bæði
foreldrið og öll börnin (t.d. er plata foreldri laganna á henni).

- `EXPORT>TAKE>GENERIC>GENE>PARENT_ID` — id foreldris
- `EXPORT>TAKE>GENERIC>GENE>GENE_ID` — id efnisins sjálfs (sést líka í skráarheiti)

## Hlutverk (`PMAP_SUBFUNC` = `PERSON_FUNC$` + kóði)

| Kóði | Hlutverk |
|---|---|
| PERFORMER | Flytjandi |
| SONGWRITER_COMPOSER | Lagahöfundur/tónskáld |
| CONDUCTOR | Stjórnandi |
| LYRICIST | Textahöfundur |
| ARRANGER_OF_VOCALS | Raddsetning |
| BALANCE ENGINEER | Hljóðmeistari |
| SOUND_ENGINEER | Tónmeistari |
| DIRECTOR | Umsjónarmaður |
| PARTICIPANT | Þátttakandi |
| PROGRAMME_PRODUCER | Dagskrárgerð |
| SUBJECT_OF_DISCUSSION | Umfjöllun |
| AUTHOR | Höfundur |
| INTRODUCER | Kynnir |
| CHOIR_DIRECTOR | Kórstjóri |
| ARRANGER | Útsetjari |
| TRANSLATOR | Þýðandi |
| TRANSCRIBER | Umritari |
| JOURNALIST | Fréttamaður |
| ACTOR | Leikari |
| PROGRAM_DIRECTOR | Leikstjóri |
| AUDIO_ENGINEER | Tæknimaður |
| PRESENTER | Þulur |
| CONSULTANT | Ráðgjafi |
| SCREENWRITER | Handritshöfundur |
| DOCUMENTER | Skrásetjari |
| PRODUCER | Stjórn upptöku |
| EDITOR | Ritstjóri |
| EDITORS | Ritstjórn |
| PRODUCTION_ASSISTANT | Aðstoð við dagskrárgerð |
| ASSISTANT_DIRECTOR | Aðstoðarleikstjóri |
| DANCER | Dansari |
| CHOREOGRAPHER | Danshöfundur |
| FILM_PRODUCER | Framleiðandi |
| PLAY_ADAPTATION | Leikgerð |
| PUBLISHER | Útgefandi |
| SOUND_MIXER | Hljóðvinnsla |
| EDITING | Klipping |
| SET_DESIGN | Leikmynd |
| VOICEOVER | Leikraddir |
| DRAWINGS | Teikningar |
| RADIO_PLAY_ADAPTOR | Útvarpsleikgerð |
| LANGUAGE_INTERPRETER | Táknmálstúlkur |

Athugið: `BALANCE ENGINEER` er með bili, ekki undirstriki, í listanum sem barst.

# Verkfæri

Forskriftir til að sækja og mæla OAI-safn. Hrein `python3` úr stýrikerfinu —
engin ytri söfn, ekkert `pip install`.

| Skrá | Hvað hún gerir |
|---|---|
| [`saekja-oai.py`](saekja-oai.py) | Sækir allt safnið með `ListIdentifiers` + `GetRecord` og skrifar JSONL. **Endurræsanleg** — sleppir því sem þegar er sótt |
| [`telja-efnisord.py`](telja-efnisord.py) | Telur efnisorð með auðkennum og skrifar TSV með uppsöfnuðu hlutfalli |
| [`gattagaegir/`](gattagaegir/) | **Gáttagægir** — vefverkfæri sem prófar OAI-PMH endapunkt gegn [gátlistanum](../oai-pmh/GATLISTI.md) og [gullna sniðinu](../snidmat/GULLNA-SNIDID.md). Límdu inn slóð, fáðu stóðst/villu-skýrslu. Sér um gildrurnar úr [LEIDBEININGAR](../oai-pmh/LEIDBEININGAR.md) |

## Af hverju `ListIdentifiers` + `GetRecord` en ekki `ListRecords`

`ListRecords` er rétta leiðin og hún er fljótari — 228 fyrirspurnir í stað
22.729. En hún hefur einn galla sem kemur fyrir í alvöru: **ein skemmd færsla
fellir alla gönguna.** Þegar það gerist er `ListRecords` ónothæft þar til
eigandinn lagar færsluna.

`ListIdentifiers` sækir aðeins hausana og fellur því ekki á skemmdu
lýsigagnasniði. `GetRecord` sækir svo hverja færslu fyrir sig: skemmda færslan
skilar villu, hinar 22.658 koma inn. Uppskeran tekur hálftíma í stað fimm
mínútna, en hún klárast í dag.

**Notaðu `ListRecords` fyrst.** Falli hún, skiptu yfir.

## Notkun

```bash
# 1. sækja auðkennin (skrifar ids.json)
curl -s "https://<safn>/oai?verb=ListIdentifiers&metadataPrefix=oai_dc" > p1.xml
#    eða láta saekja-oai.py um það

# 2. sækja allar færslur
/usr/bin/python3 saekja-oai.py          # -> raw.jsonl, villur.json

# 3. telja efnisorð
/usr/bin/python3 telja-efnisord.py      # -> efnisord-hrat.tsv
```

Slóð og `metadataPrefix` eru efst í `saekja-oai.py` (`B` og `metadataPrefix`).
Fjöldi samhliða tenginga er `THREADS = 6` — **ekki hækka það án þess að hugsa.**
Sex tengingar gáfu 13 fyrirspurnir á sekúndu á PHP-þjóni sem þoldi það vel;
tuttugu hefðu getað fellt hann.

## Kurteisi við þjóninn sem þú ert að sækja úr

- `User-Agent` sem segir hver þú ert og hvernig má ná í þig.
- Endurtaka með vaxandi bið (`1,5 s`, `3 s`, `4,5 s`), ekki í lykkju.
- Full uppskera einu sinni, svo `from`/`until` — ef veitan styður það.
- Láta eigandann vita ef þú finnur eitthvað brotið. Hann veit það oftast ekki.

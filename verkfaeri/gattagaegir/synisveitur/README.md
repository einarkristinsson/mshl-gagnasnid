# Sýnisveitur

Hver `<nafn>.xml` hér (gullið DC á `ListRecords`-formi) verður OAI-PMH 2.0
veita á **`https://oai.kann.is/<nafn>`** (og `/veitur/<nafn>/oai` á öðrum lénum
þjónustunnar). `<nafn>.json` gefur heiti, netfang, síðustærð og lýsingu.
Forsíða <https://oai.kann.is/> listar allar veiturnar.

Gagnaskrárnar sjálfar (`*.xml`) eru **ekki í git**: þær eru smíðaðar úr gögnum
gagnaeiganda sem hafa ekki samþykkt opna birtingu. Þær fara með í Cloud Run
(sjá `.gcloudignore` í rót safnsins) og eru smíðaðar með umbreytingum í
einkasafninu `leidarljos` (`dc-template/sources/<veita>/`).

Undantekningar eru Tímarit.is, Bækur.is og Listasafn Íslands: gögnin eru opin,
svo skrárnar eru líka í git sem
[`gagnaveitur/timarit/TIMARIT-tryA.xml`](../../../gagnaveitur/timarit/TIMARIT-tryA.xml),
[`gagnaveitur/baekur/BAEKUR-tryA.xml`](../../../gagnaveitur/baekur/BAEKUR-tryA.xml)
og [`gagnaveitur/listasafn/LISTASAFN-tryA.xml`](../../../gagnaveitur/listasafn/LISTASAFN-tryA.xml).
`byggja_timarit_dc.py`, `byggja_baekur_dc.py` og `byggja_listasafn_dc.py` skrifa
hver sínar tvær skrár.

| Veita | Slóð | Uppruni |
|---|---|---|
| RÚV | `https://oai.kann.is/ruv` | 312 sýnishorn frá Bergþóru Ólöfu Björgvinsdóttur, 28.9. og 30.9.2026 |
| Tímarit.is | `https://oai.kann.is/timarit` | 2.011 titlar úr opinni OAI-gagnaveitu Tímarit.is, sótt 29.9.2026 |
| Bækur.is | `https://oai.kann.is/baekur` | 2.984 stafrænar bækur úr opinni OAI-gagnaveitu Bækur.is (edm), sótt 1.10.2026 |
| Listasafn Íslands | `https://oai.kann.is/listasafn` | 124 sýningar og 5 listamannasíður úr opinni vefþjónustu Prismic á listasafn.is, sótt 2.10.2026 |
| Ævir lærðra manna | `https://oai.kann.is/aevir` | 2.801 lærður maður úr skrám Þjóðskjalasafns Íslands, unnið 30.9.2026; 1.383 með beinni slóð á opnuna og smámynd |
| Jarðaskrá | `https://oai.kann.is/jardir` | sýnishorn: 2.811 bæir í fimm sýslum og allar 133 bækur úr opinni OAI-gagnaveitu jardir.skjalasafn.is, sótt 4.9.2026; bókarslóðir leiðréttar úr `/baer/` í `/bok/` |
| Handrit.is | `https://oai.kann.is/handrit` | 142 handrit, úrval 2.9.2026 úr heildarútflutningi Landsbókasafns (júlí 2026) |
| Sögulegt mann- og bæjatal | `https://oai.kann.is/smb` | 40 einstaklingar úr opinni OAI-gagnaveitu smb.mshl.is, valdir 27.8.2026 |
| Ísmús og Sagnagrunnur | `https://oai.kann.is/ismus` | úrval: 1.000 sagnir, 1.000 hljóðrit og 1.000 einstaklingar úr sagnatrog-sniði Ísmús (opið, ismus.is/oai_pmh), sótt 6.10.2026 |

`ismus.xml` er `ismus/ISMUS-v2-SYNI-tryA.xml` úr `leidarljos/dc-template/sources/`,
smíðað með `byggja_ismus_sagnatrog_dc.py --syni 2000`; æviár fylgja aðeins látnum.

Ævir, Handrit.is og SMB eru afrit úr `leidarljos/dc-template/sources/`:
`aevir/AEVIR-menn-v3-tryA.xml`, `handrit/HANDRIT-DEMO-2026-09-02-tryA.xml` og
`smb/SMB-UNION-baer-folk-tryA.xml`. `jardir.xml` er `jardir/JARDIR-baer-ALL-tryA.xml`
og `jardir/JARDIR-bok-ALL-bokslod-tryA.xml` í einu `ListRecords`. Bæjunum er fækkað í fimm sýslur (Árnes-, Eyjafjarðar-, Gullbringu-, Rangárvalla- og Skagafjarðarsýslu) svo allar sýnisveiturnar rúmist í 256 MiB minni Cloud Run (öll skráin: um 198 MiB í ræsingu).

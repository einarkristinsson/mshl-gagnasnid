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
| Listasafn Íslands | `https://oai.kann.is/listasafn` | 124 sýningar og 4 listamannasíður úr opinni vefþjónustu Prismic á listasafn.is, sótt 1.10.2026 |

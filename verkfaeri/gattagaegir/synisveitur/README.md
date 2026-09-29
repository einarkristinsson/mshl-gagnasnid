# Sýnisveitur

Hver `<nafn>.xml` hér (gullið DC á `ListRecords`-formi) verður OAI-PMH 2.0
veita á **`https://oai.kann.is/<nafn>`** (og `/veitur/<nafn>/oai` á öðrum lénum
þjónustunnar). `<nafn>.json` gefur heiti, netfang, síðustærð og lýsingu.
Forsíða <https://oai.kann.is/> listar allar veiturnar.

Gagnaskrárnar sjálfar (`*.xml`) eru **ekki í git**: þær eru smíðaðar úr gögnum
gagnaeiganda sem hafa ekki samþykkt opna birtingu. Þær fara með í Cloud Run
(sjá `.gcloudignore` í rót safnsins) og eru smíðaðar með umbreytingum í
einkasafninu `leidarljos` (`dc-template/sources/<veita>/`).

Undantekning er Tímarit.is: gögnin eru opin, svo skráin er líka í git sem
[`gagnaveitur/timarit/TIMARIT-tryA.xml`](../../../gagnaveitur/timarit/TIMARIT-tryA.xml).
`byggja_timarit_dc.py` þar skrifar báðar skrárnar.

| Veita | Slóð | Uppruni |
|---|---|---|
| RÚV | `https://oai.kann.is/ruv` | 14 sýnishorn frá Bergþóru Ólöfu Björgvinsdóttur, 28.9.2026 |
| Tímarit.is | `https://oai.kann.is/timarit` | 2.011 titlar úr opinni OAI-gagnaveitu Tímarit.is, sótt 29.9.2026 |

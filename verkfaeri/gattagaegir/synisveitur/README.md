# Sýnisveitur

Hver `<nafn>.xml` hér (gullið DC á `ListRecords`-formi) verður OAI-PMH 2.0
veita á `/veitur/<nafn>/oai` í Gáttagægi. `<nafn>.json` gefur heiti, netfang,
síðustærð og lýsingu.

Gagnaskrárnar sjálfar (`*.xml`) eru **ekki í git**: þær eru smíðaðar úr gögnum
gagnaeiganda sem hafa ekki samþykkt opna birtingu. Þær fara með í Cloud Run
(sjá `.gcloudignore` í rót safnsins) og eru smíðaðar með umbreytingum í
einkasafninu `leidarljos` (`dc-template/sources/<veita>/`).

| Veita | Slóð | Uppruni |
|---|---|---|
| RÚV | `/veitur/ruv/oai` | 14 sýnishorn frá Bergþóru Ólöfu Björgvinsdóttur, 28.9.2026 |

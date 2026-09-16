# Gagnasnið

**Hvernig gagnaveita er afhent og hvernig hún ratar inn í Leitir.is.**

Þetta safn er unnið í Sagnatroginu — verkefni Miðstöðvar stafrænna hugvísinda
og lista um samþætta leitargátt fyrir íslensk menningarsöfn. Gögnin eru lesin
inn í Gegni og birtast í Leitir.is, sem Landskerfi bókasafna rekur.

Hér er tvennt:

**Fyrir þig sem átt gagnasafn** — hvernig þú afhendir efnið þitt svo það verði
leitanlegt við hliðina á öðrum söfnum. Byrjaðu á
[oai-pmh/LEIDBEININGAR.md](oai-pmh/LEIDBEININGAR.md).

**Fyrir þig sem átt að útfæra** — hvernig hver gagnaveita er byggð, hvað hún
skilar raunverulega og hvernig það kortleggst yfir í leitarvísinn. Byrjaðu á
[gagnaveitur/](gagnaveitur/).

---

## Efnisyfirlit

| Mappa | Hvað er þar |
|---|---|
| [`oai-pmh/`](oai-pmh/) | Hverju eiga gagnaveitur að skila? Kröfur til endapunktsins og gátlisti |
| [`snidmat/`](snidmat/) | Gullna Dublin Core-sniðið — reitur fyrir reit, með dæmum |
| [`gagnaveitur/`](gagnaveitur/) | Ein síða á hverja gagnaveitu: endapunktur, umfang, reitir, frávik |
| [`efnisord/`](efnisord/) | Sameiginlegu efnisflokkarnir og kortlagning orðaforða |
| [`verkfaeri/`](verkfaeri/) | Forskriftir til að sækja og mæla OAI-safn |

---

## Grunnhugmyndin í þremur setningum

Hvert safn heldur sínum gögnum og sínu vefviðmóti. Við sækjum **lýsigögnin** —
ekki hlutina sjálfa — með OAI-PMH, samræmum þau í eitt snið og gerum þau
leitanleg í einni gátt. Hver færsla ber tengil heim í upprunakerfið, svo
umferðin endar hjá eigandanum.

Það sem gerir þetta að **samleit** en ekki þremur listum í sama viðmóti eru
tvö svið: **efnið** (`dc:subject`) og **staðurinn** (`dc:coverage` /
`dcterms:spatial`). Titlar eru sjaldan eins milli safna; „Skarðsá" sem staður
og „Draugar" sem efni eru það.

---

## Meginreglur

1. **Eins mikið og hægt er í stöðluðu Dublin Core.** Aðlaganir ofan á, aldrei
   í staðinn. Sá sem les venjulegt `oai_dc` á að fá nothæfa færslu.
2. **Hrein gildi.** Flokkun fer í eigind, ekki í textann. `Rangárvallasýsla`,
   ekki `Sýsla: Rangárvallasýsla` — forskeytið rataði beint í síuna.
3. **Mælt, ekki áætlað.** Hver tala í þessu safni á sér mælingu á raungögnum
   og dagsetningu. Tölur fyrnast; dagsetningin segir hvenær.
4. **Frávik eru skráð hlutlægt.** Hvað mælist og hvaða afleiðingu það hefur.
   Gagnaeigandi á að geta lesið sína eigin síðu án þess að finnast hann kærður.
5. **Ekkert hér er trúnaðarmál.** Engin verð, engir samningar, engin persónugögn.

---

## Staða

Sex gagnaveitur mældar, fimm lesnar inn í prófunarumhverfi. Skjölunin er
uppfærð eftir hverja mælingu — sjá dagsetningar á hverri síðu.

*Síðast uppfært 16. september 2026.*

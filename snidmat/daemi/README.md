# Dæmi um gullnar færslur

Þrjár raunfærslur úr repo-inu, á gullna sniðinu ([`../GULLNA-SNIDID.md`](../GULLNA-SNIDID.md)).
Nafnrými eru sýnd einu sinni og `…` merkir reiti sem eru felldir brott til styttingar; öll gildi eru óbreytt.

**1 · Staður** — SMB-bær: staðarstigveldið liggur í eigindum, gildin eru hrein og hnitin fylgja.

```xml
<oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:mshl="https://mshl.is/terms#">
  <dc:identifier>https://smb.mshl.is/baer/1254</dc:identifier>
  <dc:title xml:lang="is">Stóraborg</dc:title>
  <dc:type xml:lang="is">Bær</dc:type>
  <dc:type xml:lang="en">Place</dc:type>
  <dc:subject xml:lang="is">Bær</dc:subject>
  <dcterms:spatial xsi:type="mshl:sokn" xml:lang="is">Eyvindarhólasókn</dcterms:spatial>
  <dcterms:spatial xsi:type="mshl:hreppur" xml:lang="is">Austur-Eyjafjallahreppur</dcterms:spatial>
  <dcterms:spatial xsi:type="mshl:sysla" xml:lang="is">Rangárvallasýsla</dcterms:spatial>
  <dcterms:spatial xsi:type="dcterms:Point">POINT(-19.6291269674614 63.5095112959265)</dcterms:spatial>
  <!-- … oai-auðkenni, síðari hreppur, dc:date 1703/1920, dcterms:temporal, lýsing, tungumál, útgefandi, leyfi … -->
</oai_dc:dc>
```

**2 · Manneskja** — Ævir lærðra manna: starf, EDTF-ártal og staður; óvissan geymd í `dcterms:temporal` við hlið vélræna bilsins.

```xml
<oai_dc:dc>  <!-- sömu nafnrými og að ofan -->
  <dc:identifier>https://skjalamyndir.skjalasafn.is/IS-THI-0043-2019-087-A-A-0001-01</dc:identifier>
  <dc:title xml:lang="is">Álfur Gíslason</dc:title>
  <dc:type xml:lang="is">Einstaklingur</dc:type>
  <dc:type xml:lang="en">Person</dc:type>
  <dc:subject xml:lang="is" xsi:type="mshl:starf">prestur</dc:subject>
  <dc:coverage xml:lang="is" xsi:type="mshl:stadur">Kaldaðarnesi</dc:coverage>  <!-- þágufall: á að vera Kaldaðarnes -->
  <dc:date>1696/1733</dc:date>
  <dcterms:temporal xml:lang="is" xsi:type="mshl:um">um 1696 - 1733</dcterms:temporal>
  <!-- … oai-auðkenni, safnmark, dcterms:isPartOf (bindi), dcterms:source, tilvísun, útgefandi, uppruni, tungumál … -->
</oai_dc:dc>
```

**3 · Saga með heildartexta** — Ísmús og Sagnagrunnur: sagan sjálf í `dc:description`, efnisflokkur ofan á efnisorðum, sögustaðir með hnitum og fólk með hlutverkum.

```xml
<oai_dc:dc>  <!-- sömu nafnrými og að ofan -->
  <dc:identifier>https://ismus.is/tjodfraedi/sagnir/10297</dc:identifier>
  <dc:title xml:lang="is">Sagnir Árna Jóhannessonar: III. Vofa Sigurbjargar</dc:title>
  <dc:type xml:lang="is">Sögn</dc:type>
  <dc:type xml:lang="en">Legend</dc:type>
  <dc:description xml:lang="is">Fyrri kona Bjarna Bjarnasonar á Þormóðsstöðum hét Sigurbjörg Sigurðardóttir. … Rak hann stálfleyga í kross niður í leiði Sigurbjargar og sást svipur hennar aldrei síðan.</dc:description>
  <dc:subject xml:lang="is" xsi:type="mshl:flokkur">Draugar og afturgöngur</dc:subject>
  <dc:subject xml:lang="is">Fylgjur</dc:subject>
  <!-- … þrír efnisflokkar, fjögur íslensk efnisorð og fimm ensk til viðbótar … -->
  <dc:coverage xml:lang="is">Þormóðsstaðir, Sölvadalur</dc:coverage>
  <dcterms:spatial xsi:type="dcterms:Point">POINT(-18.156287 65.378391)</dcterms:spatial>
  <dc:creator>Jóhannes Örn Jónsson</dc:creator>
  <dc:contributor>Árni Jóhannesson</dc:contributor>
  <dcterms:bibliographicCitation xml:lang="is">Jóhannes Örn Jónsson (skrásetjari) · Árni Jóhannesson (heimildarmaður)</dcterms:bibliographicCitation>
  <!-- … oai-auðkenni, tveir sögustaðir til viðbótar með hnitum, útgefandi, uppruni, tungumál … -->
</oai_dc:dc>
```

Heimildir: [`gold_test_100.xml`](../../../leidarljos/dc-template/gold/gold_test_100.xml) · [`AEVIR-TEST-2-menn-v2-tryA.xml`](../../../leidarljos/dc-template/sources/aevir/AEVIR-TEST-2-menn-v2-tryA.xml) · [`ISMUS-TEST-3-tryA.xml`](../../../leidarljos/dc-template/sources/ismus/ISMUS-TEST-3-tryA.xml)

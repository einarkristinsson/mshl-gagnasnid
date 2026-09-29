"""Sýnisveita: OAI-PMH 2.0 þjónn fyrir DC-skrá á ListRecords-formi.

Prófað gegn staðlinum sjálfum (openarchives.org/OAI/openarchivesprotocol.html),
ekki gegn því sem hermirinn gerir. Gögnin hér eru tilbúin, ekki RÚV-gögn.
"""
import unittest
import xml.etree.ElementTree as ET

from ..synisveita import Synisveita

OAI = "{http://www.openarchives.org/OAI/2.0/}"
DC = "{http://purl.org/dc/elements/1.1/}"


def _faersla(n, sett, dags):
    return (
        "  <record>\n    <header>\n"
        "      <identifier>oai:daemi.is:%d</identifier>\n"
        "      <datestamp>%sT00:00:00Z</datestamp>\n"
        "      <setSpec>source:daemi</setSpec>\n      <setSpec>%s</setSpec>\n"
        "    </header>\n    <metadata>\n"
        '<oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        '      <dc:title xml:lang="is">Færsla %d</dc:title>\n'
        "</oai_dc:dc>\n    </metadata>\n  </record>\n") % (n, dags, sett, n)


SKRA = "<ListRecords>\n" + "".join(
    _faersla(n, "type:a" if n <= 4 else "type:b", "2024-01-%02d" % n)
    for n in range(1, 8)) + "</ListRecords>\n"


def rot(xml):
    return ET.fromstring(xml.encode("utf-8"))


def villa(xml):
    e = rot(xml).find(OAI + "error")
    return e.get("code") if e is not None else None


class SynisveitaProf(unittest.TestCase):
    def setUp(self):
        self.v = Synisveita("daemi", SKRA, heiti="Dæmaveita", netfang="oai@daemi.is",
                            sidustaerd=3)
        self.base = "https://daemi.is/veitur/daemi/oai"

    def spyrja(self, **rok):
        return self.v.svara({k: [v] for k, v in rok.items()}, self.base)

    # ---- Identify ----
    def test_identify_skyldureitir(self):
        stada, xml = self.spyrja(verb="Identify")
        self.assertEqual(stada, 200)
        idn = rot(xml).find(OAI + "Identify")
        for reitur in ("repositoryName", "baseURL", "protocolVersion", "adminEmail",
                       "earliestDatestamp", "deletedRecord", "granularity"):
            self.assertTrue(idn.findtext(OAI + reitur), reitur)
        self.assertEqual(idn.findtext(OAI + "baseURL"), self.base)
        self.assertEqual(idn.findtext(OAI + "earliestDatestamp"), "2024-01-01T00:00:00Z")

    def test_umslag_ber_request_og_responseDate(self):
        _, xml = self.spyrja(verb="Identify")
        r = rot(xml)
        self.assertEqual(r.find(OAI + "request").text, self.base)
        self.assertEqual(r.find(OAI + "request").get("verb"), "Identify")
        self.assertTrue(r.findtext(OAI + "responseDate").endswith("Z"))

    # ---- snið og sett ----
    def test_listmetadataformats_ber_oai_dc(self):
        _, xml = self.spyrja(verb="ListMetadataFormats")
        pre = [e.text for e in rot(xml).iter(OAI + "metadataPrefix")]
        self.assertEqual(pre, ["oai_dc"])

    def test_listsets_tekur_oll_sett_ur_hausum(self):
        _, xml = self.spyrja(verb="ListSets")
        spec = sorted(e.text for e in rot(xml).iter(OAI + "setSpec"))
        self.assertEqual(spec, ["source:daemi", "type:a", "type:b"])

    # ---- listar og síðuskipting ----
    def test_listrecords_sidar_og_token_telur_rett(self):
        _, xml = self.spyrja(verb="ListRecords", metadataPrefix="oai_dc")
        r = rot(xml)
        self.assertEqual(len(r.findall(".//" + OAI + "record")), 3)
        tok = r.find(".//" + OAI + "resumptionToken")
        self.assertEqual(tok.get("completeListSize"), "7")
        self.assertEqual(tok.get("cursor"), "0")
        # ganga á enda: 3 + 3 + 1, síðasti token tómur
        alls, token = 3, tok.text
        while token:
            _, xml = self.spyrja(verb="ListRecords", resumptionToken=token)
            r = rot(xml)
            alls += len(r.findall(".//" + OAI + "record"))
            tok = r.find(".//" + OAI + "resumptionToken")
            token = tok.text if tok is not None else None
        self.assertEqual(alls, 7)
        self.assertIsNotNone(tok, "síðasta síða á að bera tómt resumptionToken")

    def test_set_skilar_adeins_eigin_faerslum(self):
        _, xml = self.spyrja(verb="ListIdentifiers", metadataPrefix="oai_dc", set="type:b")
        aud = [e.text for e in rot(xml).iter(OAI + "identifier")]
        self.assertEqual(aud, ["oai:daemi.is:5", "oai:daemi.is:6", "oai:daemi.is:7"])

    def test_from_until_sia_raunverulega(self):
        _, xml = self.spyrja(verb="ListIdentifiers", metadataPrefix="oai_dc",
                             **{"from": "2024-01-03", "until": "2024-01-04"})
        aud = [e.text for e in rot(xml).iter(OAI + "identifier")]
        self.assertEqual(aud, ["oai:daemi.is:3", "oai:daemi.is:4"])

    def test_getrecord_skilar_einni_faerslu_med_dc(self):
        _, xml = self.spyrja(verb="GetRecord", metadataPrefix="oai_dc",
                             identifier="oai:daemi.is:2")
        recs = rot(xml).findall(".//" + OAI + "record")
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0].findtext(".//" + DC + "title"), "Færsla 2")

    # ---- villur sem OAI-kóðar (staðall §3.6) ----
    def test_villukodar(self):
        self.assertEqual(villa(self.spyrja(verb="Harvest")[1]), "badVerb")
        self.assertEqual(villa(self.v.svara({}, self.base)[1]), "badVerb")
        self.assertEqual(villa(self.spyrja(verb="ListRecords")[1]), "badArgument")
        self.assertEqual(villa(self.spyrja(verb="ListRecords", metadataPrefix="marc")[1]),
                         "cannotDisseminateFormat")
        self.assertEqual(villa(self.spyrja(verb="GetRecord", metadataPrefix="oai_dc",
                                           identifier="oai:daemi.is:99")[1]), "idDoesNotExist")
        self.assertEqual(villa(self.spyrja(verb="ListRecords", metadataPrefix="oai_dc",
                                           set="type:ekki")[1]), "noRecordsMatch")
        self.assertEqual(villa(self.spyrja(verb="ListRecords", resumptionToken="rusl")[1]),
                         "badResumptionToken")
        self.assertEqual(villa(self.spyrja(verb="Identify", aukreitur="x")[1]), "badArgument")

    def test_token_er_einkarok(self):
        _, xml = self.spyrja(verb="ListRecords", metadataPrefix="oai_dc")
        token = rot(xml).find(".//" + OAI + "resumptionToken").text
        _, xml = self.spyrja(verb="ListRecords", resumptionToken=token, metadataPrefix="oai_dc")
        self.assertEqual(villa(xml), "badArgument")

    def test_endurtekin_rok_eru_villa(self):
        _, xml = self.v.svara({"verb": ["Identify", "Identify"]}, self.base)
        self.assertEqual(villa(xml), "badArgument")

    def test_blandad_nakvaemnisstig_i_from_until_er_villa(self):
        _, xml = self.spyrja(verb="ListRecords", metadataPrefix="oai_dc",
                             **{"from": "2024-01-01", "until": "2024-01-02T00:00:00Z"})
        self.assertEqual(villa(xml), "badArgument")

    def test_badargument_request_ber_engin_eigindi(self):
        # staðall §3.6: við badVerb/badArgument aðeins baseURL, engin eigindi
        _, xml = self.spyrja(verb="ListRecords")
        self.assertEqual(rot(xml).find(OAI + "request").attrib, {})

    def test_from_until_med_sekundum(self):
        _, xml = self.spyrja(verb="ListIdentifiers", metadataPrefix="oai_dc",
                             **{"from": "2024-01-06T00:00:00Z", "until": "2024-01-07T00:00:00Z"})
        aud = [e.text for e in rot(xml).iter(OAI + "identifier")]
        self.assertEqual(aud, ["oai:daemi.is:6", "oai:daemi.is:7"])


if __name__ == "__main__":
    unittest.main()


FORELDRI_BORN = "<ListRecords>\n" + "".join(
    ("  <record>\n    <header>\n      <identifier>oai:daemi.is:safn:%s</identifier>\n"
     "      <datestamp>2024-01-01T00:00:00Z</datestamp>\n      <setSpec>type:a</setSpec>\n"
     "    </header>\n    <metadata>\n"
     '<oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" '
     'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
     'xmlns:mshl="https://mshl.is/terms#">\n'
     '      <dc:title xml:lang="is">%s</dc:title>\n'
     '      <dc:type xml:lang="is">%s</dc:type>\n'
     '      <dc:creator mshl:role="flytjandi, stjórnandi">Jóna Jónsdóttir</dc:creator>\n'
     '      <dc:subject xml:lang="is" mshl:id="d:1">Kórar</dc:subject>\n'
     '      <dc:description xml:lang="is">Lýsing á &lt;b&gt; færslu.</dc:description>\n'
     "%s"
     "</oai_dc:dc>\n    </metadata>\n  </record>\n") % (i, t, g, p)
    for i, t, g, p in (
        ("AAA", "Platan", "Tónlistarupptaka", ""),
        ("BBB", "Fyrsta lag", "Lag",
         '      <dcterms:isPartOf xml:lang="is">Platan</dcterms:isPartOf>\n'
         "      <dcterms:isPartOf>oai:daemi.is:safn:AAA</dcterms:isPartOf>\n"
         '      <dcterms:isReferencedBy xml:lang="is">Frétt um lagið (daemi.is, 2024-01-02)</dcterms:isReferencedBy>\n'
         "      <dcterms:isReferencedBy>https://www.daemi.is/frett/lagid</dcterms:isReferencedBy>\n"),
        ("CCC", "Stakt efni", "Útvarpsþáttur",
         "      <dc:identifier>https://myndir.daemi.is/kyrrmynd.jpg</dc:identifier>\n"),
    )) + "</ListRecords>\n"


class FaerslusiduProf(unittest.TestCase):
    """Færslusíða: læsileg útgáfa einnar færslu, fyrir tengilinn heim."""

    def setUp(self):
        self.v = Synisveita("daemi", FORELDRI_BORN, audkennisforskeyti="oai:daemi.is:safn:")

    def test_faersla_eftir_stuttu_audkenni(self):
        f = self.v.faersla("BBB")
        self.assertEqual(f["titill"], "Fyrsta lag")
        self.assertEqual(f["tegund"], ["Lag"])
        self.assertEqual(f["folk"][0], {"nafn": "Jóna Jónsdóttir", "hlutverk": "flytjandi, stjórnandi",
                                        "reitur": "creator"})
        self.assertEqual(f["efnisord"], ["Kórar"])

    def test_foreldri_og_born_tengd(self):
        self.assertEqual(self.v.faersla("BBB")["foreldri"], {"stutt": "AAA", "titill": "Platan"})
        self.assertEqual(self.v.faersla("AAA")["born"], [{"stutt": "BBB", "titill": "Fyrsta lag"}])

    def test_othekkt_audkenni_er_none(self):
        self.assertIsNone(self.v.faersla("ZZZ"))

    def test_tilvisanir_parast_titill_og_slod(self):
        self.assertEqual(self.v.faersla("BBB")["tilvisanir"],
                         [{"titill": "Frétt um lagið (daemi.is, 2024-01-02)",
                           "slod": "https://www.daemi.is/frett/lagid"}])
        self.assertEqual(self.v.faersla("AAA")["tilvisanir"], [])

    def test_yfirlit_foreldri_med_bornum_og_stakt_efni(self):
        y = self.v.yfirlit()
        self.assertEqual([t["stutt"] for t in y], ["AAA", "CCC"])      # aðeins efsta stig
        self.assertEqual([b["stutt"] for b in y[0]["born"]], ["BBB"])
        self.assertEqual(y[0]["tegund"], "Tónlistarupptaka")
        self.assertEqual(y[1]["born"], [])

    def test_mynd_er_bein_myndslod_ur_identifier(self):
        self.assertEqual(self.v.faersla("CCC")["mynd"], "https://myndir.daemi.is/kyrrmynd.jpg")
        self.assertEqual(self.v.faersla("AAA")["mynd"], "")

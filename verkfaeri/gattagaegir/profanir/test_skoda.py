import json
import unittest

from ..skoda import skoda
from ..vorn import athuga
from . import Hermistjori


class SkodaProf(unittest.TestCase):
    """Flettihlutinn: ein OAI-beiðni, þáttuð og hrá."""

    def setUp(self):
        self.h = Hermistjori().__enter__()
        self.base = self.h.base + "/god/oai"

    def tearDown(self):
        self.h.__exit__()

    def test_identify_er_thattad_og_hratt(self):
        u = skoda(self.base, "Identify", bid=0)
        self.assertEqual(u["stada"], 200)
        self.assertTrue(u["gilt_xml"])
        self.assertEqual(u["domur"], "ok")
        self.assertIn("repositoryName", u["thattad"])
        self.assertIn("Identify", u["xml"])

    def test_listsets_skilar_settum(self):
        u = skoda(self.base, "ListSets", bid=0)
        spec = [s["spec"] for s in u["thattad"]["sett"]]
        self.assertIn("type:baer", spec)

    def test_listmetadataformats_skilar_prefixum(self):
        u = skoda(self.base, "ListMetadataFormats", bid=0)
        self.assertIn("oai_dc", u["thattad"]["prefixar"])

    def test_listidentifiers_hausar_og_token(self):
        u = skoda(self.base, "ListIdentifiers", {"metadataPrefix": "oai_dc"}, bid=0)
        self.assertTrue(u["thattad"]["hausar"])
        self.assertIn("token", u["thattad"])
        self.assertTrue(u["thattad"]["hausar"][0]["audkenni"])

    def test_getrecord_ein_faersla_med_reitum(self):
        li = skoda(self.base, "ListIdentifiers", {"metadataPrefix": "oai_dc"}, bid=0)
        aud = li["thattad"]["hausar"][0]["audkenni"]
        u = skoda(self.base, "GetRecord",
                  {"metadataPrefix": "oai_dc", "identifier": aud}, bid=0)
        f = u["thattad"]["faerslur"]
        self.assertEqual(len(f), 1)
        self.assertTrue(any(r["nafn"] == "dc:title" for r in f[0]["reitir"]))

    def test_listrecords_faerslur_og_token(self):
        u = skoda(self.base, "ListRecords", {"metadataPrefix": "oai_dc"}, bid=0)
        self.assertTrue(u["thattad"]["faerslur"])
        self.assertIn("token", u["thattad"])

    def test_othekkt_verb_fer_ekki_ut(self):
        u = skoda(self.base, "Harvest", bid=0)
        self.assertFalse(u["nadist"])
        self.assertIn("verb", u["villa"].lower())

    def test_oai_villa_er_thattud(self):
        u = skoda(self.base, "GetRecord",
                  {"metadataPrefix": "oai_dc", "identifier": "finnst-ekki"}, bid=0)
        self.assertEqual(u["domur"], "oai_villa")
        self.assertTrue(u["oai_villa"]["kodi"])

    def test_vorn_stoppar_innri_slod(self):
        u = skoda(self.base, "Identify", bid=0, vorn=athuga)
        self.assertFalse(u["nadist"])
        self.assertTrue(u["hafnad"])

    def test_nidurstadan_er_json_haef(self):
        u = skoda(self.base, "ListRecords", {"metadataPrefix": "oai_dc"}, bid=0)
        json.dumps(u, ensure_ascii=False)


if __name__ == "__main__":
    unittest.main()

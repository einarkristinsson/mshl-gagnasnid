"""Prófanir á byggja_timarit_dc.py (unittest, án nets).

    python3 -m unittest discover -s gagnaveitur/timarit

Dæmin eru orðrétt úr Tímarit.is-veitunni eins og hún var 29.9.2026.
"""
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import byggja_timarit_dc as b  # noqa: E402

DC = "{http://purl.org/dc/elements/1.1/}"
LANG = "{http://www.w3.org/XML/1998/namespace}lang"


def _svar(records, token=""):
    """Heilt OAI-svar eins og Tímarit.is skilar því (sjálfgefið nafnrými)."""
    tok = ('<resumptionToken completeListSize="3">%s</resumptionToken>' % token
           if token else "")
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/">'
            '<responseDate>2026-09-29T19:08:29Z</responseDate>'
            '<request verb="ListRecords">http://timarit.is/oai</request>'
            "<ListRecords>%s%s</ListRecords></OAI-PMH>" % ("".join(records), tok)
            ).encode("utf-8")


def _record(n, dc, datestamp="2020-01-06T10:24:27Z"):
    return ("<record><header><identifier>oai:timarit.is:publications/%d</identifier>"
            "<datestamp>%s</datestamp></header><metadata><oai_dc:dc>%s</oai_dc:dc>"
            "</metadata></record>" % (n, datestamp, dc))


SUJUMUT = _record(3, (
    "<dc:title>Sujumut</dc:title><dc:subject>Serials</dc:subject>"
    '<dc:description xml:lang="is"></dc:description>'
    '<dc:description xml:lang="en">Published from 1933 to 1948</dc:description>'
    "<dc:type>text</dc:type><dc:type>series</dc:type>"
    "<dc:language>kal</dc:language>"
    "<dc:identifier>http://timarit.is/publication/3</dc:identifier>"))

MORGUNBLADID = _record(58, (
    "<dc:title>Morgunblaðið</dc:title><dc:subject>Serials</dc:subject>"
    '<dc:description xml:lang="is">Dagblað.  Fréttir&#13;\n og greinar.</dc:description>'
    '<dc:description xml:lang="en">Published from 1913 to  present</dc:description>'
    "<dc:type>text</dc:type><dc:type>series</dc:type>"
    "<dc:language>isl</dc:language>"
    "<dc:identifier>http://timarit.is/publication/58</dc:identifier>"
    "<dc:publisher>Félag í Reykjavík, 1913-1919</dc:publisher>"
    "<dc:publisher>Árvakur, 1919-present</dc:publisher>"
    "<dc:publisher>Árvakur, 1920-1921</dc:publisher>"), "2023-03-14T00:00:00Z")


class Utgafuar(unittest.TestCase):
    def test_bil(self):
        self.assertEqual(b.tulka_utgafuar("Published from 1933 to 1948"),
                         ("1933/1948", "Kom út 1933–1948."))

    def test_opid_bil_med_tvofoldu_bili(self):
        self.assertEqual(b.tulka_utgafuar("Published from 1949 to  present"),
                         ("1949/..", "Hefur komið út frá árinu 1949."))

    def test_eitt_ar_med_endabili(self):
        self.assertEqual(b.tulka_utgafuar("Published in 1852 "),
                         ("1852", "Kom út árið 1852."))

    def test_sama_ar_tvisvar_verdur_eitt_ar(self):
        self.assertEqual(b.tulka_utgafuar("Published from 1913 to 1913"),
                         ("1913", "Kom út árið 1913."))

    def test_ofugt_bil_og_othekkt_mynstur(self):
        self.assertIsNone(b.tulka_utgafuar("Published from 1948 to 1933"))
        self.assertIsNone(b.tulka_utgafuar("Published c. 1900"))
        self.assertIsNone(b.tulka_utgafuar(""))

    def test_mynstur_fyrir_skyrsluna(self):
        self.assertEqual(b.mynstur(" Published c.  1900 "), "Published c. ÁÁÁÁ")


class Utgefandi(unittest.TestCase):
    def test_artol_fara(self):
        self.assertEqual(b.hreinsa_utgefanda("Niels Winther, 1852-1852"), "Niels Winther")
        self.assertEqual(b.hreinsa_utgefanda("Kvenréttindafélag Íslands, 1951-present"),
                         "Kvenréttindafélag Íslands")

    def test_kommur_inni_i_nafni_haldast(self):
        self.assertEqual(b.hreinsa_utgefanda("Walter, Swanson & Co., 1897-1898"),
                         "Walter, Swanson & Co.")
        self.assertEqual(b.hreinsa_utgefanda("The Viking Press, Ltd., 1914-1959"),
                         "The Viking Press, Ltd.")

    def test_tvofold_komma(self):
        self.assertEqual(b.hreinsa_utgefanda("Fiske, Willard,, 1903-1903"), "Fiske, Willard")

    def test_an_artala_obreytt(self):
        self.assertEqual(b.hreinsa_utgefanda("  Alþýðuflokkurinn "), "Alþýðuflokkurinn")


class MalOgLysing(unittest.TestCase):
    def test_iso_639_1(self):
        self.assertEqual([b.mal_kodi(k) for k in ("isl", "fao", "kal", "dan", "eng", "deu")],
                         ["is", "fo", "kl", "da", "en", "de"])
        self.assertEqual(b.mal_kodi("xyz"), "xyz")

    def test_setning_fyrst_svo_heimildin(self):
        self.assertEqual(b.lysing("Dagblað, gefið út af jafnaðarmönnum", "Alþýðublaðið",
                                  "Kom út 1919–1998."),
                         ("Kom út 1919–1998. Dagblað, gefið út af jafnaðarmönnum", "ur_heimild"))

    def test_titill_og_lysingu_vantar_sleppt(self):
        self.assertEqual(b.lysing("AvangnâmioK", "AvangnâmioK", "Kom út 1913–1958."),
                         ("Kom út 1913–1958.", "titill"))
        self.assertEqual(b.lysing("Lýsingu vantar", "X", "Kom út árið 1900."),
                         ("Kom út árið 1900.", "vantar"))
        self.assertEqual(b.lysing("", "X", ""), ("", "tom"))

    def test_marc_merki_fara(self):
        self.assertEqual(b.lysing("Reykjavík : |b Handbækur, |c 1967", "Hrund", "")[0],
                         "Reykjavík : Handbækur, 1967")
        # lóðrétt strik sem skilur að efnisorð er ekki MARC-merki
        self.assertEqual(b.hreinsa_lysingu("Sjávarútvegur | Fiskveiðar"),
                         "Sjávarútvegur | Fiskveiðar")


class Heild(unittest.TestCase):
    def _smida(self, *records):
        s = b.lesa_svar(_svar(records))
        texti, talning = b.smida(s["faerslur"])
        return texti, talning, ET.fromstring(texti.encode("utf-8"))

    def test_alma_snid_og_sannprofun(self):
        texti, talning, rot = self._smida(SUJUMUT, MORGUNBLADID)
        self.assertEqual(b.sannprofa(texti, 2), [])
        self.assertFalse(texti.startswith("<?xml"))
        self.assertEqual(rot.tag, "ListRecords")
        self.assertEqual(rot.findall("record")[0].find("header/identifier").text,
                         "oai:timarit.is:publications/3")
        self.assertEqual(rot.findall("record")[0].findtext("header/setSpec"), "source:timarit")
        self.assertEqual(talning["dags"]["bil"], 1)
        self.assertEqual(talning["dags"]["opid"], 1)
        self.assertEqual(dict(talning["othekkt"]), {})

    def test_reitir_sujumut(self):
        _t, _n, rot = self._smida(SUJUMUT)
        dc = rot.find("record/metadata")[0]
        self.assertEqual([e.text for e in dc.findall(DC + "identifier")],
                         ["https://timarit.is/publication/3", "oai:timarit.is:publications/3"])
        self.assertEqual([(e.get(LANG), e.text) for e in dc.findall(DC + "type")],
                         [("is", "Tímarit"), ("en", "Text")])
        self.assertEqual([(e.get(LANG), e.text) for e in dc.findall(DC + "subject")],
                         [("is", "Tímarit og blöð"), ("en", "Serials")])
        self.assertEqual(dc.findtext(DC + "date"), "1933/1948")
        self.assertEqual(dc.findtext(DC + "language"), "kl")
        self.assertEqual(dc.findtext(DC + "description"), "Kom út 1933–1948.")
        self.assertIsNone(dc.find(DC + "publisher"))
        for e in dc:
            self.assertTrue((e.text or "").strip(), e.tag)

    def test_reitir_morgunbladid(self):
        _t, _n, rot = self._smida(MORGUNBLADID)
        dc = rot.find("record/metadata")[0]
        self.assertEqual(dc.findtext(DC + "date"), "1913/..")
        self.assertEqual(dc.findtext(DC + "description"),
                         "Hefur komið út frá árinu 1913. Dagblað. Fréttir og greinar.")
        self.assertEqual([e.text for e in dc.findall(DC + "publisher")],
                         ["Félag í Reykjavík", "Árvakur"])

    def test_sannprofun_gripur_villur(self):
        texti, _n, _r = self._smida(SUJUMUT)
        self.assertTrue(b.sannprofa('<?xml version="1.0"?>\n' + texti, 1))
        self.assertTrue(b.sannprofa(texti, 2))                      # fjöldi stemmir ekki
        self.assertTrue(b.sannprofa(texti.replace("1933/1948", "1933 - 1948"), 1))
        self.assertTrue(b.sannprofa(texti.replace(">kl<", "><"), 1))  # tómur reitur

    def test_resumption_token_lesinn(self):
        s = b.lesa_svar(_svar([SUJUMUT], token="abc123"))
        self.assertEqual(s["token"], "abc123")
        self.assertEqual(s["fjoldi"], 3)
        self.assertEqual(b.lesa_svar(_svar([SUJUMUT]))["token"], "")


if __name__ == "__main__":
    unittest.main()

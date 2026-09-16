import unittest

from .. import xml_lestur as xl
from ..athuganir import Samhengi, FELL, STODST
from ..athuganir import faerslur as F, hreinlaeti as H, gildi as G
from .test_xml_lestur import _lr, _record, _Svar


def _samhengi(*records):
    sk = xl.lesa(_lr(*records))
    s = Samhengi("http://x/oai", None, {"slodaprof": False})
    s.faerslur = xl.faerslur(sk)
    s.oll_svor = [_lr(*records)]
    return s


class FaersluProf(unittest.TestCase):
    def test_F04_par_vantar(self):
        s = _samhengi(_record('<dc:title>A</dc:title>'
                              '<dc:type>Photography</dc:type>'))
        self.assertEqual(F.F04(s).stada, FELL)

    def test_F04_par_i_lagi(self):
        s = _samhengi(_record('<dc:title>A</dc:title>'
                              '<dc:type xml:lang="is">Bær</dc:type>'
                              '<dc:type xml:lang="en">Place</dc:type>'))
        self.assertEqual(F.F04(s).stada, STODST)

    def test_F13_eiginn_reitur(self):
        s = _samhengi(_record(
            '<dc:title>A</dc:title>'
            '<sarpur:x xmlns:sarpur="https://sarpur.is/ns">1</sarpur:x>'))
        self.assertEqual(F.F13(s).stada, FELL)

    def test_F12_source_slod(self):
        s = _samhengi(_record('<dc:title>A</dc:title>'
                              '<dc:source>https://x/1</dc:source>'))
        self.assertEqual(F.F12(s).stada, FELL)


class HreinlaetiProf(unittest.TestCase):
    def test_H05_none_gildi(self):
        s = _samhengi(_record('<dc:title>A</dc:title>'
                              '<dc:date>None</dc:date>'))
        self.assertEqual(H.H05(s).stada, FELL)

    def test_H06_tomur_reitur(self):
        s = _samhengi(_record('<dc:title>A</dc:title>'
                              '<dc:format></dc:format>'))
        self.assertEqual(H.H06(s).stada, FELL)

    def test_H03_styritakn(self):
        s = Samhengi("http://x/oai", None, {})
        s.oll_svor = [_Svar("<a>x\x01y</a>")]
        self.assertEqual(H.H03(s).stada, FELL)


class GildiProf(unittest.TestCase):
    def test_G01_edtf(self):
        gott = _samhengi(_record('<dc:title>A</dc:title>'
                                 '<dc:date>1703/1920</dc:date>'))
        vont = _samhengi(_record('<dc:title>A</dc:title>'
                                 '<dc:date>1920 - 1925</dc:date>'))
        self.assertEqual(G.G01(gott).stada, STODST)
        self.assertEqual(G.G01(vont).stada, FELL)

    def test_G02_G03_hnit(self):
        ofug = _samhengi(_record(
            '<dc:title>A</dc:title>'
            '<dcterms:spatial xsi:type="dcterms:Point">POINT(63.5 -19.6)'
            '</dcterms:spatial>'))
        rett = _samhengi(_record(
            '<dc:title>A</dc:title>'
            '<dcterms:spatial xsi:type="dcterms:Point">POINT(-19.6 63.5)'
            '</dcterms:spatial>'))
        self.assertEqual(G.G02(ofug).stada, STODST)  # snið í lagi
        self.assertEqual(G.G03(ofug).stada, FELL)    # röð öfug
        self.assertEqual(G.G03(rett).stada, STODST)

    def test_G04_forskeyti(self):
        s = _samhengi(_record(
            '<dc:title>A</dc:title>'
            '<dc:coverage>Sýsla: Rangárvallasýsla</dc:coverage>'))
        self.assertEqual(G.G04(s).stada, FELL)


if __name__ == "__main__":
    unittest.main()

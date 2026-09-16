import unittest

from .. import velin
from . import Hermistjori

STILL = {"bid_ms": 0, "sidur": 3, "syni": 6}


def _fell_kenni(skyrsla):
    return {a["kenni"] for h in skyrsla["hopar"]
            for a in h["athuganir"] if a["stada"] == "fell"}


class VelinProf(unittest.TestCase):
    def test_godur_endapunktur_stenst_allt(self):
        with Hermistjori() as h:
            sk = velin.keyra_allt(h.base + "/god/oai", STILL)
        self.assertEqual(sk["samantekt"]["villur"], 0)
        self.assertEqual(sk["samantekt"]["advaranir"], 0)
        self.assertEqual(sk["samantekt"]["sleppt"], 0)
        self.assertGreater(sk["syni"]["faerslur"], 20)

    def test_brotinn_endapunktur_finnur_gildrurnar(self):
        with Hermistjori() as h:
            sk = velin.keyra_allt(h.base + "/brotin/oai", STILL)
        fell = _fell_kenni(sk)
        vaentanlegar = {
            "E02", "E03", "E04", "E12", "E13", "E14", "E15", "E16",
            "F01", "F03", "F04", "F07", "F12", "F13",
            "H01", "H02", "H03", "H04", "H05", "H06", "H07", "H08",
            "G01", "G03", "G04",
        }
        vantar = vaentanlegar - fell
        self.assertEqual(vantar, set(), "þessar áttu að falla: %s" % vantar)
        self.assertGreaterEqual(sk["samantekt"]["villur"], 10)

    def test_nidri_thjonn_fellur_ekki(self):
        sk = velin.keyra_allt("http://127.0.0.1:1/oai",
                              {"bid_ms": 0, "sidur": 1, "syni": 1})
        self.assertIsNotNone(sk)
        # engin undantekning; flestar athuganir sleppt
        self.assertGreater(sk["samantekt"]["sleppt"], 10)


if __name__ == "__main__":
    unittest.main()

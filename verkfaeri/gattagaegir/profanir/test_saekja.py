import unittest

from ..saekja import Saekjari
from .. import notandastrengur
from . import Hermistjori


class SaekjariProf(unittest.TestCase):
    def test_get_eltir_beiningu(self):
        with Hermistjori() as h:
            sk = Saekjari(h.base + "/brotin/oai", notandastrengur(), bid=0)
            svar = sk.oai("Identify", elta=True)
            self.assertEqual(svar.stada, 200)
            self.assertTrue(svar.beint)  # 301 sást á leiðinni
            self.assertIn("Identify", svar.texti)

    def test_post_eltir_ekki_beiningu(self):
        with Hermistjori() as h:
            sk = Saekjari(h.base + "/brotin/oai", notandastrengur(), bid=0)
            svar = sk.oai("Identify", adferd="POST")
            self.assertEqual(svar.stada, 301)  # gildran sést

    def test_refused_skilar_villu(self):
        sk = Saekjari("http://127.0.0.1:1/oai", notandastrengur(), bid=0,
                      timalok=2)
        svar = sk.oai("Identify")
        self.assertFalse(svar.nadist)
        self.assertIsNotNone(svar.villa)

    def test_head_a_mynd(self):
        with Hermistjori() as h:
            sk = Saekjari(h.base + "/god/oai", notandastrengur(), bid=0)
            svar = sk.profa_slod(h.base + "/god/myndir/1.png", "HEAD")
            self.assertEqual(svar.stada, 200)
            self.assertIn("image/png", svar.haus("content-type"))


if __name__ == "__main__":
    unittest.main()

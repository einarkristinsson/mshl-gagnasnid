import os
import unittest

from ..__main__ import lesa_rok


class RokProf(unittest.TestCase):
    def test_sjalfgefid_er_lokad_a_eigin_vel(self):
        a = lesa_rok([], umhverfi={})
        self.assertEqual(a.host, "127.0.0.1")
        self.assertEqual(a.port, 8765)
        self.assertFalse(a.opinn)

    def test_opinn_rofi(self):
        self.assertTrue(lesa_rok(["--opinn"], umhverfi={}).opinn)

    def test_umhverfi_skysins_opnar_og_velur_port(self):
        # Cloud Run setur PORT; GATTAGAEGIR_OPINN=1 kveikir á vörninni.
        a = lesa_rok([], umhverfi={"PORT": "8080", "GATTAGAEGIR_OPINN": "1"})
        self.assertEqual(a.port, 8080)
        self.assertTrue(a.opinn)

    def test_rok_i_skel_vinna_yfir_umhverfi(self):
        a = lesa_rok(["--port", "9000"], umhverfi={"PORT": "8080"})
        self.assertEqual(a.port, 9000)


if __name__ == "__main__":
    unittest.main()


class AframsendingRokProf(unittest.TestCase):
    def test_umhverfi_gefur_aframsendingar(self):
        a = lesa_rok([], umhverfi={"AFRAMSENDING": "sagnatrog.kann.is=https://trog.example/a; annad.kann.is=https://b.example/"})
        self.assertEqual(a.aframsending, {"sagnatrog.kann.is": "https://trog.example/a",
                                          "annad.kann.is": "https://b.example/"})

    def test_engin_aframsending_sjalfgefid(self):
        self.assertEqual(lesa_rok([], umhverfi={}).aframsending, {})

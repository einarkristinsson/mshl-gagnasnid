import unittest

from ..vorn import athuga, Hafnad


def _leysir(*ip):
    """Gervi-nafnaþjónn: skilar föstum IP-tölum, óháð neti."""
    return lambda hysill: list(ip)


class VornProf(unittest.TestCase):
    def test_hafnar_loopback(self):
        with self.assertRaises(Hafnad):
            athuga("http://127.0.0.1:8766/god/oai", leysa=_leysir("127.0.0.1"))

    def test_hafnar_lysigagnathjonustu_skysins(self):
        with self.assertRaises(Hafnad):
            athuga("http://169.254.169.254/computeMetadata/v1/",
                   leysa=_leysir("169.254.169.254"))

    def test_hafnar_innra_neti(self):
        with self.assertRaises(Hafnad):
            athuga("http://safn.local/oai", leysa=_leysir("10.0.0.5"))

    def test_hafnar_odru_en_http(self):
        with self.assertRaises(Hafnad):
            athuga("ftp://safn.is/oai", leysa=_leysir("93.184.216.34"))

    def test_hafnar_lykilordi_i_slod(self):
        with self.assertRaises(Hafnad):
            athuga("https://notandi:leyni@safn.is/oai",
                   leysa=_leysir("93.184.216.34"))

    def test_hafnar_ovenjulegri_gatt(self):
        with self.assertRaises(Hafnad):
            athuga("http://safn.is:22/oai", leysa=_leysir("93.184.216.34"))

    def test_leyfir_opinbera_slod(self):
        slod = "https://smb.mshl.is/oai/"
        self.assertEqual(athuga(slod, leysa=_leysir("93.184.216.34")), slod)

    def test_hafnar_ef_ein_af_morgum_ip_er_innri(self):
        with self.assertRaises(Hafnad):
            athuga("https://safn.is/oai",
                   leysa=_leysir("93.184.216.34", "192.168.1.1"))

    def test_hafnar_ef_hysill_finnst_ekki(self):
        def leysa(h):
            raise OSError("nafn finnst ekki")
        with self.assertRaises(Hafnad):
            athuga("https://finnst-ekki.example/oai", leysa=leysa)


if __name__ == "__main__":
    unittest.main()

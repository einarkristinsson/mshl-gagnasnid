import json
import threading
import time
import unittest
import urllib.error
import urllib.request

from ..thjonn import bua_til as bua_thjon
from . import Hermistjori


def _get(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return r.status, r.read().decode("utf-8"), r.headers

def _post(url, hlutur):
    gogn = json.dumps(hlutur).encode("utf-8")
    beidni = urllib.request.Request(url, data=gogn, method="POST",
                                    headers={"Content-Type":
                                             "application/json"})
    with urllib.request.urlopen(beidni, timeout=30) as r:
        return r.status, r.read().decode("utf-8")


class ThjonnProf(unittest.TestCase):
    def setUp(self):
        self.h = Hermistjori().__enter__()
        self.thj = bua_thjon(0)
        self.port = self.thj.server_address[1]
        threading.Thread(target=self.thj.serve_forever, daemon=True).start()
        time.sleep(0.1)
        self.b = "http://127.0.0.1:%d" % self.port

    def tearDown(self):
        self.thj.shutdown()
        self.h.__exit__()

    def test_forsida_og_static(self):
        st, texti, _ = _get(self.b + "/")
        self.assertEqual(st, 200)
        self.assertIn("Gáttagægir", texti)
        st, _t, hausar = _get(self.b + "/vefur/still.css")
        self.assertEqual(st, 200)
        self.assertIn("text/css", hausar.get("Content-Type"))

    def test_hvitlisti_lokar(self):
        with self.assertRaises(urllib.error.HTTPError) as c:
            _get(self.b + "/vefur/thjonn.py")
        self.assertEqual(c.exception.code, 404)

    def test_heilsa(self):
        st, texti, _ = _get(self.b + "/api/heilsa")
        self.assertEqual(json.loads(texti)["stada"], "ok")

    def test_post_streymi_lykur_med_lok(self):
        st, texti = _post(self.b + "/api/profa",
                          {"slod": self.h.base + "/god/oai",
                           "stillingar": {"bid_ms": 0, "sidur": 2,
                                          "syni": 4}})
        linur = [json.loads(x) for x in texti.strip().splitlines() if x]
        self.assertEqual(linur[0]["tegund"], "byrjun")
        self.assertEqual(linur[-1]["tegund"], "lok")
        self.assertEqual(linur[-1]["skyrsla"]["samantekt"]["villur"], 0)

    def test_buffrad_get(self):
        st, texti, _ = _get(self.b + "/api/profa?slod=" + self.h.base
                            + "/god/oai&bid_ms=0&sidur=2&syni=4")
        d = json.loads(texti)
        self.assertEqual(d["samantekt"]["villur"], 0)

    def test_ogild_slod_400(self):
        with self.assertRaises(urllib.error.HTTPError) as c:
            _post(self.b + "/api/profa", {"slod": "ftp://x"})
        self.assertEqual(c.exception.code, 400)


if __name__ == "__main__":
    unittest.main()

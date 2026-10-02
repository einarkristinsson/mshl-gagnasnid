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
        st, trog, hausar = _get(self.b + "/vefur/trog.svg")
        self.assertEqual(st, 200)
        self.assertIn("image/svg", hausar.get("Content-Type"))
        self.assertIn("<svg", trog)

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

    def test_snid_skilar_gullna(self):
        st, texti, _ = _get(self.b + "/api/snid")
        self.assertEqual(st, 200)
        d = json.loads(texti)
        self.assertTrue(d["gullna"].strip(), "gullna á ekki að vera tómt")
        self.assertIn("oai_dc:dc", d["gullna"])
        self.assertIsInstance(d["daemi"], list)

    def test_faerslur_bera_hratt_xml(self):
        st, texti, _ = _get(self.b + "/api/profa?slod=" + self.h.base
                            + "/god/oai&bid_ms=0&sidur=2&syni=4")
        d = json.loads(texti)
        faerslur = d.get("faerslur", [])
        self.assertTrue(faerslur, "engar færslur í skýrslu")
        medxml = [f for f in faerslur if f.get("hratt_xml")]
        self.assertTrue(medxml, "engin færsla bar hratt_xml")
        self.assertIn("oai_dc:dc", medxml[0]["hratt_xml"])



class OpinnThjonnProf(unittest.TestCase):
    """Opna útgáfan (skýið): vörnin er á og heilsan segir frá því."""

    def setUp(self):
        self.h = Hermistjori().__enter__()
        self.thj = bua_thjon(0, opin=True)
        self.port = self.thj.server_address[1]
        threading.Thread(target=self.thj.serve_forever, daemon=True).start()
        time.sleep(0.1)
        self.b = "http://127.0.0.1:%d" % self.port

    def tearDown(self):
        self.thj.shutdown()
        self.h.__exit__()

    def test_heilsa_segir_opin(self):
        st, texti, _ = _get(self.b + "/api/heilsa")
        self.assertEqual(st, 200)
        self.assertTrue(json.loads(texti).get("opin"))

    def test_innri_slod_er_stoppud_i_straumnum(self):
        st, texti = _post(self.b + "/api/profa",
                          {"slod": self.h.base + "/god/oai",
                           "stillingar": {"sidur": 1, "syni": 1, "sett": 0}})
        self.assertEqual(st, 200)
        atburdir = [json.loads(l) for l in texti.splitlines() if l.strip()]
        villur = [a for a in atburdir if a.get("tegund") == "villa"]
        self.assertTrue(villur, "engin villa í straumnum")
        self.assertIn("ekki leyf", villur[0]["skilabod"].lower())
        # og ekkert var sótt af herminum
        beidnir = [a for a in atburdir if a.get("tegund") == "beidni"
                   and a.get("nadist")]
        self.assertEqual(beidnir, [])


class SkodaApiProf(unittest.TestCase):
    """POST /api/skoda — flettihlutinn yfir HTTP."""

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

    def test_skoda_skilar_thattadri_nidurstodu(self):
        st, texti = _post(self.b + "/api/skoda",
                          {"slod": self.h.base + "/god/oai", "verb": "ListSets"})
        self.assertEqual(st, 200)
        u = json.loads(texti)
        self.assertEqual(u["domur"], "ok")
        self.assertTrue(u["thattad"]["sett"])

    def test_skoda_hafnar_ogildri_slod(self):
        beidni = urllib.request.Request(
            self.b + "/api/skoda", data=json.dumps({"slod": "ftp://x", "verb": "Identify"}).encode(),
            method="POST", headers={"Content-Type": "application/json"})
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(beidni, timeout=10)
        self.assertEqual(cm.exception.code, 400)


class AframsendingProf(unittest.TestCase):
    """sagnatrog.kann.is vísar á sömu þjónustu og áframsendir á trogið á Leitir."""

    def setUp(self):
        self.thj = bua_thjon(0, aframsending={"sagnatrog.kann.is": "https://trog.example/nde/home"})
        self.port = self.thj.server_address[1]
        threading.Thread(target=self.thj.serve_forever, daemon=True).start()
        time.sleep(0.1)
        self.b = "http://127.0.0.1:%d" % self.port

    def tearDown(self):
        self.thj.shutdown()

    def _get_med_host(self, host, slod="/"):
        beidni = urllib.request.Request(self.b + slod, headers={"Host": host})
        opn = urllib.request.build_opener(_EngarBeiningar)
        try:
            with opn.open(beidni, timeout=10) as r:
                return r.status, r.headers.get("Location")
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get("Location")

    def test_aframsendingarhysill_faer_302(self):
        st, loc = self._get_med_host("sagnatrog.kann.is")
        self.assertEqual(st, 302)
        self.assertEqual(loc, "https://trog.example/nde/home")

    def test_adrir_hyslar_fa_siduna(self):
        st, loc = self._get_med_host("gattagaegir-mshl.kann.is")
        self.assertEqual(st, 200)
        self.assertIsNone(loc)


class _EngarBeiningar(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


class SynisveituLeidProf(unittest.TestCase):
    """/veitur/<nafn>/oai — sýnisveitur hýstar í sama þjóni."""

    def setUp(self):
        from ..synisveita import Synisveita
        from .test_synisveita import SKRA
        self.thj = bua_thjon(0, veitur={"daemi": Synisveita("daemi", SKRA, sidustaerd=3)})
        self.port = self.thj.server_address[1]
        threading.Thread(target=self.thj.serve_forever, daemon=True).start()
        time.sleep(0.1)
        self.b = "http://127.0.0.1:%d" % self.port

    def tearDown(self):
        self.thj.shutdown()

    def test_get_identify_skilar_xml(self):
        st, texti, haus = _get(self.b + "/veitur/daemi/oai?verb=Identify")
        self.assertEqual(st, 200)
        self.assertIn("text/xml", haus.get("Content-Type"))
        self.assertIn("<baseURL>http://127.0.0.1:%d/veitur/daemi/oai</baseURL>" % self.port, texti)

    def test_skastrik_virkar_lika(self):
        st, texti, _ = _get(self.b + "/veitur/daemi/oai/?verb=Identify")
        self.assertEqual(st, 200)
        self.assertIn("<Identify>", texti)

    def test_post_virkar(self):
        beidni = urllib.request.Request(self.b + "/veitur/daemi/oai",
                                        data=b"verb=ListSets", method="POST",
                                        headers={"Content-Type": "application/x-www-form-urlencoded"})
        with urllib.request.urlopen(beidni, timeout=10) as r:
            self.assertIn("<setSpec>type:a</setSpec>", r.read().decode("utf-8"))

    def test_othekkt_veita_404(self):
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(self.b + "/veitur/ekki/oai?verb=Identify", timeout=10)
        self.assertEqual(cm.exception.code, 404)

    def test_veitulisti(self):
        st, texti, _ = _get(self.b + "/api/veitur")
        self.assertEqual(st, 200)
        self.assertEqual(json.loads(texti)[0]["nafn"], "daemi")


class FaerslusiduLeidProf(unittest.TestCase):
    """/<veita>/<stutt auðkenni> — færslusíða; sagnatrog.kann.is sýnir hana líka."""

    def setUp(self):
        from ..synisveita import Synisveita
        from .test_synisveita import FORELDRI_BORN
        v = Synisveita("daemi", FORELDRI_BORN, audkennisforskeyti="oai:daemi.is:safn:",
                       adgangur={"texti": "Óska eftir efninu", "slod": "https://daemi.is/safn"})
        self.thj = bua_thjon(0, veitur={"daemi": v},
                             aframsending={"trog.example": "https://leitir.example/"})
        self.port = self.thj.server_address[1]
        threading.Thread(target=self.thj.serve_forever, daemon=True).start()
        time.sleep(0.1)
        self.b = "http://127.0.0.1:%d" % self.port

    def tearDown(self):
        self.thj.shutdown()

    def _get_host(self, slod, host):
        beidni = urllib.request.Request(self.b + slod, headers={"Host": host})
        opn = urllib.request.build_opener(_EngarBeiningar)
        try:
            with opn.open(beidni, timeout=10) as r:
                return r.status, r.read().decode("utf-8"), r.headers
        except urllib.error.HTTPError as e:
            return e.code, "", e.headers

    def test_faerslusida_er_html_med_efni(self):
        st, texti, haus = _get(self.b + "/daemi/BBB")
        self.assertEqual(st, 200)
        self.assertIn("text/html", haus.get("Content-Type"))
        self.assertIn("Fyrsta lag", texti)
        self.assertIn("flytjandi, stjórnandi", texti)
        self.assertIn('href="/daemi/AAA"', texti)            # hluti af foreldri
        self.assertIn("https://daemi.is/safn", texti)         # aðgangur að efninu
        self.assertIn("&lt;b&gt;", texti)                     # texti er afkóðaður, ekki HTML
        self.assertNotIn("<b>", texti)

    def test_tengill_a_eiganda_opnast_i_nyjum_flipa(self):
        # færslusíðan helst opin; noopener svo síða eigandans nái ekki í hana
        _, texti, _ = _get(self.b + "/daemi/BBB")
        self.assertIn('href="https://daemi.is/safn" target="_blank" rel="noopener"', texti)

    def test_tilvisun_birtist_med_hysilheiti_i_fyrirsogn(self):
        _, texti, _ = _get(self.b + "/daemi/BBB")
        self.assertIn("Á daemi.is", texti)
        self.assertIn('href="https://www.daemi.is/frett/lagid" target="_blank" rel="noopener"', texti)

    def test_yfirlitssida_tengir_allar_faerslur(self):
        st, texti, haus = _get(self.b + "/daemi/")
        self.assertEqual(st, 200)
        self.assertIn("text/html", haus.get("Content-Type"))
        for stutt in ("AAA", "BBB", "CCC"):
            self.assertIn('href="/daemi/%s"' % stutt, texti)
        self.assertIn('href="/veitur/daemi/oai?verb=Identify"', texti)
        self.assertEqual(_get(self.b + "/daemi")[0], 200)

    def test_mynd_birtist_a_faerslusidu(self):
        _, texti, _ = _get(self.b + "/daemi/CCC")
        self.assertIn('<img class="mynd" src="https://myndir.daemi.is/kyrrmynd.jpg"', texti)
        _, texti, _ = _get(self.b + "/daemi/AAA")
        self.assertNotIn('class="mynd"', texti)

    def test_leit_i_sagnatroginu_er_hrein_leitarord(self):
        # NDE sýnir query-gildið orðrétt í leitarreitnum; „any,contains,“ á ekki heima þar
        _, texti, _ = _get(self.b + "/daemi/AAA")
        self.assertIn("nde/search?query=Platan&amp;", texti)
        self.assertNotIn("any,contains", texti)

    def test_faerslusida_visar_a_yfirlit(self):
        _, texti, _ = _get(self.b + "/daemi/BBB")
        self.assertIn('href="/daemi/"', texti)

    def test_othekkt_faersla_404(self):
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(self.b + "/daemi/ZZZ", timeout=10)
        self.assertEqual(cm.exception.code, 404)

    def test_aframsendingarhysill_synir_faerslusidu_en_sendir_forsidu_afram(self):
        st, texti, _ = self._get_host("/daemi/AAA", "trog.example")
        self.assertEqual(st, 200)
        self.assertIn("Platan", texti)
        st, texti, _ = self._get_host("/daemi/", "trog.example")
        self.assertEqual(st, 200)
        self.assertIn('href="/daemi/AAA"', texti)
        st, texti, _ = self._get_host("/veitur/daemi/oai?verb=Identify", "trog.example")
        self.assertEqual(st, 200)                      # yfirlitið vísar á veituna
        st, _, haus = self._get_host("/", "trog.example")
        self.assertEqual(st, 302)
        self.assertEqual(haus.get("Location"), "https://leitir.example/")


def _hysill(url, host, gogn=None):
    """GET (eða POST ef gogn) með gefnu Host-hausi; fylgir ekki tilvísunum."""
    beidni = urllib.request.Request(url, data=gogn, headers={"Host": host})
    opn = urllib.request.build_opener(_EngarBeiningar)
    try:
        with opn.open(beidni, timeout=10) as r:
            return r.status, r.read().decode("utf-8"), r.headers
    except urllib.error.HTTPError as e:
        return e.code, "", e.headers


class OaiMidstodProf(unittest.TestCase):
    """Einn staður sem þjónar mörgum sýnisveitum: oai.kann.is/<veita>."""

    def setUp(self):
        from ..synisveita import Synisveita
        from .test_synisveita import SKRA
        v = Synisveita("daemi", SKRA, heiti="Dæmaveita", lysing="Tilbúin gögn til prófunar.")
        self.thj = bua_thjon(0, veitur={"daemi": v}, oai_hyslar={"oai.example"},
                             kanoniskur="gaegir.example")
        threading.Thread(target=self.thj.serve_forever, daemon=True).start()
        time.sleep(0.1)
        self.b = "http://127.0.0.1:%d" % self.thj.server_address[1]

    def tearDown(self):
        self.thj.shutdown()

    def test_forsida_listar_veitur(self):
        st, texti, haus = _hysill(self.b + "/", "oai.example")
        self.assertEqual(st, 200)
        self.assertIn("text/html", haus.get("Content-Type"))
        self.assertIn('href="/daemi?verb=Identify"', texti)
        self.assertIn("Dæmaveita", texti)

    def test_stutt_slod_er_veitan_og_baseurl_fylgir(self):
        for slod in ("/daemi?verb=Identify", "/daemi/?verb=Identify"):
            st, texti, haus = _hysill(self.b + slod, "oai.example")
            self.assertEqual(st, 200, slod)
            self.assertIn("text/xml", haus.get("Content-Type"))
            self.assertIn("<baseURL>http://oai.example/daemi</baseURL>", texti)

    def test_post_virkar_a_stuttu_slodinni(self):
        st, texti, _ = _hysill(self.b + "/daemi", "oai.example", b"verb=Identify")
        self.assertEqual(st, 200)
        self.assertIn("<Identify>", texti)

    def test_othekkt_veita_404_og_merki_opin(self):
        self.assertEqual(_hysill(self.b + "/ekkitil?verb=Identify", "oai.example")[0], 404)
        self.assertEqual(_hysill(self.b + "/vefur/still.css", "oai.example")[0], 200)

    def test_oai_vidskeyti_virkar_lika(self):
        st, texti, _ = _hysill(self.b + "/daemi/oai?verb=Identify", "oai.example")
        self.assertEqual(st, 200)
        self.assertIn("<baseURL>http://oai.example/daemi</baseURL>", texti)

    def test_veitulisti_gefur_lenid(self):
        st, texti, _ = _hysill(self.b + "/api/veitur", "gaegir.example")
        self.assertEqual(json.loads(texti)[0]["slod"], "https://oai.example/daemi")

    def test_yfirlit_visar_a_lenid_og_gattagaegi_med_slod(self):
        st, texti, _ = _hysill(self.b + "/daemi/", "gaegir.example")
        self.assertEqual(st, 200)
        self.assertIn('href="https://oai.example/daemi?verb=Identify"', texti)
        self.assertIn("?slod=https%3A%2F%2Foai.example%2Fdaemi", texti)

    def test_run_app_visar_a_kanoniskt_len(self):
        st, _, haus = _hysill(self.b + "/veitur/daemi/oai?verb=Identify", "gattagaegir-123.europe-west4.run.app")
        self.assertEqual(st, 301)
        self.assertEqual(haus.get("Location"), "https://gaegir.example/veitur/daemi/oai?verb=Identify")
        st, texti, _ = _hysill(self.b + "/veitur/daemi/oai", "gattagaegir-123.europe-west4.run.app",
                               b"verb=Identify")
        self.assertEqual(st, 200)                       # POST fylgir ekki 301 — svarað beint

    def test_annar_hysill_obreyttur(self):
        st, texti, _ = _hysill(self.b + "/", "127.0.0.1")
        self.assertEqual(st, 200)
        self.assertNotIn('href="/daemi?verb=Identify"', texti)


class FaerslusidaTvipunkturProf(unittest.TestCase):
    """Auðkenni með tvípunkti og hlutfallskóðun (Listasafn: syning:%C3%BEoka)."""

    def setUp(self):
        from ..synisveita import Synisveita
        from .test_synisveita import FORELDRI_BORN
        xml = FORELDRI_BORN.replace("safn:CCC", "safn:syning:%C3%BEoka")
        v = Synisveita("daemi", xml, audkennisforskeyti="oai:daemi.is:safn:")
        self.thj = bua_thjon(0, veitur={"daemi": v},
                             aframsending={"trog.example": "https://leitir.example/"})
        threading.Thread(target=self.thj.serve_forever, daemon=True).start()
        time.sleep(0.1)
        self.b = "http://127.0.0.1:%d" % self.thj.server_address[1]

    def tearDown(self):
        self.thj.shutdown()

    def test_faerslusida_med_tvipunkti_og_hlutfallskodun(self):
        st, texti, _ = _get(self.b + "/daemi/syning:%C3%BEoka")
        self.assertEqual(st, 200)
        self.assertIn("Stakt efni", texti)

    def test_yfirlit_visar_a_somu_slod(self):
        _, texti, _ = _get(self.b + "/daemi/")
        self.assertIn('href="/daemi/syning:%C3%BEoka"', texti)

    def test_aframsendingarhysill_synir_siduna(self):
        beidni = urllib.request.Request(self.b + "/daemi/syning:%C3%BEoka",
                                        headers={"Host": "trog.example"})
        with urllib.request.build_opener(_EngarBeiningar).open(beidni, timeout=10) as r:
            self.assertEqual(r.status, 200)
            self.assertIn("Stakt efni", r.read().decode("utf-8"))


if __name__ == "__main__":
    unittest.main()

"""Vefþjónn Gáttagægis — stdlib HTTP, static síða + NDJSON API.

Leiðir:
  GET  /                 -> vefur/index.html
  GET  /vefur/<skra>     -> still.css, gaegir.js (hvítlisti)
  GET  /api/heilsa       -> {"stada":"ok"}
  POST /api/profa        -> NDJSON straumur af atburðum
  GET  /api/profa?slod=  -> full skýrsla sem JSON (buffrað, fyrir curl)
  POST /api/skoda        -> ein OAI-beiðni, þáttuð og hrá (flettihlutinn)
  GET  /api/veitur       -> sýnisveitur sem þjónninn hýsir
  GET|POST /veitur/<nafn>/oai[/]  -> OAI-PMH 2.0 sýnisveita (synisveita.py)
  GET  /<nafn>/<stutt auðkenni>   -> færslusíða (faerslusida.py) — opin slóð á færslu
  GET  /<nafn>/                   -> yfirlit allra færslna sýnisveitunnar
  á OAI-miðstöð (OAI_HYSLAR, t.d. oai.kann.is):  /  -> listi veitna · /<nafn> -> OAI-veitan
"""
import json
import os
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from . import UTGAFA
from . import velin
from . import skoda as skodari
from .vorn import athuga as _vorn_athuga

VEFUR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vefur")
# Rót geymslunnar: skráin er í verkfaeri/gattagaegir/, rótin er þrjú þrep upp.
ROT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

_XML_BLOKK = re.compile(r"```xml\n(.*?)\n```", re.DOTALL)


def _lesa_skra(*hlutar):
    """Les textaskrá undir rótinni; skilar tómum streng ef hún vantar."""
    try:
        with open(os.path.join(ROT, *hlutar), encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def _xml_ur_markdown(texti, heimild):
    """Nær ```xml-blokkum úr markdown með fyrirsögn feitletruðu línunnar
    á undan (t.d. „**1 · Staður** — …")."""
    ut = []
    heiti = None
    innan = False
    buffer = []
    for lina in texti.splitlines():
        strk = lina.strip()
        if innan:
            if strk.startswith("```"):
                innan = False
                ut.append({"titill": heiti or "Dæmi",
                           "xml": "\n".join(buffer).strip(),
                           "heimild": heimild})
            else:
                buffer.append(lina)
        else:
            if strk.startswith("**"):
                heiti = strk.replace("**", "").strip()
            if strk.startswith("```xml"):
                innan = True
                buffer = []
    return ut


def _snid_gogn():
    """Les gullna sniðið og dæmi beint úr repo-skjölunum (skrifvarið)."""
    gullna = ""
    for m in _XML_BLOKK.finditer(_lesa_skra("snidmat", "GULLNA-SNIDID.md")):
        blokk = m.group(1).strip()
        if "oai_dc:dc" in blokk:
            gullna = blokk
            break
    daemi = []
    # sjálfstæðar .xml skrár í snidmat/daemi/ (ef einhverjar verða til)
    try:
        skrar = sorted(n for n in os.listdir(os.path.join(ROT, "snidmat",
                                                          "daemi"))
                       if n.endswith(".xml"))
    except OSError:
        skrar = []
    for n in skrar:
        daemi.append({"titill": n, "xml": _lesa_skra("snidmat", "daemi", n),
                      "heimild": "snidmat/daemi/%s" % n})
    # xml-blokkir úr README (raunfærslur á gullna sniðinu)
    readme = _lesa_skra("snidmat", "daemi", "README.md")
    if readme:
        daemi.extend(_xml_ur_markdown(readme, "snidmat/daemi/README.md"))
    return {"gullna": gullna,
            "gullna_heimild": "snidmat/GULLNA-SNIDID.md",
            "daemi": daemi}
_STATIC = {
    "still.css": "text/css; charset=utf-8",
    "gaegir.js": "application/javascript; charset=utf-8",
    "trog.svg": "image/svg+xml",
    "sagnatrog.png": "image/png",
    "favicon.png": "image/png",
}
_SAMTIMIS = threading.BoundedSemaphore(2)


def _hreinsa_stillingar(raw):
    raw = raw or {}
    def tala(nafn, sjalf, lag, hatt):
        try:
            v = int(raw.get(nafn, sjalf))
        except (TypeError, ValueError):
            v = sjalf
        return max(lag, min(hatt, v))
    return {
        "sidur": tala("sidur", 3, 1, 10),
        "syni": tala("syni", 10, 1, 25),
        "sett": tala("sett", 5, 0, 10),
        "slodaprof": bool(raw.get("slodaprof", True)),
        "bid_ms": tala("bid_ms", 250, 0, 5000),
    }


def _gild_slod(slod):
    if not slod:
        return None
    slod = slod.strip().split("?", 1)[0].strip()
    p = urlparse(slod)
    if p.scheme not in ("http", "https") or not p.netloc:
        return None
    return slod


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "Gattagaegir/" + UTGAFA

    def _send(self, kodi, gerd, gogn_b, haus=None):
        self.send_response(kodi)
        self.send_header("Content-Type", gerd)
        self.send_header("Content-Length", str(len(gogn_b)))
        for k, v in (haus or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(gogn_b)

    def _json(self, kodi, hlutur):
        self._send(kodi, "application/json; charset=utf-8",
                   json.dumps(hlutur, ensure_ascii=False).encode("utf-8"))

    def _aframsending(self):
        """sagnatrog.kann.is o.fl. vísa á sömu þjónustu: 302 á trogið."""
        kort = getattr(self.server, "aframsending", None) or {}
        hysill = (self.headers.get("Host") or "").split(":")[0].strip().lower()
        return kort.get(hysill)

    # ---- sýnisveitur: /veitur/<nafn>/oai og /veitur/<nafn>/oai/ ----
    _VEITULEID = re.compile(r"^/veitur/([a-z0-9_-]+)/oai/?$")

    def _synisveita(self, p, rok):
        m = self._VEITULEID.match(p.path)
        veitur = getattr(self.server, "veitur", None) or {}
        if not m or m.group(1) not in veitur:
            return False
        self._svara_oai(m.group(1), rok, "/veitur/%s/oai" % m.group(1))
        return True

    def _svara_oai(self, nafn, rok, leid):
        """OAI-svar veitu `nafn`; baseURL eins og gesturinn sér hana (Cloud Run: X-Forwarded-Proto)."""
        proto = (self.headers.get("X-Forwarded-Proto") or "http").split(",")[0].strip()
        hysill = self.headers.get("Host") or "127.0.0.1"
        _, xml = self.server.veitur[nafn].svara(rok, "%s://%s%s" % (proto, hysill, leid))
        self._send(200, "text/xml; charset=UTF-8", xml.encode("utf-8"),
                   {"X-Robots-Tag": "noindex, nofollow"})

    # ---- OAI-miðstöð: oai.kann.is/<veita> er veitan sjálf, forsíðan listar þær ----
    _MIDSTODVARLEID = re.compile(r"^/([a-z0-9_-]+)(?:/oai)?/?$")      # /ruv, /ruv/, /ruv/oai

    def _oai_grunnur(self, nafn):
        """Slóð veitunnar á léni OAI-miðstöðvar (https://oai.kann.is/ruv), eða None."""
        hyslar = sorted(getattr(self.server, "oai_hyslar", None) or ())
        return "https://%s/%s" % (hyslar[0], nafn) if hyslar else None

    def _kanoniskt(self):
        """GET á *.run.app → 301 á DNS-nafnið, svo gamlar slóðir í póstum virki áfram."""
        kan = getattr(self.server, "kanoniskur", None)
        hysill = (self.headers.get("Host") or "").split(":")[0].strip().lower()
        if not kan or not hysill.endswith(".run.app"):
            return False
        self.send_response(301)
        self.send_header("Location", "https://%s%s" % (kan, self.path))
        self.send_header("Content-Length", "0")
        self.end_headers()
        return True

    def _oai_hysill(self):
        hyslar = getattr(self.server, "oai_hyslar", None) or set()
        return (self.headers.get("Host") or "").split(":")[0].strip().lower() in hyslar

    def _midstod(self, p, rok):
        veitur = getattr(self.server, "veitur", None) or {}
        if p.path == "/":
            from .faerslusida import smida_midstod
            proto = (self.headers.get("X-Forwarded-Proto") or "http").split(",")[0].strip()
            rot = "%s://%s" % (proto, self.headers.get("Host") or "127.0.0.1")
            return self._send(200, "text/html; charset=utf-8",
                              smida_midstod(veitur, rot).encode("utf-8"))
        if p.path.startswith("/vefur/") and p.path[len("/vefur/"):] in _STATIC:
            nafn = p.path[len("/vefur/"):]
            return self._skra(nafn, _STATIC[nafn])
        m = self._MIDSTODVARLEID.match(p.path)
        if m and m.group(1) in veitur:
            return self._svara_oai(m.group(1), rok, "/" + m.group(1))
        return self._send(404, "text/html; charset=utf-8",
                          "<!DOCTYPE html><meta charset=utf-8><title>Finnst ekki</title>"
                          "<p>Engin veita með þessu nafni. <a href=\"/\">Allar veitur</a></p>".encode("utf-8"))

    # ---- færslusíður: /<veita>/<stutt auðkenni> ----
    _FAERSLULEID = re.compile(r"^/([a-z0-9_-]+)/([A-Za-z0-9._-]+)/?$")

    def _faerslusida(self, p):
        m = self._FAERSLULEID.match(p.path)
        veitur = getattr(self.server, "veitur", None) or {}
        if not m or m.group(1) not in veitur:
            return False
        veita = veitur[m.group(1)]
        f = veita.faersla(m.group(2))
        if f is None:
            self._send(404, "text/html; charset=utf-8",
                       "<!DOCTYPE html><meta charset=utf-8><title>Finnst ekki</title>"
                       "<p>Engin færsla með þessu auðkenni.</p>".encode("utf-8"))
            return True
        from .faerslusida import smida
        self._send(200, "text/html; charset=utf-8", smida(veita, f).encode("utf-8"),
                   {"X-Robots-Tag": "noindex, nofollow"})
        return True

    # ---- yfirlit sýnisveitu: /<veita>/ ----
    _YFIRLITSLEID = re.compile(r"^/([a-z0-9_-]+)/?$")

    def _yfirlitssida(self, p):
        m = self._YFIRLITSLEID.match(p.path)
        veitur = getattr(self.server, "veitur", None) or {}
        if not m or m.group(1) not in veitur:
            return False
        veita = veitur[m.group(1)]
        from .faerslusida import smida_yfirlit
        self._send(200, "text/html; charset=utf-8",
                   smida_yfirlit(veita, veita.yfirlit(), oai_slod=self._oai_grunnur(m.group(1))).encode("utf-8"),
                   {"X-Robots-Tag": "noindex, nofollow"})
        return True

    def do_GET(self):
        p = urlparse(self.path)
        if self._kanoniskt():
            return
        if self._oai_hysill():
            return self._midstod(p, parse_qs(p.query))
        slod = self._aframsending()
        # áframsendingarlén (sagnatrog.kann.is) sýnir yfirlit og færslusíður; forsíðan fer á Leitir
        if slod and not p.path.startswith(("/vefur/", "/api/", "/veitur/")):
            if self._yfirlitssida(p) or (self._FAERSLULEID.match(p.path) and self._faerslusida(p)):
                return
        if slod and p.path.startswith(("/vefur/", "/veitur/")):
            slod = None                      # merki síðnanna og OAI-veitan sem yfirlitið vísar á
        if slod:
            self.send_response(302)
            self.send_header("Location", slod)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if p.path.startswith("/veitur/"):
            if self._synisveita(p, parse_qs(p.query)):
                return
            return self._json(404, {"villa": "engin sýnisveita með því nafni"})
        if p.path == "/api/veitur":
            veitur = getattr(self.server, "veitur", None) or {}
            return self._json(200, [{"nafn": n, "heiti": v.heiti, "faerslur": v.fjoldi(),
                                     "slod": self._oai_grunnur(n) or "/veitur/%s/oai" % n}
                                    for n, v in sorted(veitur.items())])
        if p.path == "/":
            return self._skra("index.html", "text/html; charset=utf-8")
        if not p.path.startswith(("/vefur/", "/api/")) and (self._yfirlitssida(p) or self._faerslusida(p)):
            return
        if p.path.startswith("/vefur/"):
            nafn = p.path[len("/vefur/"):]
            if nafn in _STATIC:
                return self._skra(nafn, _STATIC[nafn])
            return self._json(404, {"villa": "óþekkt skrá"})
        if p.path == "/api/heilsa":
            return self._json(200, {"stada": "ok", "utgafa": UTGAFA,
                                    "opin": self._opin()})
        if p.path == "/api/snid":
            return self._json(200, _snid_gogn())
        if p.path == "/api/profa":
            q = {k: v[0] for k, v in parse_qs(p.query).items()}
            slod = _gild_slod(q.get("slod"))
            if not slod:
                return self._json(400, {"villa": "ógild slóð"})
            still = _hreinsa_stillingar(q)
            with _SAMTIMIS:
                skyrsla = velin.keyra_allt(slod, still, vorn=self._vorn())
            return self._json(200, skyrsla or {"villa": "engin skýrsla"})
        return self._json(404, {"villa": "ekki fundið"})

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        p = urlparse(self.path)
        if self._oai_hysill():
            lengd = int(self.headers.get("Content-Length", 0) or 0)
            return self._midstod(p, parse_qs((self.rfile.read(lengd) or b"").decode("utf-8")))
        if p.path.startswith("/veitur/"):
            lengd = int(self.headers.get("Content-Length", 0) or 0)
            rok = parse_qs((self.rfile.read(lengd) or b"").decode("utf-8"))
            if self._synisveita(p, rok):
                return
            return self._json(404, {"villa": "engin sýnisveita með því nafni"})
        if p.path not in ("/api/profa", "/api/skoda"):
            return self._json(404, {"villa": "ekki fundið"})
        try:
            lengd = int(self.headers.get("Content-Length", 0) or 0)
            beidni = json.loads(self.rfile.read(lengd) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {"villa": "ógilt JSON"})
        slod = _gild_slod(beidni.get("slod"))
        if not slod:
            return self._json(400, {"villa": "ógild slóð (http/https)"})
        if p.path == "/api/skoda":
            rok = beidni.get("rok") or {}
            if not isinstance(rok, dict):
                return self._json(400, {"villa": "rok á að vera hlutur"})
            with _SAMTIMIS:
                ut = skodari.skoda(slod, str(beidni.get("verb") or ""),
                                   {k: str(v) for k, v in rok.items()},
                                   vorn=self._vorn(),
                                   elta=bool(beidni.get("elta", True)))
            return self._json(200, ut)
        still = _hreinsa_stillingar(beidni.get("stillingar"))
        self._streyma(slod, still)

    def _streyma(self, slod, still):
        stopp = threading.Event()
        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
        self.send_header("Connection", "close")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        with _SAMTIMIS:
            try:
                for atburd in velin.keyra(slod, still, stopp,
                                          vorn=self._vorn()):
                    lina = json.dumps(atburd, ensure_ascii=False) + "\n"
                    self.wfile.write(lina.encode("utf-8"))
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                stopp.set()
        self.close_connection = True

    def _skra(self, nafn, gerd):
        slod = os.path.join(VEFUR, nafn)
        try:
            with open(slod, "rb") as f:
                self._send(200, gerd, f.read())
        except OSError:
            self._json(404, {"villa": "skrá vantar"})

    def log_message(self, *a):
        pass

    # Opin útgáfa (skýið): vörnin stöðvar slóðir inn á innra net.
    def _opin(self):
        return bool(getattr(self.server, "opin", False))

    def _vorn(self):
        return _vorn_athuga if self._opin() else None


def bua_til(port=8765, host="127.0.0.1", opin=False, aframsending=None, veitur=None, oai_hyslar=None,
            kanoniskur=None):
    """opin=True þegar þjónninn er aðgengilegur öðrum en eigin vél.
    aframsending: {hýsilheiti: slóð} — beiðnir með því Host-hausi fá 302.
    veitur: {nafn: Synisveita} — hýstar á /veitur/<nafn>/oai.
    oai_hyslar: hýsilheiti OAI-miðstöðvar (oai.kann.is): /<nafn> er veitan, / listar þær.
    kanoniskur: DNS-nafn Gáttagægis; GET á *.run.app fær 301 þangað."""
    thj = ThreadingHTTPServer((host, port), Handler)
    thj.opin = opin
    thj.aframsending = {k.lower(): v for k, v in (aframsending or {}).items()}
    thj.veitur = dict(veitur or {})
    thj.oai_hyslar = {h.strip().lower() for h in (oai_hyslar or ()) if h.strip()}
    thj.kanoniskur = (kanoniskur or "").strip().lower() or None
    return thj


def hlada_synisveitum(mappa):
    """Hver <nafn>.xml í möppunni verður sýnisveita; <nafn>.json (valfrjálst)
    gefur heiti, netfang og lýsingu. Mappa sem er ekki til → engar veitur."""
    from .synisveita import Synisveita
    ut = {}
    if not mappa or not os.path.isdir(mappa):
        return ut
    for skra in sorted(os.listdir(mappa)):
        if not skra.endswith(".xml"):
            continue
        nafn = skra[:-4]
        meta = {}
        jslod = os.path.join(mappa, nafn + ".json")
        if os.path.exists(jslod):
            with open(jslod, encoding="utf-8") as f:
                meta = json.load(f)
        with open(os.path.join(mappa, skra), encoding="utf-8") as f:
            ut[nafn] = Synisveita(nafn, f.read(), heiti=meta.get("heiti"),
                                  netfang=meta.get("netfang", "einar@kann.is"),
                                  sidustaerd=int(meta.get("sidustaerd", 5)),
                                  lysing=meta.get("lysing", ""),
                                  audkennisforskeyti=meta.get("audkennisforskeyti", ""),
                                  adgangur=meta.get("adgangur"),
                                  uppruni=meta.get("uppruni", ""))
    return ut

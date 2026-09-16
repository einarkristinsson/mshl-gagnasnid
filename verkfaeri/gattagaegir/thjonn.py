"""Vefþjónn Gáttagægis — stdlib HTTP, static síða + NDJSON API.

Leiðir:
  GET  /                 -> vefur/index.html
  GET  /vefur/<skra>     -> still.css, gaegir.js (hvítlisti)
  GET  /api/heilsa       -> {"stada":"ok"}
  POST /api/profa        -> NDJSON straumur af atburðum
  GET  /api/profa?slod=  -> full skýrsla sem JSON (buffrað, fyrir curl)
"""
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from . import UTGAFA
from . import velin

VEFUR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vefur")
_STATIC = {
    "still.css": "text/css; charset=utf-8",
    "gaegir.js": "application/javascript; charset=utf-8",
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

    def do_GET(self):
        p = urlparse(self.path)
        if p.path == "/":
            return self._skra("index.html", "text/html; charset=utf-8")
        if p.path.startswith("/vefur/"):
            nafn = p.path[len("/vefur/"):]
            if nafn in _STATIC:
                return self._skra(nafn, _STATIC[nafn])
            return self._json(404, {"villa": "óþekkt skrá"})
        if p.path == "/api/heilsa":
            return self._json(200, {"stada": "ok", "utgafa": UTGAFA})
        if p.path == "/api/profa":
            q = {k: v[0] for k, v in parse_qs(p.query).items()}
            slod = _gild_slod(q.get("slod"))
            if not slod:
                return self._json(400, {"villa": "ógild slóð"})
            still = _hreinsa_stillingar(q)
            with _SAMTIMIS:
                skyrsla = velin.keyra_allt(slod, still)
            return self._json(200, skyrsla or {"villa": "engin skýrsla"})
        return self._json(404, {"villa": "ekki fundið"})

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        p = urlparse(self.path)
        if p.path != "/api/profa":
            return self._json(404, {"villa": "ekki fundið"})
        try:
            lengd = int(self.headers.get("Content-Length", 0) or 0)
            beidni = json.loads(self.rfile.read(lengd) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {"villa": "ógilt JSON"})
        slod = _gild_slod(beidni.get("slod"))
        if not slod:
            return self._json(400, {"villa": "ógild slóð (http/https)"})
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
                for atburd in velin.keyra(slod, still, stopp):
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


def bua_til(port=8765, host="127.0.0.1"):
    return ThreadingHTTPServer((host, port), Handler)

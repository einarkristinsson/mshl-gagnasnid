"""Kurteis OAI-PMH biðill — sækir eina beiðni í einu, með vaxandi bið.

Sama kurteisi og saekja-oai.py:
  - auðkennandi User-Agent,
  - endurtaka með vaxandi bið (1,5 s / 3 s / 4,5 s), ekki í lykkju,
  - fáar samhliða tengingar (hér: ein í einu),
  - lítið sýni, aldrei full uppskera.

Sérstaða gagnvart prófun: við fylgjum EKKI 3xx sjálfkrafa. Það er viljand,
því ein af gildrunum (POST á /oai fer í 301) sést aðeins ef beiningin er
ekki elt í kyrrþey.
"""
import socket
import time
import urllib.error
import urllib.parse
import urllib.request

HAMARK_LESA = 20 * 1024 * 1024  # 20 MB þak á svar
BID_SJALFGEFIN = 0.25            # kurteisishlé milli beiðna, sekúndur
TIMALOK = 30                     # sekúndur á hverja beiðni


class Haett(Exception):
    """Kastað þegar notandi hættir við keyrslu í miðri göngu."""


def _timabundid(reason):
    """Er netvillan tímabundin (þess virði að reyna aftur)?"""
    if isinstance(reason, (socket.timeout, TimeoutError)):
        return True
    if isinstance(reason, (ConnectionRefusedError, socket.gaierror)):
        return False
    return "timed out" in str(reason).lower()


class _EngarBeinar(urllib.request.HTTPRedirectHandler):
    """Fylgir engum 3xx-beiningum — lætur þær koma upp sem HTTPError."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Svar:
    """Eitt HTTP-svar með öllu sem athuganirnar þurfa."""

    def __init__(self, slod, adferd):
        self.slod = slod
        self.adferd = adferd
        self.stada = None          # HTTP-staða (200, 301, 500 …)
        self.hausar = {}           # svarhausar (lágstafa lyklar)
        self.gogn = b""            # hrá bæti
        self.texti = ""            # afkóðaður texti (best-effort)
        self.bom = False           # byrjar svarið á UTF-8 BOM?
        self.ekki_utf8 = False     # tókst ekki að afkóða sem strangt UTF-8?
        self.ms = 0                # svartími í millisekúndum
        self.beint = []            # keðja beininga sem sást
        self.villa = None          # netvilla (strengur) ef ekki náðist í þjón

    @property
    def nadist(self):
        return self.villa is None

    def haus(self, nafn):
        return self.hausar.get(nafn.lower(), "")


def _afkoda(gogn):
    """Skilar (texti, bom, ekki_utf8)."""
    bom = gogn[:3] == b"\xef\xbb\xbf"
    hreint = gogn[3:] if bom else gogn
    try:
        return hreint.decode("utf-8"), bom, False
    except UnicodeDecodeError:
        return hreint.decode("utf-8", "replace"), bom, True


class Saekjari:
    """Sækir OAI-verb og stakar slóðir af einum endapunkti, kurteislega."""

    def __init__(self, baseurl, ua, bid=BID_SJALFGEFIN, timalok=TIMALOK,
                 stopp=None):
        self.baseurl = baseurl
        self.ua = ua
        self.bid = bid
        self.timalok = timalok
        self.stopp = stopp
        self._opnari = urllib.request.build_opener(_EngarBeinar)
        self._fyrsta = True
        self.beidnir = []   # skrá yfir allar beiðnir (til skýrslu)

    # ---- innri ----------------------------------------------------------
    def _hle(self):
        if self.stopp is not None and self.stopp.is_set():
            raise Haett()
        if not self._fyrsta and self.bid > 0:
            time.sleep(self.bid)
        self._fyrsta = False

    def _ein(self, slod, adferd, gogn=None):
        """Ein HTTP-beiðni án endurtekninga. Skilar Svar eða kastar."""
        svar = Svar(slod, adferd)
        beidni = urllib.request.Request(slod, data=gogn, method=adferd)
        beidni.add_header("User-Agent", self.ua)
        beidni.add_header("Accept", "text/xml, application/xml, */*")
        if gogn is not None:
            beidni.add_header("Content-Type",
                              "application/x-www-form-urlencoded")
        t0 = time.time()
        try:
            with self._opnari.open(beidni, timeout=self.timalok) as r:
                svar.stada = r.status
                svar.hausar = {k.lower(): v for k, v in r.headers.items()}
                svar.gogn = r.read(HAMARK_LESA + 1)
        except urllib.error.HTTPError as e:
            svar.stada = e.code
            svar.hausar = {k.lower(): v for k, v in e.headers.items()}
            try:
                svar.gogn = e.read(HAMARK_LESA + 1)
            except Exception:
                svar.gogn = b""
        svar.ms = int((time.time() - t0) * 1000)
        if len(svar.gogn) > HAMARK_LESA:
            svar.gogn = svar.gogn[:HAMARK_LESA]
        svar.texti, svar.bom, svar.ekki_utf8 = _afkoda(svar.gogn)
        return svar

    def _saekja(self, slod, adferd, gogn=None, elta=False, hopp=3):
        """Sækir slóð með endurtekningum og (valkvæmri) beiningu."""
        self._hle()
        bidir = [1.5, 3.0, 4.5]
        sidast = None
        for tilraun in range(4):
            try:
                svar = self._ein(slod, adferd, gogn)
            except urllib.error.URLError as e:
                sidast = Svar(slod, adferd)
                sidast.villa = str(e.reason)
                # Tenging neitað eða nafn finnst ekki -> reyna ekki aftur.
                if not _timabundid(e.reason):
                    return sidast
            except (socket.timeout, TimeoutError) as e:
                sidast = Svar(slod, adferd)
                sidast.villa = str(e)
            except Exception as e:
                sidast = Svar(slod, adferd)
                sidast.villa = str(e)
                return sidast
            else:
                # Tókst að ná sambandi. Meðhöndla beiningu ef GET og elta.
                if 300 <= (svar.stada or 0) < 400:
                    nyt = svar.haus("location")
                    svar.beint.append("%s → %s" % (svar.stada, nyt))
                    if elta and adferd == "GET" and nyt and hopp > 0:
                        naest = urllib.parse.urljoin(slod, nyt)
                        framhald = self._saekja(naest, "GET", None,
                                                elta=True, hopp=hopp - 1)
                        framhald.beint = svar.beint + framhald.beint
                        return framhald
                return svar
            # netvilla: bíða og reyna aftur (nema síðasta tilraun)
            if tilraun < 3:
                time.sleep(bidir[tilraun])
        return sidast

    # ---- ytra viðmót ----------------------------------------------------
    def oai(self, verb, adferd="GET", elta=True, **rok):
        """Sækir OAI-verb. rok verða að fyrirspurnarfærslum."""
        breytur = {"verb": verb}
        breytur.update({k: v for k, v in rok.items() if v is not None})
        strengur = urllib.parse.urlencode(breytur)
        if adferd == "POST":
            svar = self._saekja(self.baseurl, "POST",
                                strengur.encode("utf-8"))
        else:
            skil = "&" if ("?" in self.baseurl) else "?"
            svar = self._saekja(self.baseurl + skil + strengur, "GET",
                                elta=elta)
        self.beidnir.append("%s %s verb=%s"
                            % (adferd, self.baseurl, verb))
        return svar

    def profa_slod(self, url, adferd="HEAD"):
        """Prófar staka slóð (færsluslóð eða smámynd) án þess að elta."""
        svar = self._saekja(url, adferd, elta=False)
        self.beidnir.append("%s %s" % (adferd, url))
        return svar

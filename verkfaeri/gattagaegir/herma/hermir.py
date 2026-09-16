"""Staðbundinn OAI-PMH hermir: /god/oai (heill) og /brotin/oai (gallaður)."""
import struct
import zlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from xml.sax.saxutils import escape

from . import gogn

BOM = b"\xef\xbb\xbf"


def _png_1x1():
    """Býr til minnstu mögulegu PNG (1x1) úr stdlib — engin binary-bókstöf."""
    def chunk(teg, gogn):
        return (struct.pack(">I", len(gogn)) + teg + gogn
                + struct.pack(">I", zlib.crc32(teg + gogn) & 0xffffffff))
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    rad = zlib.compress(b"\x00\xff\xff\xff")
    return (sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", rad)
            + chunk(b"IEND", b""))


PNG = _png_1x1()


def _villa(kodi, verb, request_url):
    return _umslag('<error code="%s">%s</error>' % (kodi, kodi), verb,
                   request_url)


def _umslag(inni, verb, request_url):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<responseDate>2026-09-16T19:00:00Z</responseDate>'
        '<request verb="%s">%s</request>%s</OAI-PMH>'
        % (verb, escape(request_url), inni))


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    # ---- gagns ----------------------------------------------------------
    def _base(self):
        return "http://%s" % self.headers.get("Host", "127.0.0.1")

    def _skrifa(self, kodi, gerd, gogn_b, bom=False, haus=None):
        if bom:
            gogn_b = BOM + gogn_b
        self.send_response(kodi)
        self.send_header("Content-Type", gerd)
        self.send_header("Content-Length", str(len(gogn_b)))
        for k, v in (haus or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(gogn_b)

    def _xml(self, texti, bom=False, kodi=200):
        self._skrifa(kodi, "text/xml; charset=utf-8",
                     texti.encode("utf-8"), bom=bom)

    # ---- afgreiðsla -----------------------------------------------------
    def do_GET(self):
        self._afgreida()

    def do_POST(self):
        self._afgreida()

    def do_HEAD(self):
        self._afgreida()

    def _afgreida(self):
        p = urlparse(self.path)
        leid = p.path
        q = {k: v[0] for k, v in parse_qs(p.query).items()}
        if self.command == "POST":
            lengd = int(self.headers.get("Content-Length", 0) or 0)
            body = self.rfile.read(lengd).decode("utf-8", "replace")
            for k, v in parse_qs(body).items():
                q[k] = v[0]
        base = self._base()
        req_url = base + self.path

        # auðlindir (síður og myndir) fyrir F03/F07
        if leid.startswith("/god/hlutur/"):
            return self._skrifa(200, "text/html; charset=utf-8",
                                b"<html><body>Hlutur</body></html>")
        if leid.startswith("/god/myndir/"):
            return self._skrifa(200, "image/png", PNG)
        if leid.startswith("/brotin/hlutur/"):
            return self._skrifa(302, "text/html", b"", haus={
                "Location": base + "/brotin/"})
        if leid.startswith("/brotin/mynd-sida/"):
            return self._skrifa(200, "text/html; charset=utf-8",
                                b"<html><body>Myndasida</body></html>")

        # gildran: /brotin/oai (án skástriks) fer i 301 a /brotin/oai/.
        # GET heldur fyrirspurnarstrengnum (i lagi); POST tapar meginmali.
        if leid == "/brotin/oai":
            hala = ("?" + p.query) if (self.command == "GET" and p.query) \
                else ""
            return self._skrifa(301, "text/html", b"", haus={
                "Location": base + "/brotin/oai/" + hala})

        if leid.startswith("/god/oai"):
            return self._god(q, req_url)
        if leid == "/brotin/oai/":
            return self._brotin(q, req_url)

        self._skrifa(404, "text/plain", b"ekki fundid")

    # ---- goður endapunktur ---------------------------------------------
    def _god(self, q, req_url):
        base = self._base()
        verb = q.get("verb", "")
        if verb == "Identify":
            inni = (
                '<Identify><repositoryName>Hermir MSHL (heill)'
                '</repositoryName><baseURL>%s/god/oai</baseURL>'
                '<protocolVersion>2.0</protocolVersion>'
                '<adminEmail>oai@mshl.is</adminEmail>'
                '<earliestDatestamp>2026-05-01T10:00:00Z</earliestDatestamp>'
                '<deletedRecord>persistent</deletedRecord>'
                '<granularity>YYYY-MM-DDThh:mm:ssZ</granularity>'
                '</Identify>' % base)
            return self._xml(_umslag(inni, verb, req_url))
        if verb == "ListMetadataFormats":
            inni = ('<ListMetadataFormats>'
                    '<metadataFormat><metadataPrefix>oai_dc</metadataPrefix>'
                    '<schema>http://www.openarchives.org/OAI/2.0/oai_dc.xsd'
                    '</schema><metadataNamespace>'
                    'http://www.openarchives.org/OAI/2.0/oai_dc/'
                    '</metadataNamespace></metadataFormat>'
                    '<metadataFormat><metadataPrefix>isebel</metadataPrefix>'
                    '<schema>https://isebel.eu/isebel.xsd</schema>'
                    '<metadataNamespace>http://isebel.eu/ns'
                    '</metadataNamespace></metadataFormat>'
                    '</ListMetadataFormats>')
            return self._xml(_umslag(inni, verb, req_url))
        if verb == "ListSets":
            inni = ('<ListSets>'
                    '<set><setSpec>type:baer</setSpec>'
                    '<setName>Bæir</setName></set>'
                    '<set><setSpec>type:einstaklingur</setSpec>'
                    '<setName>Fólk</setName></set>'
                    '<set><setSpec>type:sogn</setSpec>'
                    '<setName>Sagnir</setName></set></ListSets>')
            return self._xml(_umslag(inni, verb, req_url))
        if verb in ("ListIdentifiers", "ListRecords"):
            return self._god_listi(verb, q, req_url, base)
        if verb == "GetRecord":
            aud = q.get("identifier", "")
            if q.get("metadataPrefix") not in (None, "oai_dc"):
                return self._xml(_villa("cannotDisseminateFormat", verb,
                                        req_url))
            for m in gogn.godar():
                if m["audkenni"] == aud:
                    inni = ('<GetRecord>%s</GetRecord>'
                            % gogn.faersla_god(m, base))
                    return self._xml(_umslag(inni, verb, req_url))
            return self._xml(_villa("idDoesNotExist", verb, req_url))
        return self._xml(_villa("badVerb", verb or "(ekkert)", req_url))

    def _god_listi(self, verb, q, req_url, base):
        if verb == "ListRecords" and q.get("metadataPrefix") not in (
                None, "oai_dc") and "resumptionToken" not in q:
            return self._xml(_villa("cannotDisseminateFormat", verb, req_url))
        allar = gogn.godar()
        sett = q.get("set")
        frm = q.get("from")
        until = q.get("until")
        token = q.get("resumptionToken")
        if (verb == "ListIdentifiers" and not token
                and "metadataPrefix" not in q):
            return self._xml(_villa("badArgument", verb, req_url))
        # sía
        valdar = allar
        if sett:
            valdar = [m for m in valdar if m["setSpec"] == sett]
        if frm:
            valdar = [m for m in valdar if m["datestamp"][:10] >= frm[:10]]
        if until:
            valdar = [m for m in valdar if m["datestamp"][:10] <= until[:10]]
        if not valdar:
            return self._xml(_villa("noRecordsMatch", verb, req_url))
        # blaðsíðun
        offset = int(token) if token and token.isdigit() else 0
        heild = len(valdar)
        bútur = valdar[offset:offset + gogn.SIDA]
        naest = offset + gogn.SIDA
        rt = ""
        if naest < heild:
            rt = ('<resumptionToken completeListSize="%d" cursor="%d">%d'
                  '</resumptionToken>' % (heild, offset, naest))
        else:
            rt = ('<resumptionToken completeListSize="%d" cursor="%d">'
                  '</resumptionToken>' % (heild, offset))
        if verb == "ListIdentifiers":
            hlutar = [('<header><identifier>%s</identifier><datestamp>%s'
                       '</datestamp><setSpec>%s</setSpec></header>'
                       % (m["audkenni"], m["datestamp"], m["setSpec"]))
                      for m in bútur]
            inni = '<ListIdentifiers>%s%s</ListIdentifiers>' % (
                "".join(hlutar), rt)
        else:
            hlutar = [gogn.faersla_god(m, base) for m in bútur]
            inni = '<ListRecords>%s%s</ListRecords>' % ("".join(hlutar), rt)
        return self._xml(_umslag(inni, verb, req_url))

    # ---- brotinn endapunktur -------------------------------------------
    def _brotin(self, q, req_url):
        base = self._base()
        verb = q.get("verb", "")
        brotnar = gogn.brotnar(base)  # [(aud, ds, set, xml)]
        if verb == "Identify":
            # baseURL AN skastriks -> gildran. Ekkert adminEmail.
            inni = (
                '<Identify><repositoryName>Hermir MSHL (gallaður)'
                '</repositoryName><baseURL>%s/brotin/oai</baseURL>'
                '<protocolVersion>2.0</protocolVersion>'
                '<earliestDatestamp>2026-05-01</earliestDatestamp>'
                '<deletedRecord>transient</deletedRecord>'
                '<granularity>YYYY-MM-DDThh:mm:ssZ</granularity>'
                '</Identify>' % base)
            return self._xml(_umslag(inni, verb, req_url), bom=True)
        if verb == "ListMetadataFormats":
            inni = ('<ListMetadataFormats><metadataFormat>'
                    '<metadataPrefix>oai_dc</metadataPrefix>'
                    '<schema>http://www.openarchives.org/OAI/2.0/oai_dc.xsd'
                    '</schema><metadataNamespace>'
                    'http://www.openarchives.org/OAI/2.0/oai_dc/'
                    '</metadataNamespace></metadataFormat>'
                    '</ListMetadataFormats>')
            return self._xml(_umslag(inni, verb, req_url), bom=True)
        if verb == "ListSets":
            # type:baer fyrst (fyrir E15), era:19c auglyst en tomt (E14)
            inni = ('<ListSets><set><setSpec>type:baer</setSpec>'
                    '<setName>Bæir</setName></set>'
                    '<set><setSpec>era:19c</setSpec>'
                    '<setName>19. öld</setName></set></ListSets>')
            return self._xml(_umslag(inni, verb, req_url), bom=True)
        if verb == "ListIdentifiers":
            sett = q.get("set")
            if sett == "era:19c":
                return self._xml(_villa("noRecordsMatch", verb, req_url),
                                 bom=True)
            if sett == "type:baer":
                # leki: 22 (einstaklingur) slaest inn i type:baer
                valdar = [b for b in brotnar if b[0].endswith(":21")
                          or b[0].endswith(":22")]
            else:
                valdar = brotnar
            hlutar = [('<header><identifier>%s</identifier><datestamp>%s'
                       '</datestamp><setSpec>%s</setSpec></header>'
                       % (b[0], b[1], b[2])) for b in valdar]
            inni = '<ListIdentifiers>%s</ListIdentifiers>' % "".join(hlutar)
            return self._xml(_umslag(inni, verb, req_url), bom=True)
        if verb == "ListRecords":
            token = q.get("resumptionToken")
            if token == "p2":
                # skemmd sida: PHP-fatal, olokad CDATA, styritakn
                return self._skrifa(200, "text/html; charset=utf-8",
                                    BOM + gogn.brotin_sida().encode("utf-8"))
            hlutar = [b[3] for b in brotnar]
            rt = ('<resumptionToken completeListSize="27" cursor="0">p2'
                  '</resumptionToken>')
            inni = '<ListRecords>%s%s</ListRecords>' % ("".join(hlutar), rt)
            return self._xml(_umslag(inni, verb, req_url), bom=True)
        if verb == "GetRecord":
            aud = q.get("identifier", "")
            for b in brotnar:
                if b[0] == aud:
                    inni = '<GetRecord>%s</GetRecord>' % b[3]
                    return self._xml(_umslag(inni, verb, req_url), bom=True)
            return self._xml(_villa("idDoesNotExist", verb, req_url),
                             bom=True)
        # villur-html gildran: badVerb kemur sem HTTP 500 HTML
        return self._skrifa(500, "text/html; charset=utf-8",
                            b"<html><body><b>Fatal error</b>: unknown verb"
                            b"</body></html>")

    def log_message(self, *a):
        pass


def bua_til(port=8766, host="127.0.0.1"):
    return ThreadingHTTPServer((host, port), Handler)

"""Færslusíða — læsileg síða fyrir eina færslu úr sýnisveitu.

Til hvers: gagnaeigandi sem á enga opna slóð á færslu (RÚV) fær hana hjá
Sagnatroginu. Slóðin fer í dc:identifier, Leitir tengir á hana, og síðan
vísar áfram á gagnaeigandann þar sem efnið sjálft fæst.

Síðan er merkt Sagnatroginu, ekki gagnaeigandanum: hún er færslusíða í
leitargátt MSHL, með lýsigögnum frá eigandanum, ekki eftirlíking af vef hans.
Allur texti er afkóðaður (html.escape) — lýsigögn eru aldrei HTML hér.
"""
import html
from urllib.parse import quote

LEITIR = ("https://gegnir-psb.primo.exlibrisgroup.com/nde/search?query=any,contains,%s"
          "&tab=ALLT&search_scope=MSHL_ALLT&vid=354ILC_NETWORK:MSHL_SAGNATROG_LEITIR_UNION&lang=is")

_STILL = """
:root{--bak:#f4ecdb;--spjald:#fffaf0;--texti:#2a2118;--grar:#6b5d4e;--lina:#d4c4ae;
--bl:#5c3d2e;--grar-bg:#efe4d0;--sans:"Iowan Old Style",Palatino,"Palatino Linotype",Georgia,serif;
--hn:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bak);color:var(--texti);font:17px/1.55 var(--sans)}
.innihald{max-width:820px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid var(--lina);padding:18px 0 12px}
.merki{display:flex;gap:8px;align-items:center;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--grar)}
.merki a{color:inherit;text-decoration:none}.merki img{height:34px}
main{padding:22px 0 40px}.teg{color:var(--grar);font-size:15px;margin:0 0 4px}
h1{font-size:30px;line-height:1.2;margin:0 0 8px;font-weight:600}
.dags{color:var(--grar);margin:0 0 18px}
.spjald{background:var(--spjald);border:1px solid var(--lina);border-radius:12px;padding:16px 20px;margin:0 0 16px}
.spjald h2{font-size:14px;letter-spacing:.06em;text-transform:uppercase;color:var(--grar);margin:0 0 8px;font-weight:600}
.lysing{white-space:pre-line;margin:0}
table{border-collapse:collapse;width:100%;font-size:15px}td{padding:5px 0;vertical-align:top;border-bottom:1px solid var(--grar-bg)}
td.hl{color:var(--grar);text-align:right;padding-left:12px}
.flogur{display:flex;flex-wrap:wrap;gap:6px}.flogur span{background:var(--grar-bg);border-radius:999px;padding:3px 11px;font-size:14px}
ol,ul{margin:0;padding-left:22px}a{color:var(--bl)}
.hnappar{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 18px}
.hnappur{display:inline-block;background:var(--bl);color:#fff;text-decoration:none;border-radius:8px;padding:10px 16px;font:15px var(--hn)}
.hnappur.aukab{background:var(--grar-bg);color:var(--texti)}
.smatt{color:var(--grar);font-size:14px}
footer{border-top:1px solid var(--lina);padding:14px 0 30px;color:var(--grar);font-size:13px}
"""


def _e(s):
    return html.escape(str(s or ""), quote=True)


def _radir(par):
    return "".join("<tr><td>%s</td><td class=\"hl\">%s</td></tr>" % (_e(a), _e(b)) for a, b in par if b)


def smida(veita, f, rotarslod=""):
    """HTML fyrir færslu `f` (Synisveita.faersla) úr sýnisveitu `veita`."""
    uppruni = veita.uppruni or veita.heiti
    ag = veita.adgangur or {}
    dags = f["tekid_upp"] or f["dags"]
    dagslina = []
    if f["tekid_upp"]:
        dagslina.append("Tekið upp " + f["tekid_upp"])
    if f["utsent"]:
        dagslina.append("Útsent " + ", ".join(f["utsent"]))
    if not dagslina and dags:
        dagslina.append(dags)

    folk = "".join("<tr><td>%s</td><td class=\"hl\">%s</td></tr>" % (_e(p["nafn"]), _e(p["hlutverk"]))
                   for p in f["folk"])
    efni = "".join("<span>%s</span>" % _e(e) for e in f["flokkar"] + f["efnisord"])
    hluti = ""
    if f["foreldri"]:
        hluti = ("<div class=\"spjald\"><h2>Hluti af</h2><a href=\"%s/%s/%s\">%s</a></div>"
                 % (rotarslod, _e(veita.nafn), _e(f["foreldri"]["stutt"]), _e(f["foreldri"]["titill"])))
    born = ""
    if f["born"]:
        born = ("<div class=\"spjald\"><h2>Í þessari færslu</h2><ol>%s</ol></div>"
                % "".join("<li><a href=\"%s/%s/%s\">%s</a></li>" % (rotarslod, _e(veita.nafn), _e(b["stutt"]), _e(b["titill"]))
                          for b in f["born"]))
    upplys = _radir([("Safnnúmer", ", ".join(f["safnnumer"])), ("Frumeintak", f["frumeintak"].replace("Frumeintak í safni RÚV: ", "")),
                     ("Miðill", f["midill"]), ("Lengd", _lengd(f["lengd"])),
                     ("Útgefandi", ", ".join(f["utgefandi"])), ("Auðkenni", f["audkenni"])])
    hnappar = ""
    if ag.get("slod"):
        # nýr flipi: notandinn heldur færslusíðunni opinni meðan hann biður um efnið
        hnappar += ("<a class=\"hnappur\" href=\"%s\" target=\"_blank\" rel=\"noopener\">%s</a>"
                    % (_e(ag["slod"]), _e(ag.get("texti") or "Hjá eiganda")))
    hnappar += "<a class=\"hnappur aukab\" href=\"%s\">Leita í Sagnatroginu</a>" % _e(LEITIR % quote(f["titill"]))

    return """<!DOCTYPE html>
<html lang="is"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>%(titill)s — Sagnatrog</title>
<link rel="icon" type="image/png" href="%(rot)s/vefur/favicon.png">
<style>%(still)s</style></head><body>
<header><div class="innihald merki">
<a href="https://gegnir-psb.primo.exlibrisgroup.com/nde/home?vid=354ILC_NETWORK:MSHL_SAGNATROG_LEITIR_UNION&amp;lang=is"><img src="%(rot)s/vefur/sagnatrog.png" alt="Sagnatrogið"></a>
<span>Sagnatrog · Færslusíða · Lýsigögn frá %(uppruni)s</span></div></header>
<main class="innihald">
<p class="teg">%(teg)s</p>
<h1>%(titill)s</h1>
<p class="dags">%(dagslina)s</p>
<div class="hnappar">%(hnappar)s</div>
%(lysing)s
%(folk)s
%(efni)s
%(hluti)s
%(born)s
<div class="spjald"><h2>Um færsluna</h2><table>%(upplys)s</table></div>
<p class="smatt">%(rettindi)s</p>
</main>
<footer><div class="innihald">Færslusíða í Sagnatroginu, leitargátt Miðstöðvar stafrænna hugvísinda og lista.
Lýsigögnin koma frá %(uppruni)s; efnið sjálft er hjá eigandanum. Síðan gefur færslunni opna,
varanlega slóð meðan eigandinn hefur hana ekki sjálfur.</div></footer>
</body></html>""" % {
        "titill": _e(f["titill"]), "rot": rotarslod, "still": _STILL, "uppruni": _e(uppruni),
        "teg": _e(" · ".join(f["tegund"])), "dagslina": _e(" · ".join(dagslina)),
        "hnappar": hnappar,
        "lysing": ("<div class=\"spjald\"><h2>Lýsing</h2><p class=\"lysing\">%s</p></div>" % _e(f["lysing"])) if f["lysing"] else "",
        "folk": ("<div class=\"spjald\"><h2>Fólk</h2><table>%s</table></div>" % folk) if folk else "",
        "efni": ("<div class=\"spjald\"><h2>Efni</h2><div class=\"flogur\">%s</div></div>" % efni) if efni else "",
        "hluti": hluti, "born": born, "upplys": upplys, "rettindi": _e(f["rettindi"]),
    }


def _lengd(iso):
    """'PT8M25S' → '8:25' · 'PT1H38M40S' → '1:38:40'."""
    import re
    m = re.match(r"^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", iso or "")
    if not m or not any(m.groups()):
        return ""
    k, mi, s = (int(x or 0) for x in m.groups())
    return ("%d:%02d:%02d" % (k, mi, s)) if k else ("%d:%02d" % (mi, s))

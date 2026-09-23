"""Vörn fyrir opna útgáfu Gáttagægis.

Á eigin vél (127.0.0.1) þarf ekkert af þessu. Um leið og þjónninn er opinn á
netinu sækir hann hvaða slóð sem gestur límir inn — og þá má sú slóð ekki
vísa inn í innra net hýsingaraðilans eða á lýsigagnaþjónustu skýsins
(169.254.169.254, sama hjá GCP, AWS og Azure). Það er allt sem vörnin gerir:
hún hleypir aðeins opinberum http(s)-slóðum út.

    from .vorn import athuga, Hafnad
    athuga(slod)   # skilar slóðinni, eða kastar Hafnad með skýringu

Nafnið er leyst hér og aftur í urllib — sú gjá er þekkt og þolanleg fyrir
prófunartæki sem sækir fáeinar beiðnir.
"""
import ipaddress
import socket
import urllib.parse

LEYFDAR_GATTIR = (80, 443, 8080, 8000)
LYSIGOGN_SKYS = "169.254.169.254"


class Hafnad(Exception):
    """Slóðin fær ekki að fara út — skilaboðin eru ætluð notandanum."""


def _leysa(hysill):
    """Sjálfgefinn nafnaþjónn: allar IP-tölur sem nafnið vísar á."""
    return [sockaddr[0] for *_, sockaddr in socket.getaddrinfo(hysill, None)]


def _innri(ip):
    return (ip.is_private or ip.is_loopback or ip.is_link_local
            or ip.is_multicast or ip.is_reserved or ip.is_unspecified)


def athuga(slod, leysa=_leysa):
    """Staðfestir að slóðin sé opinber http(s)-slóð. Skilar henni annars kastar."""
    u = urllib.parse.urlparse(slod)
    if u.scheme not in ("http", "https"):
        raise Hafnad("Aðeins http og https eru leyfð (fékk %r)."
                     % (u.scheme or "ekkert"))
    if not u.hostname:
        raise Hafnad("Slóðin hefur engan hýsil.")
    if u.username or u.password:
        raise Hafnad("Notandanafn og lykilorð í slóð eru ekki leyfð.")
    if u.port is not None and u.port not in LEYFDAR_GATTIR:
        raise Hafnad("Gátt %d er ekki leyfð." % u.port)
    try:
        ip_tolur = leysa(u.hostname)
    except OSError as e:
        raise Hafnad("Hýsillinn fannst ekki: %s" % e)
    for tala in ip_tolur:
        ip = ipaddress.ip_address(tala)
        if str(ip) == LYSIGOGN_SKYS:
            raise Hafnad("Lýsigagnaþjónusta skýsins. Ekki leyft.")
        if _innri(ip):
            raise Hafnad("Hýsillinn vísar á innra net (%s). Ekki leyft." % ip)
    return slod

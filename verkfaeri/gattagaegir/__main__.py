"""Gáttagægir CLI.

  python3 -m verkfaeri.gattagaegir                 # ræsir vefþjón (8765)
  python3 -m verkfaeri.gattagaegir --med-hermi     # + hermir (8766)
  python3 -m verkfaeri.gattagaegir profa <slod>    # keyrir í skel, prentar
"""
import argparse
import json
import sys
import threading

from . import UTGAFA
from . import velin
from .thjonn import bua_til as bua_til_thjon


def _profa(a):
    stillingar = {"sidur": a.sidur, "syni": a.syni, "sett": a.sett,
                  "slodaprof": not a.engin_slodaprof,
                  "bid_ms": int(a.bid * 1000)}
    skyrsla = velin.keyra_allt(a.slod, stillingar, netfang=a.netfang)
    if a.json:
        print(json.dumps(skyrsla, ensure_ascii=False, indent=1))
    else:
        print(skyrsla["texti"])
    s = skyrsla["samantekt"]
    return 1 if s["villur"] else 0


def _thjonn(a):
    if a.med_hermi:
        from .herma.hermir import bua_til as bua_hermi
        hermir = bua_hermi(a.hermi_port, a.host)
        threading.Thread(target=hermir.serve_forever, daemon=True).start()
        print("Hermir:  http://%s:%d/god/oai  ·  http://%s:%d/brotin/oai"
              % (a.host, a.hermi_port, a.host, a.hermi_port))
    thj = bua_til_thjon(a.port, a.host)
    print("Gáttagægir %s á http://%s:%d" % (UTGAFA, a.host, a.port))
    try:
        thj.serve_forever()
    except KeyboardInterrupt:
        thj.shutdown()
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="gattagaegir",
                               description="OAI-PMH prófun fyrir MSHL")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--med-hermi", action="store_true",
                   help="ræsa staðbundinn OAI-hermi samhliða")
    p.add_argument("--hermi-port", type=int, default=8766)
    und = p.add_subparsers(dest="skipun")
    pr = und.add_parser("profa", help="keyra í skel og prenta samantekt")
    pr.add_argument("slod")
    pr.add_argument("--json", action="store_true")
    pr.add_argument("--sidur", type=int, default=3)
    pr.add_argument("--syni", type=int, default=10)
    pr.add_argument("--sett", type=int, default=5)
    pr.add_argument("--engin-slodaprof", action="store_true")
    pr.add_argument("--bid", type=float, default=0.25)
    pr.add_argument("--netfang", default=None)
    a = p.parse_args(argv)
    if a.skipun == "profa":
        return _profa(a)
    return _thjonn(a)


if __name__ == "__main__":
    sys.exit(main())

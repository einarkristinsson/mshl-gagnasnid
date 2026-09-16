"""Ræsir herminn einan og sér: python3 -m verkfaeri.gattagaegir.herma"""
import argparse

from .hermir import bua_til


def main():
    p = argparse.ArgumentParser(description="OAI-PMH hermir MSHL")
    p.add_argument("--port", type=int, default=8766)
    p.add_argument("--host", default="127.0.0.1")
    a = p.parse_args()
    thj = bua_til(a.port, a.host)
    print("Hermir á http://%s:%d" % (a.host, a.port))
    print("  heill:    http://%s:%d/god/oai" % (a.host, a.port))
    print("  brotinn:  http://%s:%d/brotin/oai" % (a.host, a.port))
    try:
        thj.serve_forever()
    except KeyboardInterrupt:
        thj.shutdown()


if __name__ == "__main__":
    main()

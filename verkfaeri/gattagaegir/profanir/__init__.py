"""Prófanir Gáttagægis (unittest, án nets)."""
import threading
import time

from ..herma.hermir import bua_til


class Hermistjori:
    """Ræsir herminn á lausu porti fyrir prófun; lokar við __exit__."""

    def __enter__(self):
        self.thj = bua_til(0)
        self.port = self.thj.server_address[1]
        self.thradur = threading.Thread(target=self.thj.serve_forever,
                                        daemon=True)
        self.thradur.start()
        time.sleep(0.1)
        self.base = "http://127.0.0.1:%d" % self.port
        return self

    def __exit__(self, *a):
        self.thj.shutdown()

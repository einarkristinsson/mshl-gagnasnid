"""Athuganir Gáttagægis — grunngerðir og skráning.

Hver athugun er fall (samhengi) -> Nidurstada. Alvarleiki er fastur á
hverri athugun og lýsir því hvað „fell" þýðir:
  villa    = skylda (M) eða staðfest gildra (🔴) — verður að laga
  advorun  = ráðlagt (R) eða gildaform — ætti að laga
  abending = valkvæmt (O) eða vélræn ágiskun — til skoðunar
"""

# alvarleiki
VILLA = "villa"
ADVORUN = "advorun"
ABENDING = "abending"

# staða niðurstöðu
STODST = "stodst"
FELL = "fell"
SLEPPT = "sleppt"

# hópar
ENDAPUNKTUR = "endapunktur"
FAERSLUR = "faerslur"
HREINLAETI = "hreinlaeti"
GILDI = "gildi"

HOPHEITI = {
    ENDAPUNKTUR: "Endapunktur",
    FAERSLUR: "Færslur",
    HREINLAETI: "Hreinleiki",
    GILDI: "Gildi",
}


class Nidurstada:
    def __init__(self, kenni, hopur, heiti, alvarleiki, gildra=False,
                 tilvisun=None):
        self.kenni = kenni
        self.hopur = hopur
        self.heiti = heiti
        self.alvarleiki = alvarleiki
        self.gildra = gildra
        self.tilvisun = tilvisun
        self.stada = STODST
        self.skilabod = ""
        self.tilvik = []        # [{'audkenni','reitur','gildi','skyring'}]
        self.fjoldi = {}        # t.d. {'skodad':10,'fell':2}
        self.lagfaering = None

    # þægindaaðferðir
    def stodst_(self, skilabod="", **fjoldi):
        self.stada = STODST
        self.skilabod = skilabod
        self.fjoldi.update(fjoldi)
        return self

    def fell_(self, skilabod, lagfaering=None, **fjoldi):
        self.stada = FELL
        self.skilabod = skilabod
        if lagfaering:
            self.lagfaering = lagfaering
        self.fjoldi.update(fjoldi)
        return self

    def sleppt_(self, skilabod):
        self.stada = SLEPPT
        self.skilabod = skilabod
        return self

    def baeta(self, audkenni=None, reitur=None, gildi=None, skyring=None):
        if len(self.tilvik) < 20:
            self.tilvik.append({"audkenni": audkenni, "reitur": reitur,
                                "gildi": gildi, "skyring": skyring})
        return self

    def json(self):
        return {
            "kenni": self.kenni, "hopur": self.hopur, "heiti": self.heiti,
            "stada": self.stada, "alvarleiki": self.alvarleiki,
            "gildra": self.gildra, "skilabod": self.skilabod,
            "tilvik": self.tilvik, "fjoldi": self.fjoldi,
            "tilvisun": self.tilvisun, "lagfaering": self.lagfaering,
        }


class Samhengi:
    """Sameiginlegt ástand sem athuganir lesa úr (og fáar bæta í)."""

    def __init__(self, slod, saekjari, stillingar, stopp=None):
        self.slod = slod
        self.saekjari = saekjari
        self.stillingar = stillingar
        self.stopp = stopp
        self.svor = {}            # nafn -> Skjal
        self.hra = {}             # nafn -> Svar (hrátt HTTP-svar)
        self.oll_svor = []        # öll Svar sem sáust (til hreinlætis)
        self.identify = {}        # greint Identify
        self.faerslur = []        # sýni af færslum (S)
        self.hausar_p1 = []       # ListIdentifiers síða 1
        self.token = None
        self.completeListSize = None
        self.listrecords_sidur = 0
        self.getrecord_fjoldi = 0

    def n(self, kenni, hopur, heiti, alvarleiki, gildra=False, tilvisun=None):
        return Nidurstada(kenni, hopur, heiti, alvarleiki, gildra, tilvisun)

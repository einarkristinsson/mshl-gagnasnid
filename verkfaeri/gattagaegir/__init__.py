"""Gáttagægir — vefprófun á OAI-PMH endapunktum fyrir gagnaveitur MSHL.

Hreint python3 úr stýrikerfinu — engin ytri söfn, ekkert pip install.
Sjá README.md í þessari möppu.
"""

UTGAFA = "0.1"


def notandastrengur(netfang=None):
    """User-Agent sem segir hver er á ferð og hvernig má ná í hann.

    Sama kurteisi og saekja-oai.py: auðkennanlegur strengur með netfangi.
    """
    grunnur = "MSHL-Gattagaegir/%s (mshl-gagnasnid; OAI-profun)" % UTGAFA
    if netfang:
        return "%s; %s" % (grunnur[:-1], netfang) + ")"
    return grunnur

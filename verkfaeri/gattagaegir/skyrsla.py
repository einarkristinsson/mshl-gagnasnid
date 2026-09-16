"""Afritanleg Markdown-samantekt sem speglar GATLISTI.md."""

_TAKN = {"stodst": "x", "fell": " ", "sleppt": "~"}


def markdown(skyrsla):
    L = []
    idf = skyrsla.get("identify", {})
    syni = skyrsla.get("syni", {})
    st = skyrsla.get("samantekt", {})
    nafn = idf.get("repositoryName") or skyrsla.get("slod")
    L.append("# Gáttagægir — %s" % nafn)
    L.append("Slóð: %s · Mælt: %s · Gáttagægir %s"
             % (skyrsla.get("slod"), skyrsla.get("lokid"),
                skyrsla.get("utgafa")))
    cls = syni.get("completeListSize")
    L.append("Sýni: %s færslur (%s síður ListRecords + %s GetRecord)%s · "
             "%s beiðnir"
             % (syni.get("faerslur"), syni.get("listrecords_sidur"),
                syni.get("getrecord"),
                (" · completeListSize %s" % cls) if cls else "",
                syni.get("beidnir")))
    L.append("Niðurstaða: %d villur · %d aðvaranir · %d ábendingar · "
             "%d stóðust · %d sleppt"
             % (st.get("villur", 0), st.get("advaranir", 0),
                st.get("abendingar", 0), st.get("stodst", 0),
                st.get("sleppt", 0)))
    L.append("")
    for hopur in skyrsla.get("hopar", []):
        L.append("## %s" % hopur["heiti"])
        for a in hopur["athuganir"]:
            takn = _TAKN.get(a["stada"], " ")
            merki = "🔴 " if a.get("gildra") and a["stada"] == "fell" else ""
            lina = "- [%s] %s%s" % (takn, merki, a["heiti"])
            if a["stada"] == "fell" and a.get("skilabod"):
                lina += " — %s" % a["skilabod"]
            elif a["stada"] == "sleppt":
                lina += " — sleppt"
            L.append(lina)
        L.append("")
    L.append("## Ekki prófað sjálfvirkt")
    L.append("- Vélþýðingar í eigin reit · Lesa tíu færslur "
             "(sjá „Færslur í sýni“)")
    return "\n".join(L)

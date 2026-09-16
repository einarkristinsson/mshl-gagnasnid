"""Gagnasýni fyrir herminn — góðar færslur og gallaðar."""

NS = ('xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" '
      'xmlns:dc="http://purl.org/dc/elements/1.1/" '
      'xmlns:dcterms="http://purl.org/dc/terms/" '
      'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
      'xmlns:mshl="https://mshl.is/terms#"')

# þrjú sniðmát: staður, einstaklingur, sögn
_SNIDMAT = [
    {"tegund": "baer", "type_is": "Bær", "type_en": "Place",
     "titill": "Drangshlíð", "efni": [("Bær", "1000001")],
     "stadur": [("mshl:sokn", "Eyvindarhólasókn"),
                ("mshl:sysla", "Rangárvallasýsla")],
     "point": "POINT(-19.55 63.52)", "date": "1703/1920",
     "hofundur": None},
    {"tegund": "einstaklingur", "type_is": "Manneskja", "type_en": "Person",
     "titill": "Jón Árnason", "efni": [("Þjóðsagnasöfnun", "1000002")],
     "stadur": [("mshl:sysla", "Eyjafjarðarsýsla")],
     "point": "POINT(-18.09 65.68)", "date": "1819/1888",
     "hofundur": ("Jón Árnason", "skrásetjari")},
    {"tegund": "sogn", "type_is": "Sögn", "type_en": "Legend",
     "titill": "Sagan af Skarðsárdraugnum", "efni": [("Draugar", "1000003")],
     "stadur": [("mshl:sokn", "Skarðssókn")],
     "point": "POINT(-20.11 63.99)", "date": "1887",
     "hofundur": ("Mikkalína Friðriksdóttir", "heimildarmaður")},
]

FJOLDI_GODUR = 30
SIDA = 12  # síðustærð -> 3 síður (12,12,6)


def godar():
    """Skilar lista af færsludagbókum (dict) fyrir góða endapunktinn."""
    ut = []
    for i in range(FJOLDI_GODUR):
        m = dict(_SNIDMAT[i % 3])
        n = i + 1
        dagur = 1 + (i % 20)
        m["n"] = n
        m["audkenni"] = "oai:god.mshl.is:%s:%d" % (m["tegund"], n)
        m["datestamp"] = "2026-05-%02dT10:00:00Z" % dagur
        m["setSpec"] = "type:%s" % m["tegund"]
        m["titill"] = "%s (%d)" % (m["titill"], n)
        ut.append(m)
    return ut


def _reitir_god(m, base):
    L = []
    L.append('<dc:identifier>%s</dc:identifier>' % m["audkenni"])
    L.append('<dc:identifier>%s/god/hlutur/%d</dc:identifier>'
             % (base, m["n"]))
    L.append('<dc:identifier>%s/god/myndir/%d.png</dc:identifier>'
             % (base, m["n"]))
    L.append('<dc:title xml:lang="is">%s</dc:title>' % m["titill"])
    L.append('<dc:type xml:lang="is">%s</dc:type>' % m["type_is"])
    L.append('<dc:type xml:lang="en">%s</dc:type>' % m["type_en"])
    for txt, ident in m["efni"]:
        L.append('<dc:subject xml:lang="is" xsi:type="mshl:efnisord" '
                 'mshl:id="%s">%s</dc:subject>' % (ident, txt))
    for xsi, txt in m["stadur"]:
        L.append('<dcterms:spatial xsi:type="%s" xml:lang="is">%s'
                 '</dcterms:spatial>' % (xsi, txt))
    L.append('<dcterms:spatial xsi:type="dcterms:Point">%s'
             '</dcterms:spatial>' % m["point"])
    L.append('<dc:date>%s</dc:date>' % m["date"])
    if m["hofundur"]:
        nafn, hlutverk = m["hofundur"]
        L.append('<dc:creator mshl:role="%s">%s</dc:creator>'
                 % (hlutverk, nafn))
    L.append('<dc:publisher xml:lang="is">Miðstöð stafrænna hugvísinda'
             '</dc:publisher>')
    L.append('<dc:language>is</dc:language>')
    L.append('<dc:rights>https://creativecommons.org/licenses/by/4.0/'
             '</dc:rights>')
    return "".join(L)


def faersla_god(m, base):
    haus = ('<header><identifier>%s</identifier><datestamp>%s</datestamp>'
            '<setSpec>%s</setSpec></header>'
            % (m["audkenni"], m["datestamp"], m["setSpec"]))
    meta = ('<metadata><oai_dc:dc %s>%s</oai_dc:dc></metadata>'
            % (NS, _reitir_god(m, base)))
    return '<record>%s%s</record>' % (haus, meta)


# ----------------------------------------------------------------------
# Gallaðar færslur (brotinn endapunktur). Hver sýnir eina eða fleiri gildrur.
# ----------------------------------------------------------------------
def brotnar(base):
    """Skilar (audkenni, datestamp, setSpec, record_xml) fyrir brotinn."""
    R = []

    def rec(n, haus_set, reitir, eydd=False, tomt=False):
        aud = "oai:brotin.mshl.is:hlutur:%d" % n
        ds = "2026-05-%02dT10:00:00Z" % (1 + (n % 20))
        if tomt:
            meta = '<metadata><oai_dc:dc %s></oai_dc:dc></metadata>' % NS
        elif eydd:
            meta = ""
        else:
            meta = ('<metadata><oai_dc:dc %s>%s</oai_dc:dc></metadata>'
                    % (NS, reitir))
        stada = ' status="deleted"' if eydd else ""
        haus = ('<header%s><identifier>%s</identifier><datestamp>%s'
                '</datestamp><setSpec>%s</setSpec></header>'
                % (stada, aud, ds, haus_set))
        return (aud, ds, haus_set, '<record>%s%s</record>' % (haus, meta))

    # 21: forskeyti í gildi, þágufall, öfug hnit, None-dagsetning, tómt format
    R.append(rec(21, "type:baer",
        '<dc:identifier>%s/brotin/hlutur/21</dc:identifier>'
        '<dc:identifier>%s/brotin/mynd-sida/21.jpg</dc:identifier>'
        '<dc:title xml:lang="is">Kaldaðarnesi</dc:title>'
        '<dc:type xml:lang="is">Bær</dc:type>'
        '<dc:type xml:lang="en">Place</dc:type>'
        '<dc:subject>Draugar</dc:subject>'
        '<dc:coverage>Sýsla: Rangárvallasýsla</dc:coverage>'
        '<dcterms:spatial>Kaldaðarnesi</dcterms:spatial>'
        '<dcterms:spatial xsi:type="dcterms:Point">POINT(63.5 -19.6)'
        '</dcterms:spatial>'
        '<dc:date>None</dc:date>'
        '<dc:format></dc:format>'
        '<dc:language>Íslenska</dc:language>'
        % (base, base)))
    # 22: dc:type án lang-pars, dc:source sem slóð, æviár í nafni, ekki rights
    R.append(rec(22, "type:einstaklingur",
        '<dc:identifier>%s/brotin/hlutur/22</dc:identifier>'
        '<dc:title xml:lang="is">Sigfús Eymundsson</dc:title>'
        '<dc:type>Photography</dc:type>'
        '<dc:subject>Ljósmyndun</dc:subject>'
        '<dc:coverage>Reykjavík</dc:coverage>'
        '<dc:creator>Sigfús Eymundsson (25.5.1837 - 20.10.1911)</dc:creator>'
        '<dc:source>https://safn.is/heimild/22</dc:source>'
        '<dc:date>1920 - 1925</dc:date>'
        % base))
    # 23: eigin reitur í oai_dc, HTML í description, vantar titil
    R.append(rec(23, "type:sogn",
        '<dc:identifier>%s/brotin/hlutur/23</dc:identifier>'
        '<dc:type xml:lang="is">Sögn</dc:type>'
        '<dc:type xml:lang="en">Legend</dc:type>'
        '<dc:subject>Huldufólk</dc:subject>'
        '<dc:coverage>Skálholt</dc:coverage>'
        '<dc:description><![CDATA[Fyrsta lína.<br>Önnur lína.]]>'
        '</dc:description>'
        '<sarpur:safnnumer xmlns:sarpur="https://sarpur.is/ns">'
        'SÁM 88/1559</sarpur:safnnumer>'
        % base))
    # 24: tómt oai_dc:dc (haus en engin gögn)
    R.append(rec(24, "type:sogn", "", tomt=True))
    return R


# PHP-fatal síða með ólokað CDATA og stýritákni — fellir ListRecords.
def brotin_sida():
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">'
        '<ListRecords><record><header>'
        '<identifier>oai:brotin.mshl.is:hlutur:27</identifier>'
        '</header><metadata><description><![CDATA[ '
        'texti sem \x01 gleymdist a\xf0 loka'
        '<b>Fatal error</b>: Uncaught Error in /oai/list.php on line 88'
    )

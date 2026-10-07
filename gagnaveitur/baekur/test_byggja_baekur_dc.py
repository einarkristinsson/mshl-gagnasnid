"""Prófanir á byggja_baekur_dc.py (unittest, án nets).

    python3 -m unittest discover -s gagnaveitur/baekur

Dæmin eru orðrétt úr edm-sniði Bækur.is eins og það var 1.10.2026.
"""
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import byggja_baekur_dc as b  # noqa: E402

DC = "{http://purl.org/dc/elements/1.1/}"
DCT = "{http://purl.org/dc/terms/}"
MSHL = "{https://mshl.is/terms#}"
XSI = "{http://www.w3.org/2001/XMLSchema-instance}"
LANG = "{http://www.w3.org/XML/1998/namespace}lang"


def _svar(records, token=""):
    """Heilt OAI-svar eins og Bækur.is skilar því (sömu forskeyti, SKOS = core:)."""
    tok = ('<resumptionToken completeListSize="2984" cursor="25">%s</resumptionToken>' % token
           if token else "")
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            "<?xml-stylesheet type='text/xsl' href='oai.xsl' ?>"
            '<OAI-PMH xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" '
            'xmlns:core="http://www.w3.org/2004/02/skos/core#" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:edm="http://www.europeana.eu/schemas/edm/" '
            'xmlns:ore="http://www.openarchives.org/ore/terms/" '
            'xmlns="http://www.openarchives.org/OAI/2.0/">'
            "<responseDate>2026-10-01T11:33:57.870Z</responseDate>"
            '<request verb="ListRecords" metadataPrefix="edm">http://baekur.is/oai</request>'
            "<ListRecords>%s%s</ListRecords></OAI-PMH>" % ("".join(records), tok)
            ).encode("utf-8")


def _record(uuid, slug, cho, agentar="", rettindi="http://rightsstatements.org/page/InC/1.0/",
            datestamp="2023-10-15T02:47:39Z"):
    bok = "http://baekur.is/bok/%s/%s" % (uuid, slug)
    return ("<record><header><identifier>oai:baekur.is:books/%(u)s</identifier>"
            "<datestamp>%(ds)s</datestamp></header><metadata><rdf:RDF>"
            '<edm:ProvidedCHO rdf:about="http://baekur.is/rdf/cho/%(u)s">%(cho)s'
            '<edm:rights rdf:resource="%(r)s"/><dc:identifier>%(bok)s</dc:identifier>'
            "</edm:ProvidedCHO>%(ag)s"
            '<ore:Aggregation rdf:about="http://baekur.is/rdf/aggregation/%(u)s">'
            '<edm:dataProvider xml:lang="en">National and University Library of Iceland</edm:dataProvider>'
            '<edm:isShownAt rdf:resource="%(bok)s"/>'
            '<edm:object rdf:resource="http://baekur.is/cover/%(u)s"/>'
            '<edm:rights rdf:resource="%(r)s"/></ore:Aggregation>'
            "</rdf:RDF></metadata></record>"
            % {"u": uuid, "ds": datestamp, "cho": cho, "ag": agentar, "r": rettindi, "bok": bok})


def _agent(n, nafn, fra=None, til=None):
    return ('<edm:Agent rdf:about="http://baekur.is/rdf/agent/%s"><core:prefLabel>%s</core:prefLabel>'
            "%s%s</edm:Agent>" % (n, nafn, "<edm:begin>%s</edm:begin>" % fra if fra else "",
                                  "<edm:end>%s</edm:end>" % til if til else ""))


def _hofundur(n):
    return '<dc:creator rdf:resource="http://baekur.is/rdf/agent/%s"/>' % n


def _stadir(geo, loc):
    return ('<dcterms:spatial rdf:resource="http://sws.geonames.org/%s"/>'
            '<dcterms:spatial rdf:resource="http://id.loc.gov/vocabulary/countries/%s"/>' % (geo, loc))


SJO = _record("0c11ccb5-0929-49db-bb27-cb8f260ef28b", "Sjo_Gudraekilegar_umthenkingar_", (
    "<dc:title>Sjö Guðrækilegar umþenkingar, eður Eintal kristins manns við sjálfan sig "
    "hvern dag í vikunni, að kvöldi og morgni</dc:title>" + _hofundur(85685)
    + '<dc:subject xml:lang="is">Sálmar</dc:subject><dc:subject xml:lang="is">Bænir</dc:subject>'
    "<dc:date>1860</dc:date><dc:type xml:lang=\"en\">Book</dc:type><dc:language>is</dc:language>"
    "<dcterms:extent>94 p.</dcterms:extent><edm:type>TEXT</edm:type>"
    '<dcterms:isReferencedBy rdf:resource="http://bokaskra.landsbokasafn.is/search?s_any=991005534569706886"/>'
    + _stadir("2629691", "ic")), _agent(85685, "Hallgrímur Pétursson", "1614", "1674"))

NORDISK = _record("012886d3-35fb-4b1d-8413-84f233494916", "Nordisk", (
    "<dc:title>Nordisk Mythologi</dc:title>" + _hofundur(242473) + _hofundur(80429)
    + "<dc:date>1859</dc:date><dc:language>da</dc:language><dcterms:extent>140 p.</dcterms:extent>"
    + _stadir("2623032", "dk")),
    _agent(242473, "Arentzen, Kristian,", "1823", "1899")
    + _agent(80429, "Steingrímur Thorsteinsson", "1831", "1913"), datestamp="2023-10-01T03:19:13Z")

# „Ísland“ sem höfundur tilskipunar; LoC null → GeoNames Ísland er sjálfgefið gildi
AUGLYSING = _record("1aa23922-6861-44b1-b577-8df0d581abaf", "Auglysing", (
    "<dc:title>Auglýsing</dc:title>" + _hofundur(102619)
    + '<dc:subject xml:lang="is">Tilskipanir</dc:subject><dc:date>1809</dc:date>'
    "<dc:language>is</dc:language><dcterms:extent>4 p.</dcterms:extent>"
    + _stadir("2629691", "null")), _agent(102619, "Ísland"))

# Biblía: „höfundurinn“ er samræmdur titill; enginn efnisorð í heimild
BIBLIA = _record("0006ba32-6c16-4194-aad9-bac42d8b0850", "Biblia", (
    "<dc:title>Biblía</dc:title>" + _hofundur(172319)
    + "<dc:date>1859</dc:date><dc:language>is</dc:language><dcterms:extent>1121 p.</dcterms:extent>"
    + _stadir("2629691", "ic")), _agent(172319, "Biblían"))

STULKA = _record("0a693aae-574f-4ca7-b342-c96f939eb0fe", "Stulka", (
    "<dc:title>Stúlka</dc:title>" + _hofundur(198890)
    + '<dc:subject xml:lang="is">Ljóð</dc:subject><dc:date>1876</dc:date>'
    "<dc:language>is</dc:language><dcterms:extent>148 p.</dcterms:extent>"
    + _stadir("2629691", "ic")), _agent(198890, "Júlíana Jónsdóttir", "1838", "1917"),
    rettindi="https://creativecommons.org/publicdomain/mark/1.0/")


class Folk(unittest.TestCase):
    def test_manneskjur(self):
        self.assertEqual(b.flokka("Hallgrímur Pétursson", "1614", "1674"), "persona")
        self.assertEqual(b.flokka("Luther, Martin,", "1483", "1546"), "persona")
        self.assertEqual(b.flokka("Hómer,"), "persona")              # komma = öfugt nafn
        self.assertEqual(b.flokka("Ferrall, J. S."), "persona")
        self.assertEqual(b.flokka("Jón Einarsson"), "persona")       # engin ár, en nafn
        self.assertEqual(b.flokka("Laozi"), "persona")
        self.assertEqual(b.flokka("Bera Nordal", "1954"), "persona")

    def test_stofnanir(self):
        for n in ("Ísland", "Danmörk", "Hið íslenska bókmenntafélag", "Yfirrétturinn á Íslandi",
                  "Vesturamtið.", "Kvennalistinn (1983-2000)", "Prestaskólinn í Reykjavík.",
                  "Nordiska Konstförbundet", "Septembersýningin", "Kungliga Biblioteket (Svíþjóð)",
                  "Landsbókasafn Íslands – Háskólabókasafn", "Det Stærke lys"):
            self.assertEqual(b.flokka(n), "stofnun", n)
        # sýning með upphafsári er samt ekki manneskja
        self.assertEqual(b.flokka("Nordisk textiltriennal", "1979"), "stofnun")

    def test_verk(self):
        for n in ("Biblían", "Biblían.", "Eddukvæði.", "Eddukvæði", "Njáls saga.",
                  "Bandamanna saga", "Sneglu-Halla þáttur.", "Jónsbók", "Gulaþingslög.",
                  "Krákumál.", "Graduale.", "Íslendinga sögur.", "Fagurskinna",
                  "Íslenskir annálar 803-1430", "Handbók fyrir presta á Íslandi"):
            self.assertEqual(b.flokka(n), "verk", n)

    def test_greinarmerki_fara(self):
        self.assertEqual(b.hreinsa_nafn("Luther, Martin,", "persona"), "Luther, Martin")
        self.assertEqual(b.hreinsa_nafn("Ferrall, J. S.", "persona"), "Ferrall, J. S.")
        self.assertEqual(b.hreinsa_nafn("Scheidius, Christian Ludv.", "persona"),
                         "Scheidius, Christian Ludv.")
        self.assertEqual(b.hreinsa_nafn("Eddukvæði.", "verk"), "Eddukvæði")
        self.assertEqual(b.hreinsa_nafn("Vesturamtið.", "stofnun"), "Vesturamtið")

    def test_aeviar_adeins_ef_baedi_ar(self):
        self.assertEqual(b.nafn_med_arum("Hallgrímur Pétursson", "1614", "1674"),
                         "Hallgrímur Pétursson (1614-1674)")
        self.assertEqual(b.nafn_med_arum("Bera Nordal", "1954", ""), "Bera Nordal")
        self.assertEqual(b.nafn_med_arum("Þórður Bárðarson", "", "1690"), "Þórður Bárðarson")
        self.assertEqual(b.nafn_med_arum("Jón Árnason", "-180", ""), "Jón Árnason")
        self.assertEqual(b.aeviar("1100", "1150"), "(1100-1150)")
        self.assertEqual(b.aeviar("-160", "1608"), "")


class Land(unittest.TestCase):
    def _s(self, geo, loc):
        return ["http://sws.geonames.org/%s" % geo,
                "http://id.loc.gov/vocabulary/countries/%s" % loc]

    def test_samhljoda(self):
        self.assertEqual(b.land(self._s("2629691", "ic")), (["Ísland"], "samhljoda"))
        self.assertEqual(b.land(self._s("2623032", "dk")), (["Danmörk"], "samhljoda"))
        self.assertEqual(b.land(self._s("2921044", "gw")), (["Þýskaland"], "samhljoda"))
        self.assertEqual(b.land(self._s("2661886", "sw")), (["Svíþjóð"], "samhljoda"))
        for loc in ("enk", "stk", "xxk"):
            self.assertEqual(b.land(self._s("2635167", loc)), (["Bretland"], "samhljoda"))

    def test_null_og_xx_eru_othekkt_land(self):
        # GeoNames segir Ísland, en það er sjálfgefið gildi Bækur.is
        self.assertEqual(b.land(self._s("2629691", "null")), ([], "othekkt"))
        self.assertEqual(b.land(self._s("2629691", "xx")), ([], "othekkt"))

    def test_osamraemi_og_utan_toflu(self):
        self.assertEqual(b.land(self._s("2629691", "ge")), ([], "osamraemi"))
        self.assertEqual(b.land(self._s("3578476", "sc")), ([], "osamraemi"))
        self.assertEqual(b.land([]), ([], "vantar"))


class RettindiOgUmfang(unittest.TestCase):
    def test_rettindi(self):
        self.assertEqual(b.rettindi("http://rightsstatements.org/page/InC/1.0/"),
                         ("Höfundarréttur í gildi", "http://rightsstatements.org/vocab/InC/1.0/"))
        self.assertEqual(b.rettindi("https://creativecommons.org/publicdomain/mark/1.0/"),
                         ("Almenningseign", "https://creativecommons.org/publicdomain/mark/1.0/"))
        self.assertEqual(b.rettindi("http://creativecommons.org/publicdomain/mark/1.0"),
                         ("Almenningseign", "https://creativecommons.org/publicdomain/mark/1.0/"))
        self.assertEqual(b.rettindi("https://example.org/leyfi"), (None, "https://example.org/leyfi"))

    def test_umfang_med_rettri_tolu(self):
        self.assertEqual(b.umfang("730 p."), "730 síður í stafrænu eintaki")
        self.assertEqual(b.umfang("4 p."), "4 síður í stafrænu eintaki")
        self.assertEqual(b.umfang("1 p."), "1 síða í stafrænu eintaki")
        self.assertEqual(b.umfang("21 p."), "21 síða í stafrænu eintaki")
        self.assertEqual(b.umfang("1121 p."), "1121 síða í stafrænu eintaki")
        self.assertEqual(b.umfang("11 p."), "11 síður í stafrænu eintaki")
        self.assertEqual(b.umfang("111 p."), "111 síður í stafrænu eintaki")
        self.assertIsNone(b.umfang("[8] bl."))
        self.assertIsNone(b.umfang("0 p."))

    def test_islensk_stafrofsrod(self):
        self.assertEqual(sorted(["Þýðingar á frönsku", "Ævisögur", "Ásatrú", "Atvinnuvegir",
                                 "Íslenskar bókmenntir", "Iðnaður", "Öldrun", "Hólaprent",
                                 "Hagfræði", "Zoologi"], key=b.islensk_rod),
                         ["Atvinnuvegir", "Ásatrú", "Hagfræði", "Hólaprent", "Iðnaður",
                          "Íslenskar bókmenntir", "Zoologi", "Þýðingar á frönsku",
                          "Ævisögur", "Öldrun"])

    def test_isbd_tekid_af_titli(self):
        self.assertEqual(b.hreinsa_titil("Íslenzk list ="), "Íslenzk list")
        self.assertEqual(b.hreinsa_titil("Höggmyndir /"), "Höggmyndir")
        self.assertEqual(b.hreinsa_titil("Ný matreiðslubók ásamt ávísun um litun, þvott o.fl."),
                         "Ný matreiðslubók ásamt ávísun um litun, þvott o.fl.")


class Heild(unittest.TestCase):
    def _smida(self, *records):
        s = b.lesa_svar(_svar(records))
        texti, talning = b.smida(s["faerslur"])
        return texti, talning, ET.fromstring(texti.encode("utf-8"))

    def _dc(self, *records):
        return self._smida(*records)[2].find("record/metadata")[0]

    def test_alma_snid_og_sannprofun(self):
        texti, talning, rot = self._smida(SJO, NORDISK, AUGLYSING, BIBLIA, STULKA)
        self.assertEqual(b.sannprofa(texti, 5), [])
        self.assertFalse(texti.startswith("<?xml"))
        self.assertEqual(rot.tag, "ListRecords")
        self.assertEqual(rot.attrib, {})
        self.assertEqual(rot.findall("record")[0].find("header/identifier").text,
                         "oai:baekur.is:books/0c11ccb5-0929-49db-bb27-cb8f260ef28b")
        self.assertEqual(rot.findall("record")[0].findtext("header/setSpec"), "source:baekur")
        self.assertIn('xmlns:mshl="https://mshl.is/terms#"', texti)
        self.assertEqual(talning["flokkar"]["persona"], 4)
        self.assertEqual(talning["flokkar"]["stofnun"], 1)
        self.assertEqual(talning["flokkar"]["verk"], 1)

    def test_hofundur_leystur_med_aeviarum_og_hlutverki(self):
        dc = self._dc(SJO)
        c = dc.find(DC + "creator")
        self.assertEqual(c.text, "Hallgrímur Pétursson (1614-1674)")
        self.assertEqual(c.get(MSHL + "role"), "höfundur")
        self.assertEqual(dc.findtext(DCT + "bibliographicCitation"),
                         "Hallgrímur Pétursson (1614-1674) (höfundur)")
        self.assertEqual([e.text for e in dc.findall(DC + "identifier")],
                         ["https://baekur.is/bok/0c11ccb5-0929-49db-bb27-cb8f260ef28b",
                          "https://baekur.is/cover/tbn/0c11ccb5-0929-49db-bb27-cb8f260ef28b",
                          "oai:baekur.is:books/0c11ccb5-0929-49db-bb27-cb8f260ef28b"])
        self.assertEqual([(e.get(LANG), e.text) for e in dc.findall(DC + "type")],
                         [("is", "Bók"), ("en", "Text")])
        # efnisorð heimildar í íslenskri stafrófsröð, fasta orðið „Bækur“ aftast
        self.assertEqual([e.text for e in dc.findall(DC + "subject")], ["Bænir", "Sálmar", "Bækur"])
        self.assertEqual(dc.findtext(DC + "date"), "1860")
        self.assertEqual(dc.findtext(DCT + "extent"), "94 síður í stafrænu eintaki")
        self.assertEqual([e.text for e in dc.findall(DCT + "isReferencedBy")],
                         ["Bókaskrá Landsbókasafns",
                          "https://bokaskra.landsbokasafn.is/search?s_any=991005534569706886"])
        for e in dc:
            self.assertTrue((e.text or "").strip(), e.tag)

    def test_tveir_hofundar_og_land(self):
        dc = self._dc(NORDISK)
        self.assertEqual([e.text for e in dc.findall(DC + "creator")],
                         ["Arentzen, Kristian (1823-1899)", "Steingrímur Thorsteinsson (1831-1913)"])
        s = dc.find(DCT + "spatial")
        self.assertEqual((s.text, s.get(XSI + "type"), s.get(MSHL + "role"), s.get(LANG)),
                         ("Danmörk", "mshl:land", "útgáfustaður", "is"))
        self.assertEqual(dc.findtext(DC + "language"), "da")

    def test_island_sem_hofundur_og_ekkert_land(self):
        # land sem „höfundur“ tilskipunar fer EKKI í dc:contributor — það lenti í Fólk-síunni
        # í Leitum (140 „Ísland“). Ákvörðun Einars 7.10.2026.
        dc = self._dc(AUGLYSING)
        self.assertIsNone(dc.find(DC + "creator"))
        self.assertIsNone(dc.find(DC + "contributor"))
        self.assertIsNone(dc.find(DCT + "bibliographicCitation"))
        self.assertIsNone(dc.find(DCT + "spatial"))
        self.assertEqual(dc.findtext(DCT + "extent"), "4 síður í stafrænu eintaki")

    def test_samraemdur_titill_verdur_verk(self):
        dc = self._dc(BIBLIA)
        self.assertIsNone(dc.find(DC + "creator"))
        v = dc.find(DCT + "hasPart")
        self.assertEqual((v.text, v.get(XSI + "type")), ("Biblían", "mshl:verk"))
        self.assertEqual([e.text for e in dc.findall(DC + "subject")], ["Bækur"])
        self.assertEqual(dc.findtext(DCT + "extent"), "1121 síða í stafrænu eintaki")

    def test_rettindi_tvo_reitir(self):
        self.assertEqual([(e.get(LANG), e.text) for e in self._dc(SJO).findall(DC + "rights")],
                         [("is", "Höfundarréttur í gildi"),
                          (None, "http://rightsstatements.org/vocab/InC/1.0/")])
        self.assertEqual([e.text for e in self._dc(STULKA).findall(DC + "rights")],
                         ["Almenningseign", "https://creativecommons.org/publicdomain/mark/1.0/"])

    def test_sannprofun_gripur_villur(self):
        texti, _n, _r = self._smida(SJO)
        self.assertTrue(b.sannprofa('<?xml version="1.0"?>\n' + texti, 1))
        self.assertTrue(b.sannprofa(texti, 2))                      # fjöldi stemmir ekki
        self.assertTrue(b.sannprofa(texti.replace(">1860<", ">um 1860<"), 1))
        self.assertTrue(b.sannprofa(texti.replace(">Bænir<", "><"), 1))  # tómur reitur
        self.assertTrue(b.sannprofa(texti.replace(">Bænir<", ">None<"), 1))
        self.assertTrue(b.sannprofa(texti.replace('mshl:role="höfundur"', ""), 1))

    def test_resumption_token_lesinn(self):
        s = b.lesa_svar(_svar([SJO], token="edm/////25"))
        self.assertEqual(s["token"], "edm/////25")
        self.assertEqual(s["fjoldi"], 2984)
        self.assertEqual(b.lesa_svar(_svar([SJO]))["token"], "")


if __name__ == "__main__":
    unittest.main()

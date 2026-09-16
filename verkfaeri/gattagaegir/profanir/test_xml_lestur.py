import unittest

from ..import xml_lestur as xl


class _Svar:
    def __init__(self, texti):
        self.gogn = texti.encode("utf-8") if isinstance(texti, str) else texti
        self.texti = self.gogn.decode("utf-8", "replace")


DC = ('<oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" '
      'xmlns:dc="http://purl.org/dc/elements/1.1/" '
      'xmlns:dcterms="http://purl.org/dc/terms/" '
      'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
      'xmlns:mshl="https://mshl.is/terms#">%s</oai_dc:dc>')


def _record(inni, aud="oai:x:1", status=""):
    return ('<record><header%s><identifier>%s</identifier>'
            '<datestamp>2026-05-01T10:00:00Z</datestamp>'
            '<setSpec>type:baer</setSpec></header>'
            '<metadata>%s</metadata></record>'
            % (status, aud, DC % inni))


def _lr(*records):
    return _Svar(
        '<?xml version="1.0"?><OAI-PMH '
        'xmlns="http://www.openarchives.org/OAI/2.0/">'
        '<ListRecords>%s</ListRecords></OAI-PMH>' % "".join(records))


class ReiturProf(unittest.TestCase):
    def test_lang_xsitype_eigindir(self):
        sk = xl.lesa(_lr(_record(
            '<dc:title xml:lang="is">Bær</dc:title>'
            '<dc:subject xml:lang="is" xsi:type="mshl:efnisord" '
            'mshl:id="1000005">Draugar</dc:subject>')))
        f = xl.faerslur(sk)[0]
        self.assertEqual(f.audkenni, "oai:x:1")
        titill = f.reitir_heitir("dc:title")[0]
        self.assertEqual(titill.gildi, "Bær")
        self.assertEqual(titill.lang, "is")
        efni = f.reitir_heitir("dc:subject")[0]
        self.assertEqual(efni.xsi_type, "mshl:efnisord")
        self.assertEqual(efni.eigindir.get("mshl:id"), "1000005")

    def test_eydd_faersla(self):
        sk = xl.lesa(_lr(_record("", status=' status="deleted"')))
        f = xl.faerslur(sk)[0]
        self.assertTrue(f.eydd)

    def test_oai_villa(self):
        sk = xl.lesa(_Svar(
            '<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">'
            '<error code="badVerb">nope</error></OAI-PMH>'))
        self.assertEqual(xl.oai_villa(sk)[0], "badVerb")

    def test_html_greining(self):
        # Raunveruleg PHP-villusíða er sjaldan vel formað XML (<br> ólokað).
        sk = xl.lesa(_Svar("<html><body><br><b>Fatal error</b> á línu 88"))
        self.assertTrue(sk.er_html)
        self.assertFalse(sk.gilt)

    def test_bom_og_parse_villa(self):
        gogn = b"\xef\xbb\xbf<OAI-PMH><broken></OAI-PMH>"
        sk = xl.lesa(_Svar(gogn))
        self.assertFalse(sk.gilt)
        self.assertIn("lina", sk.villa)

    def test_bjarga_nefnir_brotna(self):
        heilt = _record('<dc:title>Gott</dc:title>', aud="oai:x:1")
        brotid = ('<record><header><identifier>oai:x:27</identifier></header>'
                  '<metadata><![CDATA[ olokad')
        heilar, brotin = xl.bjarga(heilt + brotid)
        self.assertEqual(len(heilar), 1)
        self.assertIn("oai:x:27", brotin)

    def test_resumption(self):
        sk = xl.lesa(_Svar(
            '<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">'
            '<ListRecords><resumptionToken completeListSize="42" '
            'cursor="0">tok2</resumptionToken></ListRecords></OAI-PMH>'))
        tok, cls, cur = xl.resumption(sk)
        self.assertEqual((tok, cls, cur), ("tok2", 42, 0))


if __name__ == "__main__":
    unittest.main()

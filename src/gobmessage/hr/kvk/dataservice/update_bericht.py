from xml.etree import ElementTree

from zeep import ns


class KvkUpdateBericht:
    """Very basic parser of a KvK UpdateBericht

    Input XML is a SOAP message with WSA and WSSE headers, but these are ignored for now. We simply get the information
    we need from the Body.
    """
    namespaces = {
        'soapenv': ns.SOAP_ENV_11,
        'wsa': ns.WSA,
        'wsse': ns.WSSE,
        'dgl': 'http://www.digilevering.nl/digilevering.xsd',
        'kvkupdate': 'http://schemas.kvk.nl/schemas/hrip/update/2018/01',
        'kvkbericht': 'http://schemas.kvk.nl/schemas/hrip/bericht/2018/01',
    }

    def __init__(self, msg: str):
        self.xmltree = ElementTree.fromstring(msg)

    def get_kvk_nummer(self):
        elm = self.xmltree.find(
            "."
            "/gebeurtenisinhoud"
            "/{%s}UpdateBericht" % self.namespaces['kvkupdate'] + ""
                                                                  "/{%s}heeftBetrekkingOp" % self.namespaces[
                'kvkbericht'] + ""
                                "/{%s}kvkNummer" % self.namespaces['kvkbericht']
        )

        if elm is not None:
            return elm.text

    def get_vestigingsnummer(self):
        elm = self.xmltree.find(
            "."
            "/gebeurtenisinhoud"
            "/{%s}UpdateBericht" % self.namespaces['kvkupdate'] + ""
                                                                  "/{%s}heeftBetrekkingOp" % self.namespaces[
                'kvkbericht'] + ""
                                "/{%s}wordtUitgeoefendIn" % self.namespaces['kvkbericht'] + ""
                                                                                            "/{%s}vestigingsnummer" %
            self.namespaces['kvkbericht'] + ""
        )

        if elm is not None:
            return elm.text

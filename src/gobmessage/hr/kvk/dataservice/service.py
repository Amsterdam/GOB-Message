import requests
from datetime import datetime
from zeep import Client
from zeep.transports import Transport

from gobmessage.config import HR_KEYFILE, HR_CERTFILE, KVK_DATASERVICE_ADDRESS
from gobmessage.hr.kvk.dataservice.binary_signature import KvkDataServiceBinarySignature


class KvkDataService:
    """Encapsulates SOAP requests with the KvK DataService

    Documentation: https://www.kvk.nl/sites/aansluitendataservice/index.html#/
    """

    wsdl = 'http://schemas.kvk.nl/contracts/kvk/dataservice/catalogus/2015/02/KVK-KvKDataservice.wsdl'

    def _get_client(self):
        """Returns the Zeep client, configured for use with the KvK DataService

        :return:
        """
        session = requests.Session()
        session.cert = (HR_CERTFILE, HR_KEYFILE)

        transport = Transport(session=session)

        client = Client(self.wsdl, wsse=KvkDataServiceBinarySignature(HR_KEYFILE, HR_CERTFILE), transport=transport)

        # Replace the address, as the WSDL contains example.com as address.
        client.service._binding_options['address'] = KVK_DATASERVICE_ADDRESS

        return client

    def _generate_reference(self):
        """Generates a references to be used in the request.

        :return:
        """
        dt = datetime.utcnow()
        return f"GOB-{dt.strftime('%Y%m%d%H%M%S%f')}"

    def _make_request(self, action: str, **kwargs):
        """Makes a request to :action: with provided kwargs added to the request data

        :param action:
        :param kwargs:
        :return:
        """
        client = self._get_client()

        request_data = {
            'klantreferentie': self._generate_reference(),
            **kwargs
        }

        # Strict mode is not supported by KvK DataService
        with client.settings(strict=False):
            return getattr(client.service, action)(**request_data)

    def ophalen_inschrijving_by_kvk_nummer(self, kvk_nummer):
        return self._make_request('ophalenInschrijving', kvkNummer=kvk_nummer)

    def ophalen_inschrijving_by_rsin(self, rsin):
        return self._make_request('ophalenInschrijving', rsin=rsin)

    def ophalen_vestiging_by_vestigingsnummer(self, vestigingsnummer):
        return self._make_request('ophalenVestiging', vestigingsnummer=vestigingsnummer)

    def ophalen_vestiging_by_kvk_nummer(self, kvk_nummer):
        return self._make_request('ophalenVestiging', kvkNummer=kvk_nummer)

    def ophalen_vestiging_by_rsin(self, rsin):
        return self._make_request('ophalenVestiging', rsin=rsin)

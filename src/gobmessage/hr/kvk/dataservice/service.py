import re
import requests
from datetime import datetime
from zeep import Client
from zeep.helpers import serialize_object
from zeep.transports import Transport

from gobmessage.config import HR_CERTFILE, HR_KEYFILE, KVK_DATASERVICE_ADDRESS
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

    def _unpack_raw_elements(self, in_dict: dict):
        """Unpacks _raw_elements dicts in Zeep result. _raw_elements is a list of elements that aren't parsed by Zeep
        because the result does not conform to the XSD. We do this manually in this method.

        :param in_dict:
        :return:
        """
        result = {}

        if '_raw_elements' in in_dict:
            # Return all existing elements in dict, updated with the values in _raw_elements.
            return {k: self._unpack_raw_elements(v) if isinstance(v, dict) else v
                    for k, v in in_dict.items() if k != '_raw_elements'
                    } | {re.sub(r'^{.*}', '', elm.tag): elm.text for elm in in_dict['_raw_elements']}

        for k, v in in_dict.items():
            if isinstance(v, dict):
                result[k] = self._unpack_raw_elements(v)
            elif isinstance(v, list):
                result[k] = [self._unpack_raw_elements(item) if isinstance(item, dict) else item for item in v]
            else:
                result[k] = v
        return result

    def _make_request(self, action: str, raw_response=False, **kwargs):
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
        with client.settings(strict=False, raw_response=raw_response):
            if raw_response:
                return getattr(client.service, action)(**request_data).text
            return self._unpack_raw_elements(
                serialize_object(getattr(client.service, action)(**request_data))
            )

    def ophalen_inschrijving_by_kvk_nummer(self, kvk_nummer, raw_response=False):
        return self._make_request('ophalenInschrijving', kvkNummer=kvk_nummer, raw_response=raw_response)

    def ophalen_inschrijving_by_rsin(self, rsin, raw_response=False):
        return self._make_request('ophalenInschrijving', rsin=rsin, raw_response=raw_response)

    def ophalen_vestiging_by_vestigingsnummer(self, vestigingsnummer, raw_response=False):
        return self._make_request('ophalenVestiging', vestigingsnummer=vestigingsnummer, raw_response=raw_response)

    def ophalen_vestiging_by_kvk_nummer(self, kvk_nummer, raw_response=False):
        return self._make_request('ophalenVestiging', kvkNummer=kvk_nummer, raw_response=raw_response)

    def ophalen_vestiging_by_rsin(self, rsin, raw_response=False):
        return self._make_request('ophalenVestiging', rsin=rsin, raw_response=raw_response)

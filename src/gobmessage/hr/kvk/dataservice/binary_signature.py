import xmlsec

from datetime import datetime, timedelta
from zeep import ns
from zeep.wsse import utils
from zeep.wsse.signature import (
    BinarySignature,
    _make_sign_key,
    _sign_envelope_with_key_binary,
    _sign_node,
    detect_soap_env,
    QName
)


class KvkDataServiceBinarySignature(BinarySignature):
    """Extends the Zeep WSSE BinarySignature class.

    - Fixes WSA headers that are added by Zeep
    - Correctly signs the message elements that are not signed by Zeep

    Documentation: https://www.kvk.nl/sites/aansluitendataservice/index.html#/
    """

    def _add_timestamp(self, envelope):
        """Adds WSU Timestamp element to the Security header. WSU Timestamp element is needed for WS-Security

        :param envelope:
        :return:
        """
        security = utils.get_security_header(envelope)

        created = datetime.utcnow()
        expired = created + timedelta(seconds=30000)

        timestamp = utils.WSU('Timestamp')
        timestamp.append(utils.WSU('Created', created.replace(microsecond=0).isoformat()+'Z'))
        timestamp.append(utils.WSU('Expires', expired.replace(microsecond=0).isoformat()+'Z'))

        security.append(timestamp)

    def _fix_wsa_headers(self, envelope):
        """Fixes WS-Addressing headers.

        - Replaces the wsa:To header with the correct value
        - Removes the urn: prefix Zeep adds to the wsa:MessageID. This prefix is explicitly not accepted by KvK
          DataService

        :param envelope:
        :return:
        """
        header = utils.get_or_create_header(envelope)

        # Add correct value for wsa:To header
        node = header.find(f'{{{ns.WSA}}}To')
        node.text = 'http://es.kvk.nl/kvk-dataservicePP/2015/02'

        # Remove 'urn:' prefix in wsa:MessageID header (not accepted by KvK DataService)
        node = header.find(f'{{{ns.WSA}}}MessageID')
        node.text = node.text.replace('urn:', '')

    def _sign_envelope(self, envelope):
        """Signs the SOAP envelope.

        Uses Zeep functionality. Zeep only signs the Timestamp and the Body by default, but we need to sign the
        wsa headers To, MessageID and Action as well.

        :param envelope:
        :return:
        """
        # Copied from parent BinarySignature.apply() so that we use the same signing key for all elements.
        key = _make_sign_key(self.key_data, self.cert_data, self.password)

        # This call only signs the Body and Timestamp, and sets up the Security headers. Copied from parent as well.
        _sign_envelope_with_key_binary(
            envelope, key, self.signature_method, self.digest_method
        )

        # Additionally sign To, MessageID, Action
        ctx = xmlsec.SignatureContext()
        ctx.key = key

        soap_env = detect_soap_env(envelope)
        header = envelope.find(QName(soap_env, "Header"))
        security = header.find(QName(ns.WSSE, "Security"))
        signature = security.find(QName(ns.DS, "Signature"))

        for elm in ('To', 'MessageID', 'Action'):
            _sign_node(ctx, signature, header.find(QName(ns.WSA, elm)), self.digest_method)

        ctx.sign(signature)

    def apply(self, envelope, headers):
        """Method where the magic happens

        :param envelope:
        :param headers:
        :return:
        """
        self._add_timestamp(envelope)
        self._fix_wsa_headers(envelope)
        self._sign_envelope(envelope)

        return envelope, headers

    def verify(self, envelope):
        # Bypass Zeep signature verification
        return envelope

from flask import Response, request
from gobcore.message_broker import publish

from gobmessage.config import KVK_MESSAGE_KEY, MESSAGE_EXCHANGE
from gobmessage.database.model import KvkUpdateMessage
from gobmessage.database.repository import KvkUpdateMessageRepository
from gobmessage.database.session import DatabaseSession
from gobmessage.hr.kvk.dataservice.service import KvkDataService
from gobmessage.hr.kvk.dataservice.update_bericht import KvkUpdateBericht


def kvk_endpoint():
    """Accepts KvK update berichten sent by KvK

    :return:
    """
    request_data = request.data.decode('utf-8')

    kvk_bericht = KvkUpdateBericht(request_data)

    message = KvkUpdateMessage()
    message.message = request_data
    message.kvk_nummer = kvk_bericht.get_kvk_nummer()

    with DatabaseSession() as session:
        message = KvkUpdateMessageRepository(session).save(message)

        publish(MESSAGE_EXCHANGE, KVK_MESSAGE_KEY, {'message_id': message.id})

    return Response('OK. Message received. Thank you, good bye.')


def inschrijving_endpoint(kvknummer):
    """Accepts a kvk number as path parameter and returns the result from the KvkDataService.

    Used internally for testing purposes.

    :return:
    """
    dataservice = KvkDataService()
    inschrijving = dataservice.ophalen_inschrijving_by_kvk_nummer(kvknummer, raw_response=True)

    return Response(inschrijving, content_type='application/xml')


def vestiging_endpoint(vestigingsnummer):
    """Accepts a vestigingsnummer as path parameter and returns the result from the KvkDataService.

    Used internally for testing purposes.

    :return:
    """
    dataservice = KvkDataService()
    vestiging = dataservice.ophalen_vestiging_by_vestigingsnummer(vestigingsnummer, raw_response=True)

    return Response(vestiging, content_type='application/xml')

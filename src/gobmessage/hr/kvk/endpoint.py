from flask import Response, request
from gobcore.message_broker import publish

from gobmessage.config import KVK_MESSAGE_KEY, MESSAGE_EXCHANGE
from gobmessage.database.model import KvkUpdateMessage
from gobmessage.database.repository import KvkUpdateMessages
from gobmessage.database.session import DatabaseSession
from gobmessage.hr.kvk.dataservice.update_bericht import KvkUpdateBericht


def kvk_endpoint():
    request_data = request.data.decode('utf-8')

    kvk_bericht = KvkUpdateBericht(request_data)

    message = KvkUpdateMessage()
    message.message = request_data
    message.kvk_nummer = kvk_bericht.get_kvk_nummer()
    message.vestigingsnummer = kvk_bericht.get_vestigingsnummer()

    with DatabaseSession() as session:
        message = KvkUpdateMessages(session).save(message)

        publish(MESSAGE_EXCHANGE, KVK_MESSAGE_KEY, {'message_id': message.id})

    return Response('OK. Message received. Thank you, good bye.')

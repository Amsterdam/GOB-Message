from gobmessage.database.repository import KvkUpdateMessages
from gobmessage.database.session import DatabaseSession
from gobmessage.hr.kvk_dataservice.service import KvkDataService


def hr_message_handler(msg: dict):
    """Message handler for message queue

    :param msg:
    :return:
    """
    message_id = msg['message_id']
    with DatabaseSession() as session:
        message = KvkUpdateMessages(session).get(message_id)

    service = KvkDataService()

    if message.kvk_nummer:
        inschrijving = service.ophalen_inschrijving_by_kvk_nummer(message.kvk_nummer)
        print("INSCHRIJVING")
        print(inschrijving)
    else:
        print("No new data retrieved because 'KvK nummer' was not found in the received message")

    if message.vestigingsnummer:
        vestiging = service.ophalen_vestiging_by_vestigingsnummer(message.vestigingsnummer)
        print("VESTIGING")
        print(vestiging)
    else:
        print("No new data retrieved because 'Vestiging' was not found in the received message")

import os
from threading import Thread

from gobcore.message_broker.initialise_queues import create_queue_with_binding
from gobcore.message_broker.messagedriven_service import messagedriven_service

from gobmessage.api import get_flask_app
from gobmessage.config import GOB_MESSAGE_PORT, KVK_MESSAGE_KEY, KVK_MESSAGE_QUEUE, MESSAGE_EXCHANGE, \
    UPDATE_OBJECT_COMPLETE_KEY, UPDATE_OBJECT_COMPLETE_QUEUE
from gobmessage.database.connection import connect
from gobmessage.database.repository import UpdateObjectRepository
from gobmessage.database.session import DatabaseSession
from gobmessage.hr.kvk.message import kvk_message_handler


def update_object_complete_handler(msg):
    """Callback for when an import flow started by the GOB-Message service is finished.

    :param msg:
    :return:
    """

    with DatabaseSession() as session:
        repo = UpdateObjectRepository(session)
        update_object = repo.get_active_for_entity_id(
            msg['header']['catalogue'],
            msg['header']['entity'],
            msg['header']['entity_id']
        )
        update_object.status = repo.object_class.STATUS_ENDED
        repo.save(update_object)

    return msg


SERVICEDEFINITION = {
    'kvk_message': {
        'exchange': MESSAGE_EXCHANGE,
        'queue': KVK_MESSAGE_QUEUE,
        'handler': kvk_message_handler
    },
    'update_object_complete': {
        'exchange': MESSAGE_EXCHANGE,
        'queue': UPDATE_OBJECT_COMPLETE_QUEUE,
        'handler': update_object_complete_handler,
    }
}


def run_message_thread():
    try:
        # First create queues with bindings if not exists yet
        create_queue_with_binding(exchange=MESSAGE_EXCHANGE, queue=KVK_MESSAGE_QUEUE, key=KVK_MESSAGE_KEY)
        create_queue_with_binding(exchange=MESSAGE_EXCHANGE, queue=UPDATE_OBJECT_COMPLETE_QUEUE,
                                  key=UPDATE_OBJECT_COMPLETE_KEY)

        messagedriven_service(SERVICEDEFINITION, "Message")
    except:  # noqa: E722 do not use bare 'except'
        pass
    print(f"ERROR: no connection with GOB message broker, application is stopped")
    os._exit(os.EX_UNAVAILABLE)


def get_app():
    # Start messagedriven_service in separate thread
    t = Thread(target=run_message_thread)
    t.start()

    return get_flask_app()


def run():
    """
    Get the Flask app and run it at the port as defined in config

    :return: None
    """
    connect()
    app = get_app()
    app.run(port=GOB_MESSAGE_PORT)

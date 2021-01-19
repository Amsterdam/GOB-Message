import os
from threading import Thread

from gobcore.message_broker.initialise_queues import create_queue_with_binding
from gobcore.message_broker.messagedriven_service import messagedriven_service

from gobmessage.api import get_flask_app
from gobmessage.config import GOB_MESSAGE_PORT, KVK_MESSAGE_KEY, KVK_MESSAGE_QUEUE, MESSAGE_EXCHANGE
from gobmessage.database.connection import connect
from gobmessage.hr.kvk.message import kvk_message_handler

SERVICEDEFINITION = {
    'kvk_message': {
        'exchange': MESSAGE_EXCHANGE,
        'queue': KVK_MESSAGE_QUEUE,
        'handler': kvk_message_handler
    }
}


def run_message_thread():
    try:
        # First create queue and binding if not exists yet
        create_queue_with_binding(exchange=MESSAGE_EXCHANGE, queue=KVK_MESSAGE_QUEUE, key=KVK_MESSAGE_KEY)
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

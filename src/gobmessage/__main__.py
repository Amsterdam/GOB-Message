from threading import Thread

from gobcore.message_broker.initialise_queues import create_queue_with_binding
from gobcore.message_broker.messagedriven_service import messagedriven_service

from gobmessage.api import run as run_api
from gobmessage.config import MESSAGE_EXCHANGE, HR_MESSAGE_QUEUE, HR_MESSAGE_KEY
from gobmessage.hr.message import hr_message_handler


SERVICEDEFINITION = {
    'hr_message': {
        'exchange': MESSAGE_EXCHANGE,
        'queue': HR_MESSAGE_QUEUE,
        'handler': hr_message_handler
    }
}


def run_message_thread():
    # First create queue and binding if not exists yet
    create_queue_with_binding(exchange=MESSAGE_EXCHANGE, queue=HR_MESSAGE_QUEUE, key=HR_MESSAGE_KEY)

    messagedriven_service(SERVICEDEFINITION, "Message")


def init():
    if __name__ == "__main__":
        # Run messagedriven service in separate thread
        t = Thread(target=run_message_thread)
        t.start()

        # Run API
        run_api()


init()

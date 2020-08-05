from flask import request, Response
from gobcore.message_broker import publish
from gobmessage.config import MESSAGE_EXCHANGE, HR_MESSAGE_KEY


def hr_endpoint():
    request_data = request.data.decode('utf-8')

    publish(MESSAGE_EXCHANGE, HR_MESSAGE_KEY, {'contents': request_data})

    return Response('OK. Message received. Thank you, good bye.')

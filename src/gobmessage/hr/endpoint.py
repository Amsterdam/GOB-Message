from flask import request, Response


def hr_endpoint():
    request_data = request.data.decode('utf-8')

    # Return request data for now
    return Response('OK: ' + request_data)

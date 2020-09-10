from flask import Flask
from flask_cors import CORS

from gobmessage.config import API_BASE_PATH
from gobmessage.hr.endpoint import hr_endpoint


def _health():
    """

    :return: Message telling the StUF API is OK
    """
    return 'Connectivity OK'


def get_flask_app():
    """
    Initializes the Flask App that serves the SOAP endpoint(s)

    :return: Flask App
    """

    ROUTES = [
        # Health check URL
        ('/status/health/', _health, ['GET']),

        (f'{API_BASE_PATH}/hr', hr_endpoint, ['POST']),
    ]

    app = Flask(__name__)
    CORS(app)

    for route, view_func, methods in ROUTES:
        app.route(rule=route, methods=methods)(view_func)

    return app

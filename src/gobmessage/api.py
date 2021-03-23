from flask import Flask, request
from flask_cors import CORS

from gobcore.secure.request import is_secured_request, extract_roles
from gobcore.secure.config import GOB_HR_ADMIN
from gobmessage.config import API_BASE_PATH
from gobmessage.hr.kvk.endpoint import kvk_endpoint, inschrijving_endpoint, vestiging_endpoint


def _health():
    """

    :return: Message telling the StUF API is OK
    """
    return 'Connectivity OK'


def _secure_route(view_func):
    def wrapper(*args, **kwargs):
        if is_secured_request(request.headers):
            roles = extract_roles(request.headers)

            if GOB_HR_ADMIN in roles:
                return view_func(*args, **kwargs)

        return "Forbidden", 403
    wrapper.__name__ = f"secure_{view_func.__name__}"
    return wrapper


def get_flask_app():
    """
    Initializes the Flask App that serves the SOAP endpoint(s)

    :return: Flask App
    """
    PUBLIC = "public"
    SECURED = "secured"

    ROUTES = [
        # Health check URL
        (PUBLIC, '/status/health/', _health, ['GET']),
        (PUBLIC, f'{API_BASE_PATH}/hr', kvk_endpoint, ['POST']),
        (SECURED, f'{API_BASE_PATH}/inschrijving/<kvknummer>', inschrijving_endpoint, ['GET']),
        (SECURED, f'{API_BASE_PATH}/vestiging/<vestigingsnummer>', vestiging_endpoint, ['GET']),
    ]

    app = Flask(__name__)
    CORS(app)

    for sec_type, route, view_func, methods in ROUTES:
        if sec_type == PUBLIC:
            func = view_func
        elif sec_type == SECURED:
            func = _secure_route(view_func)
        else:  # pragma: no cover
            raise NotImplementedError(f"Unknown sec type: {sec_type}")

        app.route(rule=route, methods=methods)(func)
    return app

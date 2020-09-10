import os


def _getenv(varname, default_value=None, is_optional=False):
    """
    Returns the value of the environment variable "varname"
    or the default value if the environment variable is not set

    :param varname: name of the environment variable
    :param default_value: value to return if variable is not set
    :raises AssertionError: if variable not set or value is empty
    :return: the value of the given variable
    """
    value = os.getenv(varname, default_value)
    assert is_optional or value, f"Environment variable '{varname}' not set or empty"
    return value


GOB_MESSAGE_PORT = os.getenv('GOB_MESSAGE_PORT', default=8167)
API_BASE_PATH = os.getenv("BASE_PATH", default="")

MESSAGE_EXCHANGE = "gob.message"
HR_MESSAGE_QUEUE = f"{MESSAGE_EXCHANGE}.hr"
HR_MESSAGE_KEY = f"message.mutation.hr"

# Optional parameters
HR_KEYFILE = _getenv("HR_KEYFILE", is_optional=True)
HR_CERTFILE = _getenv("HR_CERTFILE", is_optional=True)
KVK_DATASERVICE_ADDRESS = _getenv("KVK_DATASERVICE_ADDRESS", is_optional=True)

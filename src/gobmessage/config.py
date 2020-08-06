import os

GOB_MESSAGE_PORT = os.getenv('GOB_MESSAGE_PORT', default=8167)
API_BASE_PATH = os.getenv("BASE_PATH", default="")

MESSAGE_EXCHANGE = "gob.message"
HR_MESSAGE_QUEUE = f"{MESSAGE_EXCHANGE}.hr"
HR_MESSAGE_KEY = f"message.mutation.hr"

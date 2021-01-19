from gobmessage.database.model import KvkUpdateMessage


class KvkUpdateMessages:

    def __init__(self, session):
        self.session = session

    def get(self, id: int):
        return self.session.query(KvkUpdateMessage).get(id)

    def save(self, message: KvkUpdateMessage):
        self.session.add(message)
        self.session.flush()
        return message

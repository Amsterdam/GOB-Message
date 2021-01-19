from sqlalchemy import BigInteger, Boolean, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class KvkUpdateMessage(Base):
    __tablename__ = "kvk_update_message"
    id = Column(Integer, doc='Database-generated id', primary_key=True, index=True)
    kvk_nummer = Column(BigInteger, doc='KvK nummer referenced in this message')
    vestigingsnummer = Column(BigInteger, doc='Vestigingsnummer referenced in this message')
    message = Column(Text, doc='The message as received')
    is_processed = Column(Boolean, doc='Whether this message is processed or not', default=False)

    def __repr__(self):
        return f'<KvkUpdateMessage {self.id}>'

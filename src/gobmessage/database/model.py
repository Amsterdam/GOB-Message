from sqlalchemy import BigInteger, Boolean, Column, Integer, Text, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class KvkUpdateMessage(Base):
    __tablename__ = "kvk_update_message"
    id = Column(Integer, doc='Database-generated id', primary_key=True, index=True)
    kvk_nummer = Column(BigInteger, doc='KvK nummer referenced in this message')
    vestigingsnummer = Column(BigInteger, doc='Vestigingsnummer referenced in this message')
    message = Column(Text, doc='The message as received')
    is_processed = Column(Boolean, doc='Whether this message is processed or not', default=False)
    received_at = Column(DateTime, doc='Time of receiving', default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<KvkUpdateMessage {self.id}>'


class UpdateObject(Base):
    STATUS_STARTED = 'started'
    STATUS_ENDED = 'ended'

    __tablename__ = "update_object"
    id = Column(Integer, doc='Database-generated id', primary_key=True, index=True)
    created_at = Column(DateTime, doc='Time of creation', default=datetime.datetime.utcnow)
    catalogue = Column(String, doc='The catalogue of the object')
    collection = Column(String, doc='The collection of the object')
    entity_id = Column(String, doc='The entity id of the object to update')
    status = Column(String, doc='The status of this update (started, ended, ...)', default=STATUS_STARTED)

    def __repr__(self):
        return f'<UpdateObject {self.catalogue} {self.collection} {self.entity_id}>'

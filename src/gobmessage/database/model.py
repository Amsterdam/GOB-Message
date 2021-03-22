from sqlalchemy import BigInteger, Boolean, Column, Integer, Text, DateTime, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from typing import Optional

Base = declarative_base()


class KvkUpdateMessage(Base):
    __tablename__ = "kvk_update_message"
    id = Column(Integer, doc='Database-generated id', primary_key=True, index=True)
    kvk_nummer = Column(BigInteger, doc='KvK nummer referenced in this message')
    message = Column(Text, doc='The message as received')
    is_processed = Column(Boolean, doc='Whether this message is processed or not', default=False)
    received_at = Column(DateTime, doc='Time of receiving', default=datetime.datetime.utcnow)

    update_objects = relationship("UpdateObject", back_populates='update_message')

    def __repr__(self):
        return f'<KvkUpdateMessage {self.id}>'

    def get_next_queued_update_object(self) -> Optional['UpdateObject']:
        for update_object in self.update_objects:
            if update_object.status == UpdateObject.STATUS_QUEUED:
                return update_object


class UpdateObject(Base):
    STATUS_QUEUED = 'queued'
    STATUS_STARTED = 'started'
    STATUS_ENDED = 'ended'

    __tablename__ = "update_object"
    id = Column(Integer, doc='Database-generated id', primary_key=True, index=True)
    created_at = Column(DateTime, doc='Time of creation', default=datetime.datetime.utcnow)
    catalogue = Column(String, doc='The catalogue of the object')
    collection = Column(String, doc='The collection of the object')
    source = Column(String, doc='The source of the object')
    application = Column(String, doc='The application of the object')
    entity_id = Column(String, doc='The entity id of the object to update')
    status = Column(String, doc='The status of this update (started, ended, ...)', default=STATUS_QUEUED)
    mapped_entity = Column(JSON, doc='The processed object, mapped to the GOB model')
    update_message_id = Column(ForeignKey(KvkUpdateMessage.id))
    update_message = relationship("KvkUpdateMessage", back_populates='update_objects')

    def __repr__(self):
        return f'<UpdateObject {self.catalogue} {self.collection} {self.entity_id}>'

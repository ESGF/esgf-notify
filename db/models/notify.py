
from sqlalchemy import Column, Integer, Sequence, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship, backref

from db.schema import NOTIFY_SCHEMA, SECURITY_SCHEMA
from db.models.base import Base


class ESGFSubscribers(Base):
    """ Class that represents the 'esgf_subscription.subscribers' table in the ESGF database."""

    __tablename__ = 'subscribers'
    __table_args__ = { 'schema': 'esgf_subscription'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('esgf_security.user.id'))
    period = Column(Integer)  # ForeignKey (Q: do we want to define this?)

    terms = relationship("ESGFTerms", back_populates="subscriber", passive_deletes=True, cascade='all, delete, delete-orphan')    

    users = relationship("ESGFUser", back_populates='subscription')

class ESGFTerms(Base):
    """ Class that represents the 'esgf_subscription.keys' table in the ESGF database."""

    __tablename__ = 'terms'
    __table_args__ = { 'schema': 'esgf_subscription'}
  
    id = Column(Integer, primary_key=True)
    subscribers_id = Column(Integer, ForeignKey('esgf_subscription.subscribers.id', ondelete="CASCADE")) # FK
    keyname = Column(String)
    valuename = Column(String)

    subscriber = relationship("ESGFSubscribers", back_populates='terms') 


from sqlalchemy import Column, Integer, Sequence, String, Date, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, backref

from db.schema import NOTIFY_SCHEMA, SECURITY_SCHEMA
from db.models.base import Base

class ESGFUser(Base):

    # Real Table definitions
    __tablename__ = 'user'
    __table_args__ = {'schema': SECURITY_SCHEMA}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    firstname = Column(
        String(100),
        nullable=False
    )
    lastname = Column(
        String(100),
        nullable=False
    )
    email = Column(
        String(100),
        nullable=False
    )
    username = Column(
        String(100),
        unique=True,
        nullable=False
    )
    password = Column(
        String(100)
    )
    db = Column(
        String(300)
    )
    openid = Column(
        String(200),
        index=True,
        nullable=False
    )
    organization = Column(
        String(200)
    )
    city = Column(
        String(100)
    )
    state = Column(
        String(100)
    )
    country = Column(
        String(100)
    )

    # For the sqlAlchemy's sake, does not effect table creation
    subscription = relationship(
        "ESGFSubscribers",
        back_populates='users'
    )

class Group(Base):
    __tablename__ = 'group'
    __table_args__ = {'schema': SECURITY_SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    visible = Column(Boolean, default=True)
    automatic_approval = Column(Boolean, default=False)

class Role(Base):
    __tablename__ = 'role'
    __table_args__ = {'schema': SECURITY_SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)


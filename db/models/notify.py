
from sqlalchemy import Column, Integer, Sequence, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship, backref

from db.schema import NOTIFY_SCHEMA, SECURITY_SCHEMA
from db.models.base import Base

class Subscription(Base):

    # Real Table definitions
    __tablename__ = 'subscription'
    __table_args__ = {'schema': NOTIFY_SCHEMA}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id = Column(
        Integer,
        ForeignKey(
            '%s.user.id' % SECURITY_SCHEMA,
            ondelete='CASCADE'
        )
    )

    # For the sqlAlchemy's sake, does not effect table creation
    user = relationship(
        "User",
        backref=backref("%s.subscription" % NOTIFY_SCHEMA, passive_deletes=True)
    )
    constraint = relationship(
        "Constraint",
        backref="%s.constraint" % NOTIFY_SCHEMA
    )

class Constraint(Base):

    # Real Table definitions
    __tablename__ = 'constraint'
    __table_args__ = {'schema': NOTIFY_SCHEMA}

    # id = Column(Integer,  autoincrement=True)
    sub_id = Column(
        Integer,
        ForeignKey(
            '%s.subscription.id' % NOTIFY_SCHEMA,
            ondelete='CASCADE'
        ),
        primary_key=True
    )
    field = Column(
        String(200),
        nullable=False,
        primary_key=True
    )
    value = Column(
        String(200),
        nullable=False,
        primary_key=True
    )

    # For the sqlAlchemy's sake, does not effect table creation
    subscription = relationship(
        "Subscription",
        backref=backref(
            "%s.constraint" % NOTIFY_SCHEMA,
            passive_deletes=True
        )
    )
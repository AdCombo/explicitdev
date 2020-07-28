from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
)

from .base import Base
from ...utils.auto_name_attrs import AutoNamedModelAttrs


class UserType:
    backend = 'backend'
    frontend = 'frontend'
    admin = 'admin'


class User(Base):
    id = Column(Integer, primary_key=True)
    name = Column(
        String,
        comment='Name of a user.',
        unique=True,
    )
    type = Column(
        String,
        comment='User types. Look at enum.',
        index=True,
    )
    jira_name = Column(
        String,
        comment='Name of a user in Jira',
        unique=True,
    )
    birth_date = Column(
        Date,
        comment='Birth date of a user.',
        index=True,
    )
    working_start_date = Column(
        Date,
        comment='Date when user begin to work in the company.',
        index=True,
    )
    working_end_date = Column(
        Date,
        comment='Date when user stop to work in the company.',
        index=True,
    )


class UserAttrs(User, metaclass=AutoNamedModelAttrs):
    pass

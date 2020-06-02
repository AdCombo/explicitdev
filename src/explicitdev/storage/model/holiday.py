from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
)

from .base import Base
from ...utils.auto_name_attrs import AutoNamedModelAttrs


class HolidayType:
    government = 'government'
    corporate = 'corporate'


class Holiday(Base):
    id = Column(Integer, primary_key=True)
    type = Column(
        String,
        comment='User types. Look at enum.',
        index=True,
    )
    date = Column(
        Date,
        comment='Date of a day',
        unique=True,
    )


class HolidayAttrs(Holiday, metaclass=AutoNamedModelAttrs):
    pass

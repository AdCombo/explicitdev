from sqlalchemy import (
    Column,
    String,
    Integer,
    TIMESTAMP, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base
from ...utils.auto_name_attrs import AutoNamedModelAttrs


class Status(Base):
    id = Column(Integer, primary_key=True)
    jira_id = Column(Integer, unique=True)
    issue_key = Column(
        String,
        comment='Issue key from a linked jira issue.',
        index=True,
        nullable=False,
    )
    author = Column(String, index=True)
    status = Column(String, index=True, nullable=False)
    start_ts = Column(TIMESTAMP(timezone=True), index=True, nullable=False)
    # todo make constraint to forbid it be lesser than start_ts
    end_ts = Column(TIMESTAMP(timezone=True), index=True)

    __table_args__ = (
        UniqueConstraint(issue_key, start_ts, status),
    )


class StatusAttrs(Status, metaclass=AutoNamedModelAttrs):
    pass

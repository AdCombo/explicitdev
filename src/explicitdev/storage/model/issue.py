from sqlalchemy import (
    Column,
    String,
    TIMESTAMP,
)
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base
from ...utils.auto_name_attrs import AutoNamedModelAttrs


class Issue(Base):
    key = Column(
        String,
        comment='Issue key from jira',
        primary_key=True,
    )
    # todo create separate table for this
    assignee = Column(String)
    creator = Column(String)
    reporter = Column(String)
    priority = Column(
        String,
        comment='Current priority of an Issue.'
    )
    project = Column(
        String,
        comment='Jira project linked with an issue.',
    )
    updated = Column(TIMESTAMP(timezone=True), index=True)
    created = Column(TIMESTAMP(timezone=True), index=True)
    resolutiondate = Column(TIMESTAMP(timezone=True), index=True)
    status = Column(
        String,
        comment='Current status of the issue.',
    )
    resolution = Column(String)
    link = Column(
        String,
        comment='Link back for issue.',
    )
    type = Column(
        String,
        comment='Type of an issue.',
    )
    description = Column(
        String,
        comment='Long text description of a task.',
    )
    summary = Column(
        String,
        comment='Aka short name of task.',
    )
    # todo make labels on separate table
    # labels = Column(String, comment='Issue key from jira')

    raw_json = Column(
        JSONB,
        nullable=False,
        default={},
        server_default='{}',
        comment='Fresh raw json from Jira API',
    )


class IssueAttrs(Issue, metaclass=AutoNamedModelAttrs):
    pass

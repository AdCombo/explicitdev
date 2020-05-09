from pathlib import Path

import pytz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from explicitdev.analyse.jira import JiraAnalyzer
from explicitdev.storage.factory import (
    FactoryIssue,
    FactoryStatus,
    FactoryHistory,
)
from explicitdev.storage.model.issue import Issue as AlchemyIssue
from explicitdev.storage.model.status import Status as AlchemyStatus
from explicitdev.storage.session import session_scope


class Config:
    class Jira:
        API_URL: str = ''
        LOGIN: str = ''
        PASS: str = ''
        JQL_PROJECTS: str = ''

    class DumpFiles:
        FILENAME: str = "issue_dumps.json"
        PATH: str = ''

    class Models:
        class Issue:
            Class = AlchemyIssue
            Factory = FactoryIssue

        class Status:
            Class = AlchemyStatus
            Factory = FactoryStatus

        FactoryHistory = FactoryHistory
        models_with_containers = (Issue.Class, Status.Class)

    JiraAnalyzer = JiraAnalyzer

    class Reports:
        dir: Path = None

    DB_CONN_STRING: str = 'postgresql://test:test@127.0.0.1:5433/test'
    engine = create_engine(DB_CONN_STRING)
    CHUNK_DB_SIZE: int = 1000
    session = None
    TIMEZONE = pytz.timezone('Etc/GMT+0')
    """Timezone for a Jira instance."""

    @classmethod
    def session_context(cls):
        if not cls.session:
            engine = create_engine(cls.DB_CONN_STRING)
            session = sessionmaker(bind=engine)
        # noinspection PyUnboundLocalVariable
        return session_scope(session)

from pathlib import Path
from typing import (
    TYPE_CHECKING,
)

import gspread
import pytz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from explicitdev.analyse.jira import JiraAnalyzer
from explicitdev.storage.factory import (
    FactoryIssue,
    FactoryStatus,
    FactoryHistory,
    FactoryUser,
    FactoryHoliday,
)
from explicitdev.storage.model import (
    Issue as AlchemyIssue,
    User as AlchemyUser,
    Status as AlchemyStatus,
    Holiday as AlchemyHoliday,
)
from explicitdev.storage.session import session_scope
from explicitdev.utils.const import ReportSaveModes

if TYPE_CHECKING:
    from explicitdev.storage.model.base import ModelContainerTypeTuple


class Config:
    class Jira:
        API_URL: str = ''
        LOGIN: str = ''
        PASS: str = ''
        JQL_PROJECTS: str = ''

    class DataFiles:
        PATH: Path = None
        """Folder to store different data files as source and target for dump"""
        ISSUE_DUMPS: str = "issue_dumps.json"
        HOLIDAYS: str = "holidays.csv"

    class Models:
        class Issue:
            Class = AlchemyIssue
            Factory = FactoryIssue

        class Status:
            Class = AlchemyStatus
            Factory = FactoryStatus

        class User:
            Class = AlchemyUser
            Factory = FactoryUser

        class Holiday:
            Class = AlchemyHoliday
            Factory = FactoryHoliday

        FactoryHistory = FactoryHistory
        models_with_containers: 'ModelContainerTypeTuple' = (Issue.Class, Status.Class)

    JiraAnalyzer = JiraAnalyzer

    class Reports:
        dir: Path = None
        """Path to folder with reports"""
        gspread_client: gspread.Client = None
        """Client for working with gspread reports"""

        class AbstractReport:
            description: str = ''
            """What this report supposed to do."""
            csv_name: str = ''
            """Name for csv file"""
            save_mode: str = ReportSaveModes.csv
            gspread_key: str = ''
            """Google spreadsheet key for identify linked spreadsheet"""
            gspread_worksheet_name: str = 'data'
            """Name of a worksheet to save data"""

        class StatusesDuration(AbstractReport):
            description = 'Calculate statuses duration with production calendar.'

        class UserBeginPerformance(AbstractReport):
            description = 'Report for measure developers productivity from beginning of the work'

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

import logging
from datetime import datetime
from typing import List

from sqlalchemy import func

from explicitdev.config import Config
from explicitdev.fetch.jira import FetchJiraData
from explicitdev.storage.factory.abstract import ModelBulkInsertUpdate, DataDict
from explicitdev.storage.model.issue import IssueAttrs
from explicitdev.storage.session import Session
from explicitdev.storage.update.abstract import AbstractUpdate


class UpdateJira(AbstractUpdate):
    """It works only when Issue attribute same as key from dict"""

    def __init__(self, c):
        super().__init__(c)
        self.factory_issue = c.Models.Issue.Factory(c)
        self.factory_history = c.Models.FactoryHistory(c)
        self.Issue = c.Models.Issue.Class
        self.models_with_containers = self.c.Models.models_with_containers

    def _max_updated_issue(self, session: Session) -> int:
        result = session.query(
            func.coalesce(func.max(self.Issue.updated), datetime.min),
        ).scalar()
        # in ms its Jira demand.
        result = int(result.timestamp()) * 1000
        return result

    def _create_data_containers_dict(self):
        """Create containers for transport data between code."""
        data = dict()
        for model in self.models_with_containers:
            data[model.__name__] = ModelBulkInsertUpdate(model=model)
        return data

    def add_new_issues(self, issues: List[dict]):
        """Add new issues into DB. If already existed, update it."""
        data = self._create_data_containers_dict()

        issues_count = len(issues)
        logging.info('Going to add %s issues into DB.', issues_count)
        with self.c.session_context() as session:
            self.factory_issue.get_existed_entities(session)
            self.factory_history.get_existed_entities(session)
            for n, raw_issue in enumerate(issues, start=1):
                issue = self.factory_issue.fill_dict_from_raw_dict(raw_issue, data)
                issue_key = issue[IssueAttrs.key]
                self.factory_history.fill_dict_from_raw_dict(
                    raw_issue,
                    data,
                    issue_key=issue_key,
                    issue_created=issue[IssueAttrs.created],
                    issue_status=issue[IssueAttrs.status],
                )
                if not n % Config.CHUNK_DB_SIZE or n == issues_count:
                    self._bulk_update_insert_mappings(session, data)
                    logging.info('%s issues of %s completed.', n, issues_count)
            logging.info('Going to commit into DB %s issues.', issues_count)
            session.commit()

    def sync(self):
        # todo create option for optional dump data
        with self.c.session_context() as session:
            last_updated_issue = self._max_updated_issue(session)
            logging.info('Last updated issue has timestamp %s', last_updated_issue)
        fetcher = FetchJiraData(self.c)
        data = fetcher.fetch_data(last_updated_issue)
        self.add_new_issues(data)


__all__ = [
    UpdateJira.__name__,
]

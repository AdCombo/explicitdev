import pytest

from explicitdev.config import Config
from explicitdev.storage.model.issue import Issue
from explicitdev.storage.update import UpdateJira
# noinspection PyUnresolvedReferences
from tests.sample import (
    get_sample,
    Registry,
    raw_jira_list_result,
    raw_jira_json,
)
from tests.utils.mock import patch_imported, NonCallableMock, MagicMock


class TestUpdateJira:
    @pytest.fixture(scope='session')
    def updater(self):
        return UpdateJira(Config)

    class Test_add_new_issues:
        def test(self, updater: UpdateJira, raw_jira_list_result):
            updater.add_new_issues(raw_jira_list_result)


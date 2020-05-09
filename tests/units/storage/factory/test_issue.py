from unittest.mock import NonCallableMock

from explicitdev.config import Config
from explicitdev.storage.factory import FactoryIssue
from explicitdev.storage.update import UpdateJira
# noinspection PyUnresolvedReferences
from tests.sample import (
    get_sample,
    Registry,
    raw_jira_list_result,
    raw_jira_json,
)
from tests.utils.mock import patch_imported


class TestFactoryIssue:

    @patch_imported(
        FactoryIssue.__name__ + '.' + FactoryIssue.solve_update_or_insert.__name__,
        FactoryIssue,
    )
    def test_fill_from_raw_dict(self, mock_solve: NonCallableMock, raw_jira_list_result):
        data = raw_jira_list_result[0]
        factory = FactoryIssue(Config)
        updater = UpdateJira(Config)
        data_containers = updater._create_data_containers_dict()
        result = factory.fill_dict_from_raw_dict(data, data_containers)

        # todo it's possible for more checks here. Maybe check, that all fields filled? Get it from model.
        assert isinstance(result, dict)
        mock_solve.assert_called_once()

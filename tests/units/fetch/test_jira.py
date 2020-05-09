from unittest.mock import NonCallableMock

from jira import JIRA

from explicitdev.config import Config
from explicitdev.fetch.jira import FetchJiraData
# noinspection PyUnresolvedReferences
from tests.sample import (
    get_sample,
    Registry,
    raw_jira_json,
)
from tests.utils.mock import patch_imported


class TestFetchJiraData:
    # noinspection PyPep8Naming
    class Test_fetch_data:

        @patch_imported(JIRA.__name__, FetchJiraData)
        def test_success(self, mock_jira: JIRA):
            fetcher = FetchJiraData(Config)
            mock_jira().search_issues.return_value = get_sample(Registry.RAW_JIRA, json_load=True)
            result = fetcher.fetch_data()
            assert len(result) == 3

    # noinspection PyPep8Naming
    class Test_dump_data:
        @patch_imported('Path.open', FetchJiraData)
        @patch_imported('json.dump', FetchJiraData)
        def test(self, mock_dump: NonCallableMock, mock_open: NonCallableMock):
            data = [
                {1: 1},
                {2: 2},
            ]
            FetchJiraData(Config).dump_data(data)

            mock_open.assert_called_once()
            mock_dump.assert_called_once()

    @patch_imported('Path.open', FetchJiraData)
    @patch_imported('json.load', FetchJiraData)
    def test_load_data(self, mock_load: NonCallableMock, mock_open: NonCallableMock):
        mock_load.return_value = {1: 1}
        result = FetchJiraData(Config).load_data()

        assert result

        mock_open.assert_called_once()
        mock_load.assert_called_once()

    def test_extend_result_list(self, raw_jira_json):
        result_list = list()
        FetchJiraData.extend_result_list(result_list, raw_jira_json)

        assert len(result_list) == len(raw_jira_json['issues'])

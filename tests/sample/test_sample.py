import json

from .sample import (
    Registry,
    get_sample,
)


class Test_get_sample_data:
    def test_loag_raw_jira_str(self):
        result = get_sample(Registry.RAW_JIRA)
        result = json.loads(result)

        assert isinstance(result, dict)


    def test_json_sample(self):
        result = get_sample(Registry.RAW_JIRA, json_load=True)

        assert isinstance(result, dict)

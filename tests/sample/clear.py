import json
import re

from explicitdev.utils.json import pretty_dump
from tests.sample import get_sample, Registry
from tests.sample.config_clear import ConfigClear
from tests.sample.sample import data_path

CUSTOM_FIELD_PREFIX = 'customfield_'


def clear_raw_jira(delete_custom_field=True):
    file_str = get_sample(Registry.RAW_JIRA)
    for regex, replace_pattern in ConfigClear.REPLACE_PAIRS.items():
        file_str = re.sub(regex, replace_pattern, file_str, flags=re.IGNORECASE)
    file_str_dict = json.loads(file_str)
    for issue in file_str_dict['issues']:
        field_dict: dict = issue['fields']
        iter_issue_field = field_dict.copy()
        for field_key in iter_issue_field:
            if field_key.startswith(CUSTOM_FIELD_PREFIX):
                del field_dict[field_key]

    pretty_dump(data_path.joinpath(Registry.RAW_JIRA), file_str_dict)


if __name__ == '__main__':
    clear_raw_jira()

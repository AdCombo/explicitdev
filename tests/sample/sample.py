import inspect
import json
from pathlib import Path

import pytest

from explicitdev.fetch.jira import FetchJiraData
from . import data


class Registry:
    RAW_JIRA = 'raw_jira.json'  # raw answer from Jira v8.2.3


# get data path for data folder
data_path = Path(inspect.getfile(data)).parent


def get_sample(name: str, data_path: Path() = data_path, json_load=False) -> str:
    path = data_path.joinpath(name)
    with open(path, newline='\n') as file:
        if json_load:
            return json.load(file)
        return file.read()


@pytest.fixture(scope='session')
def raw_jira_json():
    return get_sample(Registry.RAW_JIRA, json_load=True)


@pytest.fixture(scope='session')
def raw_jira_list_result(raw_jira_json):
    list_ = list()
    FetchJiraData.extend_result_list(list_, raw_jira_json)
    return list_

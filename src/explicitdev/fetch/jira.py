import json
import logging
import time
from typing import Type

import attr
from jira import JIRA

from explicitdev.config import Config


@attr.s(auto_attribs=True)
class JiraSearchParams:
    jql_str: str = ''
    """Actually JQL request"""
    maxResults: int = 50
    json_result: bool = True
    """Set it to true. For getting dict. It fobidden from usinc acync mode in client. Work issues another way or 
    forget """
    expand: str = 'changelog'
    """Expand with changelog for getting all changes"""
    startAt: int = 0
    fields: str = '*all'
    """To get all fields from issues with comments and worklog"""


@attr.s(auto_attribs=True)
class JQLRequestParams:
    jql_projects: str = ''
    start_ts: int = 0
    end_ts: int = 0


class FetchJiraData:
    """
    Class for update
    """

    JQL_REQUEST: str = \
        'project IN ({jql_projects}) AND ' \
        'updated > {start_ts} AND ' \
        'updated < {end_ts} ' \
        'ORDER BY updated ASC'  # Sort by ASC, if task updated during fetching, new tasks will be in the end

    """Template for JQL requst for getting issues from Jira"""

    def __init__(self, c: Type[Config]):
        self._dump_path = c.DataFiles.PATH.joinpath(c.DataFiles.ISSUE_DUMPS)
        """Path for file where to put dump from issues and get data from. Useful for development."""
        self.c: Config = c

    @classmethod
    def extend_result_list(cls, result_list: list, result_dict: dict):
        result_list.extend(result_dict['issues'])

    def fetch_data(self, start_ts: int = 0) -> list:
        """
        Fetching data from jira begin with passed timestamp and ended just now.
        :param start_ts: should be in ms, because of Jira demands
        :return:
        """
        jira = JIRA(self.c.Jira.API_URL, basic_auth=(self.c.Jira.LOGIN, self.c.Jira.PASS))
        raw_jira_issues = list()

        jql_params = JQLRequestParams()
        jql_params.jql_projects = self.c.Jira.JQL_PROJECTS
        jql_params.start_ts = start_ts
        jql_params.end_ts = int(round(time.time() * 1000))  # timestamp should be in ms

        jql = self.JQL_REQUEST.format(**attr.asdict(jql_params))
        params = JiraSearchParams(jql_str=jql)
        while True:
            response = jira.search_issues(**attr.asdict(params))
            total = response['total']
            if not total:
                logging.info('No issues have been found.')
                return []
            self.extend_result_list(raw_jira_issues, response)
            logging.info('Getting %s of %s new issues has been completed', params.startAt, total)
            params.startAt += params.maxResults
            if total <= params.startAt + 1:
                break
        return raw_jira_issues

    def dump_data(self, data: list) -> None:
        """Dump data to a local storage"""
        logging.info('Starting to dump %s Jira issues onto disk.', len(data))
        logging.info('Going to dump data from jira to file %s', self._dump_path)
        with self._dump_path.open(mode='w') as file:
            json.dump(data, file, indent=4)
        logging.info('Dump has been successfully completed.')

    def load_data(self) -> list:
        """Load data from """
        logging.info('Going to load load from file %s', self._dump_path)
        with self._dump_path.open() as file:
            result = json.load(file)
            logging.info('Dump has been successfully loaded.')
            return result

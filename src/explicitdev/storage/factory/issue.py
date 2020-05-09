from functools import partial

from sqlalchemy import func
from sqlalchemy.orm import Session

from explicitdev.storage.factory.abstract import FactoryAbstract
from explicitdev.storage.model.issue import (
    IssueAttrs,
)
from explicitdev.utils.nested_dict import get_name_or_empty

IA = IssueAttrs


class FactoryIssue(FactoryAbstract):
    ISSUE_FIELDS_NESTED_DICT_KEYS = (
        IssueAttrs.assignee,
        IssueAttrs.creator,
        IssueAttrs.priority,
        IssueAttrs.project,
        IssueAttrs.reporter,
        IssueAttrs.resolution,
        IssueAttrs.status,
    )
    """It works only when Issue attribute same as key from dict"""

    def __init__(self, c):
        super().__init__(c)
        self.Issue = c.Models.Issue.Class

    def fill_dict_from_raw_dict(self, raw_json_dict, data, result_dict: dict = None) -> dict:
        if not result_dict:
            result_dict = dict()

        issue_fields = raw_json_dict['fields']
        get_name_or_empty_fields = partial(get_name_or_empty, issue_fields)

        issue_key = raw_json_dict[IA.key]

        result_dict.update(
            {
                IA.key           : issue_key,
                IA.link          : raw_json_dict['self'],

                IA.updated       : issue_fields[IA.updated],
                IA.created       : issue_fields[IA.created],
                IA.summary       : issue_fields[IA.summary],
                IA.description   : issue_fields[IA.description],
                IA.resolutiondate: issue_fields[IA.resolutiondate],
                IA.raw_json      : raw_json_dict,

                IA.type          : get_name_or_empty_fields('issuetype'),
            }
        )

        for key in self.ISSUE_FIELDS_NESTED_DICT_KEYS:
            result_dict[key] = get_name_or_empty_fields(key)

        self.solve_update_or_insert(data[self.Issue.__name__], result_dict, issue_key, primary_key=IssueAttrs.key)

        return result_dict

    def get_existed_entities(self, session: Session) -> set:
        result_dict = dict()
        result = session.query(
            func.coalesce(
                func.array_agg(self.Issue.key), []
            )
        ).scalar()
        for key in result:
            result_dict[key] = key
        self.existed_entities = result_dict
        return result

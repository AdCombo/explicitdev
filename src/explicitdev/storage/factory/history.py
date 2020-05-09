from datetime import datetime

from sqlalchemy.orm import Session

from explicitdev.storage.factory.abstract import FactoryAbstract
from explicitdev.storage.model.status import StatusAttrs
from explicitdev.utils.datetime import convert_to_datetime
from explicitdev.utils.nested_dict import get_nested_dict


def get_name_or_empty(dict_: dict, key: str):
    """
    Get value from nested dict with predifined arguments.
    :param dict_:
    :param key:
    :return:
    """
    return get_nested_dict(dict_, key, 'name', fallback_value='')


SA = StatusAttrs


class FactoryHistory(FactoryAbstract):
    def __init__(self, c):
        super().__init__(c)
        self.status_factory = c.Models.Status.Factory(c)
        self.Status = c.Models.Status.Class

    def get_existed_entities(self, session: Session):
        self.status_factory.get_existed_entities(session)

    def fill_dict_from_raw_dict(
            self,
            raw_issue_dict,
            data,
            issue_key: str = None,
            issue_created: datetime = None,
            issue_status: str = None,
            existed_statutes: set = None,
    ) -> dict:
        statuses_container = data[self.Status.__name__]

        previous_status_ts = issue_created
        for history_dict in raw_issue_dict['changelog']['histories']:
            history_created = history_dict['created']
            history_id = history_dict['id']
            for item_dict in history_dict['items']:
                # todo maybe compose fields type into enum?
                if item_dict['field'] == 'status':
                    item_status = item_dict['fromString']
                    previous_status_ts = convert_to_datetime(previous_status_ts)
                    status_dict = {
                        SA.issue_key: issue_key,
                        SA.jira_id  : history_id,
                        SA.status   : item_status,
                        SA.start_ts : previous_status_ts,
                        SA.end_ts   : history_created,
                    }
                    # Depends on jira it possible to obtain null status, but we have to move timestamp forward
                    if item_status:
                        self.status_factory.solve_update_or_insert(statuses_container, status_dict,
                                                                   (issue_key, previous_status_ts, item_status))
                    previous_status_ts = history_created
        previous_status_ts = convert_to_datetime(previous_status_ts)
        current_status_dict = {
            SA.issue_key: issue_key,
            SA.status   : issue_status,
            SA.start_ts : previous_status_ts,
        }
        self.status_factory.solve_update_or_insert(statuses_container, current_status_dict,
                                                   checking_value=(issue_key, previous_status_ts, issue_status))
        return raw_issue_dict

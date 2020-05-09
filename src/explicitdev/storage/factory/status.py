from sqlalchemy.orm import Session

from explicitdev.storage.factory.abstract import FactoryAbstract
from explicitdev.storage.model.status import StatusAttrs
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


class FactoryStatus(FactoryAbstract):

    def __init__(self, c):
        super().__init__(c)
        self.Status = c.Models.Status.Class

    def get_existed_entities(self, session: Session):
        existed_entites = dict()
        # todo write correct type for this
        query = session.query(
            self.Status.id,
            self.Status.issue_key,
            self.Status.start_ts,
            self.Status.status,
        )
        for row in query:
            existed_entites[(row.issue_key, row.start_ts, row.status)] = row.id
        self.existed_entities = existed_entites

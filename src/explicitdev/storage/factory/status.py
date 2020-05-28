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

    def get_existed_entities(self, session: Session, **kwargs):
        # noinspection PyTypeChecker
        result = super().get_existed_entities(
            session=session,
            model=self.Status,
            columns=(
                SA.issue_key,
                SA.start_ts,
                SA.status,
            ),
        )
        return result

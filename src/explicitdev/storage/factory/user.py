from sqlalchemy.orm import Session

from explicitdev.storage.factory.abstract import FactoryAbstract
from explicitdev.storage.model.user import (
    UserAttrs,
)

UA = UserAttrs


class FactoryUser(FactoryAbstract):

    def __init__(self, c):
        super().__init__(c)
        self.User = c.Models.User.Class

    def fill_dict_from_raw_dict(self, raw_json_dict, data, result_dict: dict = None) -> dict:
        if not result_dict:
            result_dict = dict()

        self.solve_update_or_insert(data[self.User.__name__], result_dict, result_dict[UA.jira_name])

        return result_dict

    def get_existed_entities(self, session: Session, **kwargs) -> dict:
        # noinspection PyTypeChecker
        result = super().get_existed_entities(
            session=session,
            model=self.User,
            columns=(
                UA.jira_name,
            ),
        )
        return result

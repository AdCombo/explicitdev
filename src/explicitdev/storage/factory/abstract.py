from typing import (
    TYPE_CHECKING,
    List,
    Type,
    Dict, Tuple,
)

import attr
from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from explicitdev.config import Config
    from explicitdev.storage.model.base import Base


@attr.s(auto_attribs=True)
class ModelBulkInsertUpdate:
    update: List[dict] = attr.ib(default=attr.Factory(list))
    insert: List[dict] = attr.ib(default=attr.Factory(list))
    model: 'Type[Base]' = None


DataDict = Dict[str, ModelBulkInsertUpdate]


class FactoryAbstract:
    def __init__(self, c):
        # type: (Type[Config]) -> None
        self.c = c
        self.existed_entities = None

    def fill_dict_from_raw_dict(self, raw_json_dict: dict, data: DataDict) -> dict:
        """

        :param raw_json_dict: dict with values to fill result dict
        :param data:
        :param result_dict:
        :return:
        """
        pass

    def solve_update_or_insert(
            self,
            data_container: ModelBulkInsertUpdate,
            entity_dict: dict,
            checking_value,
            primary_key='id',
    ):
        """

        :param data_container:
        :param entity_dict:
        :param checking_value: unique id for checking in existing values dict
        :param primary_key:
        :return:
        """
        id_ = self.existed_entities.get(checking_value)
        if id_:
            entity_dict[primary_key] = id_
            data_container.update.append(entity_dict)
        else:
            data_container.insert.append(entity_dict)

    def get_existed_entities(
            self,
            session: Session,
            model=None,
            columns: Tuple[str] = None,
            id_field: str = 'id',
    ) -> dict:
        """

        :param id_field:
        :param model:
        :param columns: column from model to aggregate from data and set keys for result dict
        :param session:
        :return:
        """
        existed_entites = dict()
        # todo write correct type for this

        model_columns = [getattr(model, column) for column in columns]
        query = session.query(
            getattr(model, id_field),
            *model_columns,
        )
        for row in query:
            key = [getattr(row, c) for c in columns]
            if len(key) == 1:
                key = key[0]
            else:
                # key should be tuple if it contains many keys
                key = tuple(key)
            existed_entites[key] = getattr(row, id_field)
        self.existed_entities = existed_entites

        return existed_entites


__all__ = [
    FactoryAbstract.__name__,
]

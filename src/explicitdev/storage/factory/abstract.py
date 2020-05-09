from typing import (
    TYPE_CHECKING,
    List,
    Type,
    Dict,
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
        pass

    def solve_update_or_insert(self, data_container: ModelBulkInsertUpdate, entity_dict: dict, checking_value,
                               primary_key='id'):
        id_ = self.existed_entities.get(checking_value)
        if id_:
            entity_dict[primary_key] = id_
            data_container.update.append(entity_dict)
        else:
            data_container.insert.append(entity_dict)

    def get_existed_entities(self, session: Session):
        pass


__all__ = [
    FactoryAbstract.__name__,
]

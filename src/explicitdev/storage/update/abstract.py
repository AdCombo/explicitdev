import logging
from typing import TYPE_CHECKING

from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError

from explicitdev.config import Config
from explicitdev.storage.factory.abstract import ModelBulkInsertUpdate, DataDict
from explicitdev.utils.abstract import AbstractWithConfig

if TYPE_CHECKING:
    from explicitdev.storage.model.base import ModelContainerTypeTuple


class AbstractUpdate(AbstractWithConfig):

    def __init__(self, c: Config, *args, **kwargs):
        super().__init__(c, *args, **kwargs)
        # noinspection PyTypeChecker
        self.models_with_containers: 'ModelContainerTypeTuple' = None

    @staticmethod
    def _bulk_update_insert_mappings(session: Session, data: DataDict):
        for name, container in data.items():
            logging.info('Going to insert %s %s into DB', len(container.insert), name)
            session.bulk_insert_mappings(container.model, container.insert)
            # For avoid different problems simply always override all fields in all entities.
            logging.info('Going to update %s %s in DB', len(container.update), name)
            session.bulk_update_mappings(container.model, container.update)
            session.flush()
            container.update = list()
            container.insert = list()

    def _create_data_containers_dict(self):
        """Create containers for transport data between code."""
        data = dict()
        for model in self.models_with_containers:
            data[model.__name__] = ModelBulkInsertUpdate(model=model)
        return data

    def drop_create_tables(self):
        for model in self.models_with_containers:
            model_name = model.__name__
            logging.info('Going to drop %s', model_name)
            try:
                model.__table__.drop(self.c.engine)
            except ProgrammingError:
                logging.info('Table for model %s doesn\'t exsit', model_name)
            logging.info('Going to create %s', model_name)
            model.__table__.create(self.c.engine)

    def sync(self):
        pass

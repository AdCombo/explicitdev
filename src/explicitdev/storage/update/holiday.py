from explicitdev.config import Config
from explicitdev.fetch.holiday_csv import FetchHolidayCSV
from explicitdev.storage.factory import FactoryHoliday
from explicitdev.storage.update.abstract import AbstractUpdate


class UpdateHolidayCSV(AbstractUpdate):

    def __init__(self, c: Config, *args, **kwargs):
        super().__init__(c, *args, **kwargs)
        self.models_with_containers = (c.Models.Holiday.Class,)

    def sync(self):
        fetcher = FetchHolidayCSV(self.c)
        factory = FactoryHoliday(self.c)
        containers = self._create_data_containers_dict()
        with self.c.session_context() as session:
            factory.get_existed_entities(session)
            for row in fetcher.get_data():
                factory.fill_dict_from_raw_dict(row, containers)
            self._bulk_update_insert_mappings(session, containers)
            # Todo write verification for a working and non-working day for a row
            session.commit()

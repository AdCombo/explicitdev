from explicitdev.config import Config
from explicitdev.fetch.abstract_csv import FetchCSV


class FetchHolidayCSV(FetchCSV):

    def __init__(self, c: Config):
        super().__init__(c)
        self.file_name = c.DataFiles.HOLIDAYS

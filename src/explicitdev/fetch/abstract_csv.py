import csv
from pathlib import Path

from explicitdev.utils.abstract import AbstractWithConfig


class FetchCSV(AbstractWithConfig):

    def __init__(self, c, *args, **kwargs):
        super().__init__(c, *args, **kwargs)
        self.data_path: Path = c.DataFiles.PATH
        self.file_name: str = ''

    def get_data(self):
        file_path = self.data_path.joinpath(self.file_name)
        # noinspection PyTypeChecker
        with open(file_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row

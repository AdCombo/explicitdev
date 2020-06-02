from datetime import date

from sqlalchemy.orm import Session

from explicitdev.storage.factory.abstract import FactoryAbstract
from explicitdev.storage.model import HolidayAttrs
from explicitdev.storage.model.holiday import HolidayType

HA = HolidayAttrs


class FactoryHoliday(FactoryAbstract):
    YEAR_FIELD_NAME = 'Год/Месяц'

    SKIP_SYMBOL = '*'
    """A symbol from calenders on witch we skip days."""

    def __init__(self, c):
        super().__init__(c)
        self.Holiday = c.Models.Holiday.Class

    def fill_dict_from_raw_dict(self, raw_json_dict, data, result_dict: dict = None) -> dict:
        """

        :param raw_json_dict:
        :param data:
        :param result_dict: Actually passing this will not work, because result_dict generated internally.
        :return:
        """
        if not result_dict:
            result_dict = dict()

        rjd = raw_json_dict
        year = int(rjd.pop(self.YEAR_FIELD_NAME))
        for month, month_days in enumerate(rjd.values(), start=1):
            if month > 12:
                break
            for day in month_days.split(','):
                try:
                    day = int(day)
                except ValueError:
                    symbol = day[-1:]
                    if symbol == self.SKIP_SYMBOL:
                        continue
                    day = int(day[:-1])

                result_dict = {
                    HA.date: date(year, month, day),
                    HA.type: HolidayType.government,
                }

                self.solve_update_or_insert(
                    data[self.Holiday.__name__],
                    result_dict,
                    result_dict[HA.date],
                )

        return result_dict

    def get_existed_entities(self, session: Session, **kwargs) -> dict:
        # noinspection PyTypeChecker
        result = super().get_existed_entities(
            session=session,
            model=self.Holiday,
            columns=(
                HA.date,
            ),
        )
        return result

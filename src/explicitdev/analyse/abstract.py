import logging
from typing import Type, TYPE_CHECKING

from explicitdev.utils.abstract import AbstractWithConfig
from explicitdev.utils.const import ReportSaveModes
from explicitdev.utils.csv import save_alchemy_query_to_csv

if TYPE_CHECKING:
    from explicitdev.config import Config


class AbstractAnalyzer(AbstractWithConfig):

    def __init__(self, c: 'Config', *args, **kwargs):
        super().__init__(c, *args, **kwargs)
        self.Issue = c.Models.Issue.Class
        self.Status = c.Models.Status.Class
        self.Report: Config.Reports.AbstractReport = None
        """Report upload settings from config"""

    def get_report(self):
        """Method for actually getting and saving report"""
        pass

    def _save_results_to_csv(self, results_query, report_name: str, **kwargs):
        report_path = self.c.Reports.dir.joinpath(report_name)
        save_alchemy_query_to_csv(results_query, report_path, **kwargs)

    @staticmethod
    def _get_rows_from_query(query):
        first_row = True
        for row in query:
            if first_row:
                # возвражаещ заголовки
                yield tuple(row._asdict().keys())
                first_row = False
            yield tuple(row)

    def _update_gspread(self, query):
        class_name = self.Report.__name__

        gc = self.c.Reports.gspread_client
        spread_sheet = gc.open_by_key(self.Report.gspread_key)
        work_sheet = spread_sheet.worksheet(self.Report.gspread_worksheet_name)
        old_row_count = work_sheet.row_count
        rows = list(self._get_rows_from_query(query))
        new_rows_count = len(rows)
        logging.info('Going to upload %s rows into %s report', new_rows_count, class_name)
        work_sheet.insert_rows(
            rows,
        )
        logging.info('Upload data to %s completed', class_name)
        logging.info('Going to delete old %s rows', old_row_count)
        work_sheet.delete_rows(1, old_row_count)
        # for don't touch first row
        # work_sheet.delete_rows(2, old_row_count)
        logging.info(('Rows delete complete.'))

    def _save_report(self, query):
        save_mode = self.Report.save_mode
        if save_mode == ReportSaveModes.csv:
            self._save_results_to_csv(query, self.Report.csv_name)
        elif save_mode == ReportSaveModes.gspread:
            self._update_gspread(query)
        else:
            raise NotImplementedError('Unknonw save mode for the report.')

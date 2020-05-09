from typing import Type, TYPE_CHECKING

from explicitdev.utils.csv import save_alchemy_query_to_csv

if TYPE_CHECKING:
    from explicitdev.config import Config


class AbstractAnalyzer:
    def __init__(self, c):
        # type: (Type[Config]) -> None
        self.c = c
        self.Issue = c.Models.Issue.Class
        self.Status = c.Models.Status.Class

    def save_results_to_csv(self, results_query, report_name: str, **kwargs):
        report_path = self.c.Reports.dir.joinpath(report_name)
        save_alchemy_query_to_csv(results_query, report_path, **kwargs)

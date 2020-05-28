from datetime import timezone, datetime

from explicitdev.storage.model import UserAttrs
from sqlalchemy import func, select, text, and_, column, alias

from explicitdev.analyse.abstract import AbstractAnalyzer
from explicitdev.storage.model.user import UserType


class JiraAnalyzer(AbstractAnalyzer):
    pass


class UserBeginPerformance(AbstractAnalyzer):
    PERIOD_START_DATE = 'period_start_date'
    PERIOD_END_DATE = 'period_end_date'
    PERIOD_NUMBER = 'period_number'

    SHIFT_INTERVAL = text("INTERVAL  '30 days'")

    def __init__(self, c):
        super().__init__(c)
        self.Report = c.Reports.UserBeginPerformance
        self.User = c.Models.User.Class
        self.Issue = c.Models.Issue.Class

    def get_report(self):
        """Данный очёт показывает количество тех задач которые не могут быть отрезолвены"""
        with self.c.session_context() as session:
            # todo create additional request for guaranty all month in timeline
            # date_list = func.generate_series(first_date, datetime.now(timezone.utc), '1 day').alias('end_month')

            User = self.User
            Issue = self.Issue

            # sq_created_count = self.count_for_month(session, Issue.created)
            # sq_resolved_count = self.count_for_month(session, Issue.resolutiondate)
            # created_year_month_column = sq_created_count.c[self.FIELD_YEAR_MONTH]
            # resolved_count_column = sq_resolved_count.c[self.FIELD_COUNT]
            # created_count_column = sq_created_count.c[self.FIELD_COUNT]
            # growth_column = created_count_column - resolved_count_column

            sq = session.query(
                User.jira_name,
                # begin_column,
                func.generate_series(
                    # to get only full periods before current date
                    User.working_start_date + self.SHIFT_INTERVAL,
                    datetime.now(timezone.utc),
                    '30 days',
                ).label(self.PERIOD_END_DATE),
                # (
                #         column(self.PERIOD_END_DATE) - column(self.SHIFT_INTERVAL)
                # ).label(self.PERIOD_START_DATE),

            ).filter(
                User.type.in_((UserType.backend,))
            ).subquery()

            column_period_end_date = sq.c[self.PERIOD_END_DATE]
            column_period_start_date = column_period_end_date - self.SHIFT_INTERVAL

            q = session.query(
                sq.c[UserAttrs.jira_name],
                # Numerate all periods of working in company from the begining
                func.row_number().over(
                    order_by=column_period_end_date,
                    partition_by=sq.c[UserAttrs.jira_name],
                ).label(self.PERIOD_NUMBER),
                column_period_end_date,
                column_period_start_date.label(self.PERIOD_START_DATE),
                Issue.resolutiondate,
            ).outerjoin(
                Issue, and_(
                    Issue.resolutiondate >= column_period_start_date,
                    Issue.resolutiondate < column_period_end_date,
                )
            )

            self._save_report(q)

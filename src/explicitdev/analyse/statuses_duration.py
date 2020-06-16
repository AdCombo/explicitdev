from datetime import datetime, timezone, time, timedelta

from sqlalchemy import func, literal_column, and_, text, case, Integer, cast, Date
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import coalesce

from explicitdev.analyse.abstract import AbstractAnalyzer
from explicitdev.config import Config
from explicitdev.storage.model import StatusAttrs


class StatusesDuration(AbstractAnalyzer):
    STATUS_DURATION = 'status_duration'
    STATUS_DURATION_DAYS = 'status_duration_days'
    STATUS_PERIODS_COUNT = 'status_periods_count'
    LAST_STATUS_CHANGE_TIME = 'last_status_change_time'
    FIRST_STATUS_CHANGE_TIME = 'first_status_change_time'
    WORK_TIME_DURATION = 'work_time_duration'
    WORK_TIME_DURATION_SUM = 'work_time_duration_sum'
    HOLIDAYS_PERIOD_COUNT = 'holidays_period_count'

    ONE_DAY_INTERVAL = text("INTERVAL  '1 days'")

    WORK_DAY_START = time(8, 0, 0, 0, timezone.utc)
    WORK_DAY_END = time(16, 0, 0, 0, timezone.utc)
    WORK_HOURS_PER_DAY = 8

    def __init__(self, c: Config):
        super().__init__(c)
        self.Report = c.Reports.StatusesDuration
        self.User = c.Models.User.Class
        self.Issue = c.Models.Issue.Class
        self.Status = c.Models.Status.Class
        self.Holiday = c.Models.Holiday.Class

    def get_max_date(self, session, filter_date):
        """
        Return max first non holiday day lesser or equal to passed one.
        :param session:
        :param filter_date:
        :return:
        """
        Holiday = self.Holiday

        max_holiday = func.max(Holiday.date)

        query_date = session.query(Holiday.date).subquery()

        # Ищем первый невыходной день меньше текущего
        sq = session.query(max_holiday - self.ONE_DAY_INTERVAL).filter(
            (Holiday.date - self.ONE_DAY_INTERVAL).notin_(query_date),
            Holiday.date <= filter_date,
        ).as_scalar()

        result = session.query(
            case(
                [
                    # If it non holiday, just return current day
                    (max_holiday != filter_date, filter_date),
                ],
                # else return first work day with calculation
                else_=sq
            ),
        ).filter(
            Holiday.date <= filter_date,
        ).scalar()

        return result.date()

    def get_last_work_day_end_time(self, session: Session):
        Holiday = self.Holiday

        now = datetime.now(timezone.utc)
        today = now.date()
        now_time = now.timetz()

        last_work_day = self.get_max_date(session, today)

        if today != last_work_day:
            return datetime.combine(last_work_day, self.WORK_DAY_END)

        elif now_time < self.WORK_DAY_START:
            # Если рабочий день ещё не начался, берём предыдущий рабочий день
            last_work_day = self.get_max_date(session, today - timedelta(days=1))
            return datetime.combine(last_work_day, self.WORK_DAY_END)

        elif self.WORK_DAY_START <= now_time <= self.WORK_DAY_END:
            return now

        elif self.WORK_DAY_END < now_time:
            return datetime.combine(last_work_day, self.WORK_DAY_END)
        else:
            raise ValueError('Something goes wrong!')

    def _prepare_query(self, session: Session, final_query_fields):
        Status = self.Status
        Holiday = self.Holiday

        end_ts = coalesce(Status.end_ts, self.get_last_work_day_end_time(session))
        status_duration = end_ts - Status.start_ts
        status_duration_days = func.date_part('DAY', status_duration)
        holiday_period_count = func.count(Holiday.date)

        sq = session.query(
            Status.issue_key,
            Status.status,
            Status.start_ts,
            end_ts.label('end_ts'),
            status_duration.label(self.STATUS_DURATION),
            status_duration_days.label(self.STATUS_DURATION_DAYS),
            holiday_period_count.label(self.HOLIDAYS_PERIOD_COUNT),
        ).outerjoin(
            # Leave only days stricly between start and end of a status interval
            Holiday, and_(
                end_ts > Holiday.date,
                Status.start_ts < Holiday.date,
            )
        ).group_by(
            Status.issue_key,
            Status.status,
            Status.start_ts,
            end_ts,
            status_duration,
            status_duration_days,
        ).subquery()

        status_duration = sq.c[self.STATUS_DURATION]
        holiday_period_count = sq.c[self.HOLIDAYS_PERIOD_COUNT]
        start_date = cast(sq.c[StatusAttrs.start_ts], Date)
        end_date = cast(sq.c[StatusAttrs.end_ts], Date)
        # Calculate it differently because we need only days inside range
        status_duration_days = end_date - start_date
        # Worktime days end
        end_of_start_day = start_date + self.WORK_DAY_END
        start_of_end_day = end_date + self.WORK_DAY_START
        start_ts = sq.c[StatusAttrs.start_ts]
        end_ts = sq.c[StatusAttrs.end_ts]
        query_fields = [sq.c[field_name] for field_name in final_query_fields]
        """Fields for group_by and select"""

        q = session.query(
            func.sum(
                case([
                    # If begin and end in a same calendar day, just return difference.
                    (start_date == end_date, status_duration),
                    (
                        start_date != end_date,
                        # calculate start day work time
                        case(
                            [
                                # If start of a status lesser then the work_day_end, return difference. Otherwise just 0
                                (start_ts < end_of_start_day, end_of_start_day - start_ts),
                            ],
                            else_=timedelta(0),
                        ) +
                        # calculate full working hours for working days between start and end days
                        func.make_interval(
                            0, 0, 0, 0,
                            # Convert hours to pg interval.
                            cast(
                                (status_duration_days - sq.c[self.HOLIDAYS_PERIOD_COUNT]) * self.WORK_HOURS_PER_DAY,
                                Integer
                            )
                        ) +
                        # Calculate end day work time
                        case(
                            [
                                # If end of a status is greater then the work start of the day, return difference.
                                (end_ts > start_of_end_day, end_ts - start_of_end_day),
                            ],
                            else_=timedelta(0),
                        )
                        ,
                    ),
                ])
            ).label(self.WORK_TIME_DURATION),
            func.sum(sq.c[self.STATUS_DURATION]).label(self.STATUS_DURATION),
            *query_fields,
        ).group_by(
            *query_fields,
        )

        return q

    def prepare_query(self, session: Session):
        return self._prepare_query(session, (StatusAttrs.issue_key, StatusAttrs.status))

    def query_group_by_jira_key(self, session):
        return self._prepare_query(session, (StatusAttrs.issue_key,))

    def get_report(self):
        """Данный очёт показывает количество тех задач которые не могут быть отрезолвены"""
        with self.c.session_context() as session:
            query = self.prepare_query(session)

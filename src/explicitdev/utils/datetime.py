from datetime import datetime, timedelta

FORMAT_FOR_JIRA_TIME = "%Y-%m-%dT%H:%M:%S.%f%z"


def convert_to_datetime(s: str) -> datetime:
    return datetime.strptime(s, FORMAT_FOR_JIRA_TIME)


def days_hours_minutes_delta(td: timedelta, as_str=True):
    result = td.days * 24 + td.seconds // 3600, (td.seconds // 60) % 60, td.seconds % 60
    if as_str:
        result = ':'.join((str(r) for r in result))
    return result

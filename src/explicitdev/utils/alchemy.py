from sqlalchemy import func


def date_to_str(column, format: str):
    return func.to_char(column, format)


def date_to_iso_str(column):
    return date_to_str(column, 'YYYY-MM-DD"T"HH24:MI:SS"Z"')


def date_year_month_str(column):
    return date_to_str(column, 'YYYY-MM')

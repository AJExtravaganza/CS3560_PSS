from calendar import monthrange
from datetime import datetime, date, timedelta
from typing import Union


def days_in_month(year: int, month: int):
    return monthrange(year, month)[1]


def increment_month(dt: datetime):
    year = dt.year if dt.month != 12 else (dt.year + 1)
    month = (dt.month + 1) if dt.month != 12 else 1
    day = min(dt.day, days_in_month(year, month))
    return dt.replace(year=year, month=month, day=day)


def first_of_month(current_date: Union[datetime, date]):
    result = current_date.date() if type(current_date) is datetime else current_date
    result.replace(day=1)
    return result


def last_of_month(current_date: Union[datetime, date]):
    return increment_month(first_of_month(current_date)) - timedelta(days=1)

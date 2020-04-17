import enum
from calendar import monthrange
from datetime import date, datetime, timedelta
from typing import List

from Task import Task


class RecurrenceFrequency(enum.Enum):
    DAILY = 1
    WEEKLY = 7
    MONTHLY = 30


class RecurringTask(Task):
    end_date: date
    frequency: RecurrenceFrequency
    cancellations: List[date]
    valid_types = {
        'Class',
        'Study',
        'Sleep',
        'Exercise',
        'Work',
        'Meal',
    }

    def __init__(self, json: dict):
        try:
            self.cancellations = []
            end_date_string = str(json['EndDate'])
            self.end_date = datetime.strptime(end_date_string, '%Y%m%d').date()

            self.frequency = RecurrenceFrequency(json['Frequency'])
        except KeyError as err:
            raise ValueError(f'Task definition lacks required field: {err}')
        except ValueError as err:
            raise ValueError(f"Task definition has invalid data: {err}")
        super().__init__(json)

    def as_dict(self):
        base = super(RecurringTask, self).as_dict()
        base.update({
            'EndDate': int(self.end_date.strftime('%Y%m%d')),
            'Frequency': self.frequency.value
        })
        return base

    def generate_recurrence_datetimes(self):
        def days_in_month(year: int, month: int):
            return monthrange(year, month)[1]

        def increment_month(dt: datetime):
            year = dt.year if dt.month != 12 else (dt.year + 1)
            month = (dt.month + 1) if dt.month != 12 else 1
            day = min(dt.day, days_in_month(year, month))
            return dt.replace(year=year, month=month, day=day)

        current_datetime = self.start
        recurrences = []

        while current_datetime.date() <= self.end_date:
            recurrences.append(current_datetime)

            if self.frequency == RecurrenceFrequency.DAILY:
                current_datetime += timedelta(days=1)
            elif self.frequency == RecurrenceFrequency.WEEKLY:
                current_datetime += timedelta(days=7)
            elif self.frequency == RecurrenceFrequency.MONTHLY:
                current_datetime = increment_month(current_datetime)
                current_datetime = current_datetime.replace(
                    day=min(self.start.day, days_in_month(current_datetime.year, current_datetime.month)))
            else:
                raise ValueError(f"RecurringTask.frequency {self.frequency} is invalid")

        return recurrences

    def coincides_with(self, dt: datetime) -> bool:
        if dt < self.start or dt.date() > self.end_date:
            return False

        if not (dt.hour == self.start.hour and dt.minute == self.start.minute):
            return False

        # If the task is daily, there is no need to iterate over a pattern of days
        if self.frequency == RecurrenceFrequency.DAILY:
            return True

        return dt in self.generate_recurrence_datetimes()

    def add_cancellation(self, dt):
        if not self.coincides_with(dt):
            raise ValueError(
                f'datetime {dt} does not coincide with start_date={self.start}, frequency={self.frequency}')

        self.cancellations.append(dt)

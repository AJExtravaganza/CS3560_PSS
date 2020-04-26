from calendar import monthrange
from datetime import date, datetime, timedelta
from typing import List

from Field import Field
from Task import Task
from enum_RecurrenceFrequency import RecurrenceFrequency
from exceptions import PSSValidationError
from field_validators import validate_date_string, validate_recurrence_frequency


class RecurringTask(Task):
    end_date: date
    frequency: RecurrenceFrequency
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

            self.frequency = RecurrenceFrequency(int(json['Frequency']))
        except KeyError as err:
            raise PSSValidationError(f'Task definition lacks required field: {err}')
        except ValueError as err:
            raise PSSValidationError(f"Task definition has invalid data: {err}")
        super().__init__(json)

    @classmethod
    def get_input_fields(cls) -> List[Field]:
        return super().get_input_fields() + [
            Field('EndDate',
                  'task end date',
                  validate_date_string,
                  'value must be date in YYYYMMDD format'),
            Field('Frequency',
                  'task recurrence frequency',
                  validate_recurrence_frequency,
                  f'value must be in {[enum_value for enum_value in RecurrenceFrequency]}')
        ]

    def as_dict(self):
        base = super(RecurringTask, self).as_dict()
        base.update({
            'EndDate': int(self.end_date.strftime('%Y%m%d')),
            'Frequency': self.frequency.value,
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
            if current_datetime.date() not in [anti_task.start.date() for anti_task in self.cancellations]:
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
                raise PSSValidationError(f"RecurringTask.frequency {self.frequency} is invalid")

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

    def has_cancellation_with_name(self, name: str):
        return any([cancellation.name == name for cancellation in self.cancellations])

    def add_anti_task(self, anti_task):
        cancellation_datetime = datetime(year=anti_task.start.year, month=anti_task.start.month, day=anti_task.start.day).replace(hour=self.start.hour, minute=self.start.minute)

        if not self.coincides_with(cancellation_datetime):
            raise PSSValidationError(
                f'date {anti_task.date} does not coincide with start_date={self.start.date()}, frequency={self.frequency}')

        self.cancellations.append(anti_task)

    def remove_cancellation(self, anti_task):
        try:
            matching_cancellation = next(filter(lambda existing_anti_task: existing_anti_task.start.date == anti_task.start.date, self.cancellations))
        except StopIteration:
            raise PSSValidationError(f'Task "{self.name} has no existing cancellation on {anti_task.start.date}"')

        self.cancellations.remove(matching_cancellation)

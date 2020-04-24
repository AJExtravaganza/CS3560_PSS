from collections import Set
from datetime import datetime, timedelta
from math import floor
from typing import List

from Field import Field
from field_validators import validate_nonempty_string, validate_date_string, validate_time_string, \
    validate_task_duration_string, validate_value_in_set


def validate_fractional_hours(hours: float) -> float:
    if hours * 4 % 1 != 0:
        raise ValueError('Duration must be a fractional hour value corresponding to a multiple of 15 minutes')
    return hours


class Task:
    name: str
    type: str
    start: datetime
    duration_minutes: int

    valid_types: set = set()

    def __init__(self, json: dict):
        try:
            self.name = json['Name']
            self.type = json['Type']

            start_date_string = str(json['StartDate'])
            start_hours = validate_fractional_hours(float(json['StartTime']))
            self.start = datetime.strptime(start_date_string, '%Y%m%d') \
                .replace(hour=floor(start_hours), minute=int(start_hours % 1 * 60))

            duration_hours = validate_fractional_hours(float(json['Duration']))
            self.duration_minutes = int(duration_hours * 60)

        except (ValueError, KeyError):
            raise ValueError("Attempted to instantiate task from invalid data: " + str(json))

        if self.type not in self.valid_types:
            raise ValueError("Attempted to instantiate task from invalid data: " + str(json))

    def __lt__(self, other):
        return self.start < other.start

    def overlaps(self, other):
        self_finish = self.start + timedelta(minutes=self.duration_minutes)
        other_finish = other.start + timedelta(minutes=other.duration_minutes)
        if self.start > other.start:
            return self.start < other_finish
        else:
            return self_finish > other.start

    def as_dict(self):
        return {
            'Name': self.name,
            'Type': self.type,
            'StartDate': int(self.start.strftime('%Y%m%d')),
            'StartTime': self.start.hour + self.start.minute / 60,
            'Duration': self.duration_minutes / 60
        }

    @classmethod
    def get_input_fields(cls) -> List[Field]:
        return [
            Field('Name',
                  'task name',
                  validate_nonempty_string,
                  'value must have len > 0'),

            Field('Type',
                  'task type',
                  lambda x: validate_value_in_set(x, cls.valid_types),
                  f'value must be in {cls.valid_types}'),

            Field('StartDate',
                  'task start date',
                  validate_date_string,
                  'value must be date in YYYYMMDD format'),

            Field('StartTime',
                  'task start time',
                  validate_time_string,
                  'value must be floating-point number in [0.0, 23.75]'),

            Field('Duration',
                  'task duration (minutes)',
                  validate_task_duration_string,
                  'value must be positive integer in [0, 3600]')
        ]

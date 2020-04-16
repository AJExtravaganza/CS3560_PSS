import enum
from datetime import date, datetime

from Task import Task


class RecurrenceFrequency(enum.Enum):
    DAILY = 1
    WEEKLY = 7
    MONTHLY = 30


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
            self.name = json['Name']
            self.type = json['Type']

            end_date_string = str(json['EndDate'])
            self.end_date = datetime.strptime(end_date_string, '%Y%m%d').date()

            self.frequency = json['Frequency']
        except KeyError as err:
            raise ValueError(f'Task definition lacks required field: {err}')
        except ValueError as err:
            raise ValueError(f"Task definition has invalid data: {err}")
        super().__init__(json)

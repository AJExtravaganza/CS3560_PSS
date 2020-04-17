from collections import Set
from datetime import datetime, timedelta
from math import floor


def validate_fractional_hours(hours: float) -> float:
    if hours * 4 % 1 != 0:
        raise ValueError('Duration must be a fractional hour value corresponding to a multiple of 15 minutes')
    return hours


class Task:
    name: str
    type: str
    start: datetime
    duration_minutes: int

    valid_types: Set

    def __init__(self, json: dict):
        try:
            self.name = json['Name']
            self.type = json['Type']

            start_date_string = str(json['StartDate'])
            start_hours = validate_fractional_hours(json['StartTime'])
            self.start = datetime.strptime(start_date_string, '%Y%m%d') \
                .replace(hour=floor(start_hours), minute=int(start_hours % 1 * 60))

            duration_hours = validate_fractional_hours(json['Duration'])
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

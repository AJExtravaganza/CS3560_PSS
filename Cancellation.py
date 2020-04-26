from datetime import date


class Cancellation:
    def __init__(self, cancellation_date: date, name: str):
        self.name = name
        self.date = cancellation_date

    def __str__(self):
        return f'{self.date} ({self.name})'

    def __eq__(self, other):
        return self.name == other.name \
            and self.date == other.date

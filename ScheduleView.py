from abc import ABC
from datetime import date
from typing import Union, List

from RecurringTaskInstance import RecurringTaskInstance
from TransientTask import TransientTask


class ScheduleView(ABC):
    start: date
    end: date

    def __init__(self, tasks: List[Union[TransientTask, RecurringTaskInstance]]):
        self.tasks = sorted(
            filter(lambda task: self.start <= task.start.date() <= self.end, tasks))

    def display(self):
        pass

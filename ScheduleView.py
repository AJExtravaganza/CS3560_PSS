from abc import ABC
from datetime import date
from typing import List

from TaskInstance import TaskInstance


class ScheduleView(ABC):
    start: date
    end: date

    def __init__(self, tasks: List[TaskInstance]):
        self.tasks = sorted(
            filter(lambda task: self.start <= task.start.date() <= self.end, tasks))

    def display(self):
        pass

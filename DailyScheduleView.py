from datetime import date
from typing import List

from CliView import CliView
from ScheduleView import ScheduleView
from TaskInstance import TaskInstance


class DailyScheduleView(ScheduleView):
    def __init__(self, tasks: List[TaskInstance], start: date):
        self.start = start
        self.end = start
        super().__init__(tasks)

    def display(self):
        CliView.display_schedule_chunk(self.tasks, f'SCHEDULE FOR {self.start}:')

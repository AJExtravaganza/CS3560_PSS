from datetime import date
from typing import List, Union

from CliView import CliView
from RecurringTaskInstance import RecurringTaskInstance
from ScheduleView import ScheduleView
from TransientTask import TransientTask


class DailyScheduleView(ScheduleView):
    def __init__(self, tasks: List[Union[TransientTask, RecurringTaskInstance]], start: date):
        self.start = start
        self.end = start
        super().__init__(tasks)

    def display(self):
        CliView.display_schedule_chunk(self.tasks, f'SCHEDULE FOR {self.start}:')

from collections import OrderedDict
from datetime import date, timedelta
from functools import reduce
from typing import List

from CliView import CliView
from ScheduleView import ScheduleView
from TaskInstance import TaskInstance
from datetime_helpers import first_of_month, last_of_month


class MonthlyScheduleView(ScheduleView):
    def __init__(self, tasks: List[TaskInstance], start: date):
        self.start = first_of_month(start)
        self.end = last_of_month(start)
        super().__init__(tasks)

    def display(self):
        def put_in_date_bucket(buckets: OrderedDict, task: TaskInstance):
            if task.start.date() in buckets:
                buckets.get(task.start.date()).append(task)
            else:
                buckets.update({task.start.date(): [task, ]})

            return buckets

        tasks_by_date = reduce(put_in_date_bucket, self.tasks, OrderedDict())
        for d, tasks_for_date in tasks_by_date.items():
            CliView.display_schedule_chunk(tasks_for_date, f'SCHEDULE FOR {d}:', '    ')

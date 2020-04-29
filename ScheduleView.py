from abc import ABC
from collections import OrderedDict
from datetime import date
from functools import reduce
from typing import List

from CliView import CliView
from TaskInstance import TaskInstance


class ScheduleView:
    start: date
    end: date

    def __init__(self, tasks: List[TaskInstance]):
        self.tasks = sorted(tasks)

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

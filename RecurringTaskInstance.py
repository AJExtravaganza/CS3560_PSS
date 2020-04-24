from datetime import datetime

from RecurringTask import RecurringTask
from Task import Task


class RecurringTaskInstance(Task):
    valid_types = RecurringTask.valid_types

    def __init__(self, recurring_task: RecurringTask, dt: datetime):
        super().__init__(recurring_task.as_dict())
        self.start = dt

    @staticmethod
    def generate_instances(recurring_task: RecurringTask, **kwargs):
        range_start = kwargs.get('start', recurring_task.start.date())
        range_end = kwargs.get('end', recurring_task.end_date)
        return [RecurringTaskInstance(recurring_task, dt)
                for dt in recurring_task.generate_recurrence_datetimes()
                if range_start <= dt.date() <= range_end]

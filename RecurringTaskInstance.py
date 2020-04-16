from datetime import datetime

from RecurringTask import RecurringTask
from Task import Task


class RecurringTaskInstance(Task):
    valid_types = RecurringTask.valid_types

    def __init__(self, recurring_task: RecurringTask, dt: datetime, ):
        super().__init__(recurring_task.as_dict())

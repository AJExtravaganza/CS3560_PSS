from RecurringTask import RecurringTask
from Task import Task


class AntiTask(Task):
    valid_types = {'Cancellation'}

    def matches(self, recurring_task: RecurringTask):
        return \
            self.name == recurring_task.name \
            and self.duration_minutes == recurring_task.duration_minutes \
            and recurring_task.coincides_with(self.start)

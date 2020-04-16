from datetime import date

from RecurringTask import RecurringTask
from Task import Task


class AntiTask(Task):
    valid_types = {'Cancellation'}

    def matches(self, recurring_task: RecurringTask):
        return \
            self.name == recurring_task.name \
            and self.duration_minutes == recurring_task.duration_minutes \
            and recurring_task.coincides_with(self.start)

    @staticmethod
    def from_recurring_task(recurring_task: RecurringTask, dt: date):
        init_data = recurring_task.as_dict()
        # start = recurring_task.start.replace(year=dt.year, month=dt.month, day=dt.day)
        init_data['StartDate'] = dt.strftime('%Y%m%d')
        init_data['Type'] = 'Cancellation'
        return AntiTask(init_data)

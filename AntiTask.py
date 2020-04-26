from datetime import date

from RecurringTask import RecurringTask
from Task import Task


class AntiTask(Task):
    valid_types = {'Cancellation'}

    def matches(self, recurring_task: RecurringTask):
        return self.duration_minutes == recurring_task.duration_minutes \
               and recurring_task.coincides_with(self.start)

    @staticmethod
    def from_recurring_task(recurring_task: RecurringTask, d: date):
        init_data = recurring_task.as_dict()
        init_data['Name'] = f'{recurring_task.name}_cancel_{d.strftime("%Y%m%d")}'
        init_data['StartDate'] = d.strftime('%Y%m%d')
        init_data['Type'] = 'Cancellation'
        return AntiTask(init_data)

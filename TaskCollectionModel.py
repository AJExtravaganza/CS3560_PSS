from typing import List

from AntiTask import AntiTask
from FileHandler import FileHandler
from RecurringTask import RecurringTask
from TransientTask import TransientTask


def generate_anti_tasks(recurring_tasks: List[RecurringTask]) -> List[AntiTask]:
    return [AntiTask.from_recurring_task(recurring_task, dt) for recurring_task in recurring_tasks for dt in
            recurring_task.cancellations]


class TaskCollectionModel:
    transient_tasks: List[TransientTask]
    recurring_tasks: List[RecurringTask]

    def load(self, **kwargs):
        filename = kwargs.get('filename', 'schedule.json')
        file_handler = FileHandler(filename)

        tasks = file_handler.read_tasks()
        self.transient_tasks = list(filter(lambda task: task.__class__ == TransientTask, tasks))
        self.recurring_tasks = list(filter(lambda task: task.__class__ == RecurringTask, tasks))

        recurring_tasks_by_name = {}
        recurring_tasks_by_name.update([(task.name, task) for task in self.recurring_tasks])

        anti_tasks = list(filter(lambda task: task.__class__ == AntiTask, tasks))
        for anti_task in anti_tasks:
            try:
                matching_task = recurring_tasks_by_name[anti_task.name]
                if matching_task.coincides_with(anti_task.start):
                    matching_task.add_cancellation(anti_task.start)
            except KeyError as err:
                pass

    def save(self, **kwargs):
        filename = kwargs.get('filename', 'schedule.json')
        file_handler = FileHandler(filename)
        tasks = self.transient_tasks + self.recurring_tasks + generate_anti_tasks(self.recurring_tasks)
        file_handler.write_tasks(tasks)

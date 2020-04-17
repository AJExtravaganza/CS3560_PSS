from datetime import date
from typing import List

from AntiTask import AntiTask
from FileHandler import FileHandler
from RecurringTask import RecurringTask
from RecurringTaskInstance import RecurringTaskInstance
from Task import Task
from TransientTask import TransientTask


class TaskInsertionError(ValueError):
    pass


class TaskNameNotUniqueError(TaskInsertionError):
    pass


class TaskOverlapError(TaskInsertionError):
    pass


class NoAntiTaskMatchError(TaskInsertionError):
    pass


def generate_anti_tasks(recurring_tasks: List[RecurringTask]) -> List[AntiTask]:
    return [AntiTask.from_recurring_task(recurring_task, dt) for recurring_task in recurring_tasks for dt in
            recurring_task.cancellations]


class TaskCollectionModel:
    def __init__(self):
        self.transient_tasks: List[TransientTask] = []
        self.recurring_tasks: List[RecurringTask] = []

    def check_name_uniqueness(self, task: Task):
        existing_names = [task.name for task in self.transient_tasks + self.recurring_tasks]
        if task.name in existing_names:
            raise TaskNameNotUniqueError(f'Task with name {task.name} already exists')

    def check_for_overlap_with_existing_task(self, new_task: Task):
        existing_tasks = self.transient_tasks + [instance for recurring_task in self.recurring_tasks for instance in
                                                 RecurringTaskInstance.generate_instances(recurring_task)]
        new_task_instances = RecurringTaskInstance.generate_instances(
            new_task) if new_task.__class__ == RecurringTask else [new_task, ]
        for new_task_instance in new_task_instances:
            if any([True for existing_task in existing_tasks if new_task_instance.overlaps(existing_task)]):
                raise TaskOverlapError(f'New task overlaps existing task')

    def add_task(self, task: Task):
        if task.__class__ == AntiTask:
            self.add_cancellation(task)
            return

        self.check_name_uniqueness(task)
        self.check_for_overlap_with_existing_task(task)

        if task.__class__ == TransientTask:
            self.transient_tasks.append(task)
        elif task.__class__ == RecurringTask:
            self.recurring_tasks.append(task)
        else:
            raise RuntimeError(f'Unrecognised task class {task.__class__} in TaskCollectionModel::add_task()')

    def add_cancellation(self, anti_task: AntiTask):
        try:
            matching_task = next(
                filter(lambda recurring_task: recurring_task.name == anti_task.name, self.recurring_tasks))
        except StopIteration:
            raise NoAntiTaskMatchError(f'No task matching Antitask with name {anti_task.name}')

        if matching_task.coincides_with(
                anti_task.start) and matching_task.duration_minutes == anti_task.duration_minutes:
            matching_task.add_cancellation(anti_task.start)
        else:
            raise NoAntiTaskMatchError(
                f'No task matching Antitask with name {anti_task.name} coinciding with start={anti_task.start} and duration_minutes={anti_task.duration_minutes}')

    def update_task(self, task: Task):
        pass

    def delete_task(self, task: Task):
        pass

    def remove_cancellation(self, task: Task, date: date):
        pass

    def load(self, **kwargs):
        filename = kwargs.get('filename', 'schedule.json')
        file_handler = FileHandler(filename)

        for task in file_handler.read_tasks():
            try:
                self.add_task(task)
            except TaskInsertionError as err:
                print(str(err) + ', skipping')

        recurring_tasks_by_name = {}
        recurring_tasks_by_name.update([(task.name, task) for task in self.recurring_tasks])

    def save(self, **kwargs):
        filename = kwargs.get('filename', 'schedule.json')
        file_handler = FileHandler(filename)
        tasks = self.transient_tasks + self.recurring_tasks + generate_anti_tasks(self.recurring_tasks)
        file_handler.write_tasks(tasks)

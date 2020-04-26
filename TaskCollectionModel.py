import copy
from typing import List

from AntiTask import AntiTask
from Cancellation import Cancellation
from FileHandler import FileHandler
from RecurringTask import RecurringTask
from RecurringTaskInstance import RecurringTaskInstance
from Task import Task
from TransientTask import TransientTask
from exceptions import TaskNameNotUniqueError, TaskOverlapError, NoAntiTaskMatchError, PSSError, \
    PSSNoExistingTaskMatchError, TaskInsertionError, PSSInvalidOperationError


def generate_anti_tasks(recurring_tasks: List[RecurringTask]) -> List[AntiTask]:
    return [AntiTask.from_recurring_task(recurring_task, cancellation) for recurring_task in recurring_tasks for
            cancellation in recurring_task.cancellations]


class TaskCollectionModel:
    def __init__(self):
        self.transient_tasks: List[TransientTask] = []
        self.recurring_tasks: List[RecurringTask] = []

    def get_all_cancellations(self):
        return [cancellation for recurring_task in self.recurring_tasks
                          for cancellation in recurring_task.cancellations]

    def check_name_uniqueness(self, task_name: str):

        existing_names = [task.name for task in self.transient_tasks + self.recurring_tasks ] \
                         + [cancellation.name for cancellation in self.get_all_cancellations()]
        if task_name in existing_names:
            raise TaskNameNotUniqueError(f'Task with name {task_name} already exists')

    def check_for_overlap_with_existing_task(self, new_task: Task):
        existing_tasks = self.transient_tasks + [instance for recurring_task in self.recurring_tasks for instance in
                                                 RecurringTaskInstance.generate_instances(recurring_task)]
        new_task_instances = RecurringTaskInstance.generate_instances(
            new_task) if new_task.__class__ == RecurringTask else [new_task, ]
        for new_task_instance in new_task_instances:
            if any([True for existing_task in existing_tasks if new_task_instance.overlaps(existing_task)]):
                raise TaskOverlapError(f'New task overlaps existing task')

    def get_task_by_name(self, target_task_name: str):
        try:
            return filter(lambda task: task.name == target_task_name,
                          self.transient_tasks + self.recurring_tasks).__next__()
        except StopIteration:
            raise PSSNoExistingTaskMatchError(f'No task with name {target_task_name} exists in records.')

    def add_task(self, task: Task):
        if task.__class__ == AntiTask:
            self.add_cancellation(task)
            return

        self.check_name_uniqueness(task.name)
        self.check_for_overlap_with_existing_task(task)

        if task.__class__ == TransientTask:
            self.transient_tasks.append(task)
        elif task.__class__ == RecurringTask:
            self.recurring_tasks.append(task)
        else:
            raise RuntimeError(f'Unrecognised task class {task.__class__} in TaskCollectionModel::add_task()')

    def add_cancellation(self, anti_task: AntiTask):
        try:
            self.check_name_uniqueness(anti_task.name)
            matching_task = next(
                filter(lambda recurring_task: anti_task.matches(recurring_task), self.recurring_tasks))
        except StopIteration:
            raise NoAntiTaskMatchError(
                f'No task matching Antitask with start={anti_task.start}, duration={anti_task.duration_minutes}min')

        matching_task.add_cancellation(Cancellation(anti_task.start.date(), anti_task.name))

    def remove_task(self, task: Task):
        if task.__class__ == AntiTask:
            self.remove_cancellation(task)

        if task.__class__ == TransientTask:
            tasks_to_search = self.transient_tasks
        elif task.__class__ == RecurringTask:
            tasks_to_search = self.recurring_tasks
        else:
            raise PSSError(f'Unrecognised Task subclass {task.__class__}')

        try:
            matching_task = next(filter(lambda existing_task: existing_task.name == task.name, tasks_to_search))
            tasks_to_search.remove(matching_task)
        except StopIteration:
            raise PSSNoExistingTaskMatchError('FLESH THIS MESSAGE OUT LATER IF NECESSARY. IT SHOULD NEVER RAISE')

    def remove_cancellation(self, cancellation_name: str):
        def contains_cancellation_with_name(task: RecurringTask, name: str):
            return len(list(filter(lambda cancellation: cancellation.name == cancellation_name, task.cancellations)))

        matching_task = next(
            filter(lambda task: contains_cancellation_with_name(task, cancellation_name), self.recurring_tasks))
        matching_cancellation = next(
            filter(lambda cancellation: cancellation.name == cancellation_name, matching_task.cancellations))
        matching_task.remove_cancellation(matching_cancellation.date)

    def import_tasks_from_file(self, **kwargs):
        filename = kwargs.get('filename', 'schedule.json')
        revert_changes_on_error = kwargs.get('revert_changes_on_error', True)
        file_handler = FileHandler(filename)
        transient_task_backup = copy.deepcopy(self.transient_tasks)
        recurring_task_backup = copy.deepcopy(self.recurring_tasks)

        try:
            for task in file_handler.read_tasks():
                try:
                    self.add_task(task)
                except TaskInsertionError as err:
                    if revert_changes_on_error:
                        raise PSSInvalidOperationError()
        except PSSInvalidOperationError:
            # Revert changes if revert_changes_on_error
            self.transient_tasks = transient_task_backup
            self.recurring_tasks = recurring_task_backup

        recurring_tasks_by_name = {}
        recurring_tasks_by_name.update([(task.name, task) for task in self.recurring_tasks])

    def save(self, **kwargs):
        filename = kwargs.get('filename', 'schedule.json')
        file_handler = FileHandler(filename)
        tasks = self.transient_tasks + self.recurring_tasks + generate_anti_tasks(self.recurring_tasks)
        file_handler.write_tasks(tasks)

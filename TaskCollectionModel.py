import copy
from typing import List

from AntiTask import AntiTask
from FileHandler import FileHandler
from RecurringTask import RecurringTask
from RecurringTaskInstance import RecurringTaskInstance
from Task import Task
from TaskInstance import TaskInstance
from TransientTask import TransientTask
from exceptions import TaskNameNotUniqueError, TaskOverlapError, NoAntiTaskMatchError, PSSError, \
    PSSNoExistingTaskMatchError, TaskInsertionError, PSSInvalidOperationError


def generate_anti_tasks(recurring_tasks: List[RecurringTask]) -> List[AntiTask]:
    return [anti_task for recurring_task in recurring_tasks for
            anti_task in recurring_task.cancellations]


class TaskCollectionModel:
    def __init__(self):
        self.transient_tasks: List[TransientTask] = []
        self.recurring_tasks: List[RecurringTask] = []

    def get_all_anti_tasks(self):
        return [cancellation for recurring_task in self.recurring_tasks
                          for cancellation in recurring_task.cancellations]

    def get_recurring_task_instances(self) -> List[RecurringTaskInstance]:
        return [instance for recurring_task in self.recurring_tasks for instance in RecurringTaskInstance.generate_instances(recurring_task)]

    def get_task_instances(self) -> List[TaskInstance]:
        return self.transient_tasks + self.get_recurring_task_instances()

    def check_name_uniqueness(self, task_name: str):

        existing_names = [task.name for task in self.transient_tasks + self.recurring_tasks ] \
                         + [cancellation.name for cancellation in self.get_all_anti_tasks()]
        if task_name in existing_names:
            raise TaskNameNotUniqueError(f'Task with name {task_name} already exists')

    def check_for_overlap_with_existing_task(self, new_task: Task):
        existing_tasks = self.get_task_instances()
        new_task_instances = RecurringTaskInstance.generate_instances(
            new_task) if new_task.__class__ == RecurringTask else [new_task, ]
        for new_task_instance in new_task_instances:
            if any([True for existing_task in existing_tasks if new_task_instance.overlaps(existing_task)]):
                raise TaskOverlapError(f'New task overlaps existing task')

    def get_task_by_name(self, target_task_name: str):
        try:
            return filter(lambda task: task.name == target_task_name,
                          self.transient_tasks + self.recurring_tasks + self.get_all_anti_tasks()).__next__()
        except StopIteration:
            raise PSSNoExistingTaskMatchError(f'No task with name {target_task_name} exists in records.')

    def add_task(self, task: Task):
        if task.__class__ == AntiTask:
            self.add_anti_task(task)
            return

        self.check_name_uniqueness(task.name)
        self.check_for_overlap_with_existing_task(task)

        if task.__class__ == TransientTask:
            self.transient_tasks.append(task)
        elif task.__class__ == RecurringTask:
            self.recurring_tasks.append(task)
        else:
            raise RuntimeError(f'Unrecognised task class {task.__class__} in TaskCollectionModel::add_task()')

    def add_anti_task(self, anti_task: AntiTask):
        try:
            self.check_name_uniqueness(anti_task.name)
            matching_recurring_task = next(
                filter(lambda recurring_task: anti_task.matches(recurring_task), self.recurring_tasks))
        except StopIteration:
            raise NoAntiTaskMatchError(
                f'No task matching Antitask with start={anti_task.start}, duration={anti_task.duration_minutes}min')

        matching_recurring_task.add_anti_task(anti_task)

    def get_recurring_task_having_anti_task(self, anti_task: AntiTask):
        return next(filter(lambda recurring_task: recurring_task.has_cancellation_with_name(anti_task.name),
                           self.recurring_tasks))

    def remove_task(self, task: Task):
        if task.__class__ == AntiTask:
            self.remove_anti_task(task)
            return

        if task.__class__ == TransientTask:
            task_collection = self.transient_tasks
        elif task.__class__ == RecurringTask:
            task_collection = self.recurring_tasks
        else:
            raise PSSError(f'Unrecognised Task subclass {task.__class__}')

        try:
            matching_task = next(filter(lambda existing_task: existing_task.name == task.name, task_collection))
            task_collection.remove(matching_task)
        except StopIteration:
            raise PSSNoExistingTaskMatchError('FLESH THIS MESSAGE OUT LATER IF NECESSARY. IT SHOULD NEVER RAISE')

    def remove_anti_task(self, anti_task: AntiTask, parent_task: RecurringTask=None):
        removal_conflicts_with_task = anti_task.find_overlapping_task(self.get_task_instances())
        if removal_conflicts_with_task is not None:
            raise PSSInvalidOperationError(f'AntiTask {anti_task.name} overlaps with {removal_conflicts_with_task}')

        matching_task = parent_task if parent_task is not None else self.get_recurring_task_having_anti_task(anti_task)

        matching_anti_task = next(
            filter(lambda candidate_anti_task: candidate_anti_task.name == anti_task.name, matching_task.cancellations))

        matching_task.remove_cancellation(matching_anti_task)

    def import_task_data_from_file(self, **kwargs):
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

    def write_task_data_to_file(self, **kwargs):
        filename = kwargs.get('filename', 'schedule.json')
        file_handler = FileHandler(filename)
        tasks = self.transient_tasks + self.recurring_tasks + generate_anti_tasks(self.recurring_tasks)
        file_handler.write_tasks(tasks)

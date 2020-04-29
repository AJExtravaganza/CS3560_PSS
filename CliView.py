from typing import List, Union

from RecurringTask import RecurringTask
from RecurringTaskInstance import RecurringTaskInstance
from Task import Task
from TransientTask import TransientTask


class CliView:

    @classmethod
    def display_notification(cls, message: str):
        print(message)

    @classmethod
    def display_menu(cls, menu):
        if menu.prompt is not None:
            print(menu.prompt)

        for idx, item in enumerate(menu.items):
            print(f'{idx}) {item}')

    @classmethod
    def display_task(cls, task: Task, preamble=None):
        if preamble is not None:
            print(preamble)
        for key, value in task.as_ordered_dict().items():
            print(f'{key}: {value}')
        if type(task) is RecurringTask:
            print(
                f"Cancellations: {[int(cancellation.start.date().strftime('%Y%m%d')) for cancellation in task.cancellations]}")

    @classmethod
    def display_task_as_schedule_entry(cls, task: Union[TransientTask, RecurringTaskInstance], prefix: str = ''):
        print(f'{prefix}{task.start.strftime("%H:%M")}-{task.end().strftime("%H:%M")}: {task.name} [{task.type}]')

    @classmethod
    def display_schedule_chunk(cls, tasks: List[Union[TransientTask, RecurringTaskInstance]], preamble=None):
        if preamble is not None:
            print(preamble)
        for task in tasks:
            cls.display_task_as_schedule_entry(task)

    @classmethod
    def display_exception(cls, err: Exception):
        print(f'Error: {err}')

    @classmethod
    def display_invalid_selection_error(cls):
        print('Invalid selection.')

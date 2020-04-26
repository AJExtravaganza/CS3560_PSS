from RecurringTask import RecurringTask
from Task import Task


class CliView:
    @classmethod
    def display_menu(cls, menu):
        if menu.prompt is not None:
            print(menu.prompt)

        for idx, item in enumerate(menu.items):
            print(f'{idx}) {item}')

    @classmethod
    def display_task(cls, task: Task):
        for key, value in task.as_ordered_dict().items():
            print(f'{key}: {value}')
        if type(task) is RecurringTask:
            print(f"Cancellations: {[int(cancellation.strftime('%Y%m%d')) for cancellation in task.cancellations]}")


    @classmethod
    def display_exception(cls, err: Exception):
        print(f'Error: {err}')

    @classmethod
    def display_invalid_selection_error(cls):
        print('Invalid selection.')
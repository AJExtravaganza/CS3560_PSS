from typing import Type

from AntiTask import AntiTask
from CliController import CliController
from CliView import CliView
from Menu import Menu
from MenuItem import MenuItem
from RecurringTask import RecurringTask
from Task import Task
from TaskCollectionModel import TaskCollectionModel
from TransientTask import TransientTask
from exceptions import PSSValidationError, PSSInvalidOperationError


class CreateTaskMenuItem(MenuItem):
    def __init__(self, model: TaskCollectionModel):
        self.model = model
        super().__init__('Create Task', self.create_task_through_ui)

    def create_task_through_ui(self):
        task_create_type: Type[Task] = Menu(
            [
                MenuItem('Transient Task', lambda: TransientTask),
                MenuItem('Recurring Task', lambda: RecurringTask),
                MenuItem('Cancellation', lambda: AntiTask)
            ],
            'What type of task would you like to create?',
        ).process()

        if Task not in type.mro(task_create_type):
            raise RuntimeError('Invalid task type resulting from CreateTaskMenuItem.create_task_through_ui()')

        fields = task_create_type.get_input_fields()
        CliController.populate_fields(fields)
        field_values = CliController.fields_as_dict(fields)

        task = task_create_type(field_values)
        try:
            self.model.add_task(task)
        except PSSValidationError as err:
            raise PSSInvalidOperationError(f'Could not complete operation: {err}')

        CliView.display_notification(f'Successfully added {task}')

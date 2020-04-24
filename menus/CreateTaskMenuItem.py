from typing import Type

from AntiTask import AntiTask
from Menu import Menu
from MenuItem import MenuItem
from RecurringTask import RecurringTask
from Task import Task
from TaskCollectionModel import TaskCollectionModel
from TransientTask import TransientTask
from exceptions import PSSValidationError, PSSInvalidOperationError
from ui_helpers import fields_as_dict, populate_fields


class CreateTaskMenuItem(MenuItem):
    on_select = 'something'

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

        if not task_create_type.__base__ == Task:
            raise RuntimeError('Invalid task type resulting from CreateTaskMenuItem.create_task_through_ui()')

        fields = task_create_type.get_input_fields()
        populate_fields(fields)
        field_values = fields_as_dict(fields)

        task = task_create_type(field_values)
        try:
            self.model.add_task(task)
        except PSSValidationError as err:
            raise PSSInvalidOperationError(f'Could not complete operation: {err}')

        print(f'Successfully added {task}')

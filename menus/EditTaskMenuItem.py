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
from exceptions import PSSValidationError, PSSInvalidOperationError, PSSNoExistingTaskMatchError


class EditTaskMenuItem(MenuItem):
    def __init__(self, model: TaskCollectionModel):
        self.model = model
        super().__init__('Edit Task', self.edit_task_through_ui)

    def edit_task_through_ui(self):

        def anti_tasks_invalidated(task_before_changes: RecurringTask, task_after_changes: RecurringTask):
            return task_before_changes.start != task_after_changes.start \
                   or task_before_changes.frequency != task_after_changes.frequency

        CliView.display_notification('Please choose a task.')
        task_name_field = filter(lambda field: field.name == 'Name', Task.get_input_fields()).__next__()
        CliController.populate_field(task_name_field)

        try:
            existing_task = self.model.get_task_by_name(task_name_field.value)
            CliView.display_task(existing_task, 'Current details:')

            TaskType = type(existing_task)
            fields = TaskType.get_input_fields()
            CliController.populate_fields(fields, allow_blank=True)

            field_values = existing_task.as_dict()
            field_values.update(CliController.fields_as_dict(fields))

            updated_task = TaskType(field_values)
            if TaskType == RecurringTask:
                if anti_tasks_invalidated(existing_task, updated_task):
                    CliView.display_notification('Cancellations could not be retained and will need to be re-entered.')
                else:
                    updated_task.cancellations = existing_task.cancellations

            self.model.remove_task(existing_task)
            try:
                self.model.add_task(updated_task)
            except PSSValidationError as err:
                # Restore existing_task
                self.model.add_task(existing_task)
                raise PSSInvalidOperationError(f'Could not edit details for task  "{existing_task.name}": {err}')

            CliView.display_notification(f'Successfully updated {existing_task}')

        except PSSNoExistingTaskMatchError as err:
            raise PSSInvalidOperationError(f'Cannot find task with name "{task_name_field.value}": {err}')
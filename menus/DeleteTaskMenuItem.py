from CliController import CliController
from MenuItem import MenuItem
from Task import Task
from TaskCollectionModel import TaskCollectionModel
from exceptions import PSSInvalidOperationError


class DeleteTaskMenuItem(MenuItem):
    def __init__(self, model: TaskCollectionModel):
        self.model = model
        super().__init__('Delete Task By Name', self.find_and_display_task_through_ui)

    def find_and_display_task_through_ui(self):
        task_name_field = filter(lambda field: field.name == 'Name', Task.get_input_fields()).__next__()
        CliController.populate_field(task_name_field)

        try:
            task = self.model.get_task_by_name(task_name_field.value)
            self.model.remove_task(task)
        except PSSInvalidOperationError as err:
            raise PSSInvalidOperationError(f'Could not delete task: {err}')


from CliController import CliController
from CliView import CliView
from MenuItem import MenuItem
from Task import Task
from TaskCollectionModel import TaskCollectionModel
from exceptions import PSSValidationError, PSSInvalidOperationError, PSSNoExistingTaskMatchError


class ViewTaskMenuItem(MenuItem):
    on_select = 'something'

    def __init__(self, model: TaskCollectionModel):
        self.model = model
        super().__init__('Search Task By Name', self.find_and_display_task_through_ui)

    def find_and_display_task_through_ui(self):
        task_name_field = filter(lambda field: field.name == 'Name', Task.get_input_fields()).__next__()
        CliController.populate_field(task_name_field)

        try:
            task = self.model.get_task_by_name(task_name_field.value)
            CliView.display_task(task)
        except PSSNoExistingTaskMatchError as err:
            raise PSSInvalidOperationError(f'Cannot find task with name "{task_name_field.value}": {err}')


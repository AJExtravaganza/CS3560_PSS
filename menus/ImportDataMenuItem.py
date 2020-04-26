from CliController import CliController
from CliView import CliView
from Field import Field
from MenuItem import MenuItem
from TaskCollectionModel import TaskCollectionModel
from exceptions import PSSInvalidOperationError


class ImportDataMenuItem(MenuItem):
    def __init__(self, model: TaskCollectionModel):
        self.model = model
        super().__init__('Import Data From File', self.import_data, )

    def import_data(self):
        filename_field = Field('filename', 'filename',)
        CliController.populate_field(filename_field)

        try:
            self.model.import_task_data_from_file(filename=filename_field.value)
            CliView.display_notification(f'Successfully imported task data from {filename_field.value}')
        except Exception as err:
            raise PSSInvalidOperationError(f'Cannot read valid data from "{filename_field.value}": {err}')

from CliController import CliController
from CliView import CliView
from Field import Field
from MenuItem import MenuItem
from TaskCollectionModel import TaskCollectionModel
from exceptions import PSSInvalidOperationError


class ExportDataMenuItem(MenuItem):
    def __init__(self, model: TaskCollectionModel):
        self.model = model
        super().__init__('Export Data To File', self.save_schedule, )

    def save_schedule(self):
        filename_field = Field('filename', 'filename',)
        CliController.populate_field(filename_field)

        try:
            self.model.save(filename=filename_field.value)
            CliView.display_notification(f'Successfully saved task data to {filename_field.value}')
        except Exception as err:
            raise PSSInvalidOperationError(f'Cannot write to file "{filename_field.value}": {err}')

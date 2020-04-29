from datetime import datetime
from typing import Type, Union, List

from CliController import CliController
from CliView import CliView
from Field import Field
from Menu import Menu
from MenuItem import MenuItem
from ScheduleView import ScheduleView
from TaskCollectionModel import TaskCollectionModel
from exceptions import PSSInvalidOperationError
from field_validators import validate_date_string, validate_data_filename


class ExportScheduleMenuItem(MenuItem):
    def __init__(self, model: TaskCollectionModel):
        self.model = model
        super().__init__('Write Schedule To File', self.write_schedule_through_ui)

    def write_schedule_through_ui(self):
        get_schedule_task_instances = Menu(
            [
                MenuItem('Daily Schedule', lambda : lambda start_date: self.model.get_task_instances_for_date(start_date)),
                MenuItem('Weekly Schedule', lambda : lambda start_date: self.model.get_task_instances_for_week_starting(start_date)),
                MenuItem('Monthly Schedule', lambda : lambda start_date: self.model.get_task_instances_for_month(start_date))
            ],
            'What type of schedule would you like to write?',
        ).process()

        start_date_field = Field(
            'StartDate',
            'Start Date',
            validate_date_string,
            "Must be a date in form YYYYMMDD",
            lambda start_date_string: datetime.strptime(start_date_string, '%Y%m%d').date()
        )


        filename_field = Field(
            'Filename',
            'filename',
            validate_data_filename,
        )

        try:
            CliController.populate_fields([start_date_field, filename_field])
            task_instances = get_schedule_task_instances(start_date_field.value)
            self.model.write_task_instances_to_file(filename=filename_field.value, task_instances=task_instances)
            CliView.display_notification(f'Exported schedule to "{filename_field.value}"')
        except Exception as err:
            raise PSSInvalidOperationError(f'Failed to export schedule: {err}')


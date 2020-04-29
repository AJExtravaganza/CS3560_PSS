from datetime import datetime
from typing import Type, Union, List

from CliController import CliController
from Field import Field
from Menu import Menu
from MenuItem import MenuItem
from ScheduleView import ScheduleView
from TaskCollectionModel import TaskCollectionModel
from field_validators import validate_date_string


class ViewScheduleMenuItem(MenuItem):
    def __init__(self, model: TaskCollectionModel):
        self.model = model
        super().__init__('View Schedule', self.view_schedule_through_ui)

    def view_schedule_through_ui(self):
        get_schedule_tasks = Menu(
            [
                MenuItem('Daily Schedule', lambda : lambda start_date: self.model.get_task_instances_for_date(start_date)),
                MenuItem('Weekly Schedule', lambda : lambda start_date: self.model.get_task_instances_for_week_starting(start_date)),
                MenuItem('Monthly Schedule', lambda : lambda start_date: self.model.get_task_instances_for_month(start_date))
            ],
            'What type of schedule would you like to view?',
        ).process()
        start_date_field = Field(
            'StartDate',
            'Start Date',
            validate_date_string,
            "Must be a date in form YYYYMMDD",
            lambda start_date_string: datetime.strptime(start_date_string, '%Y%m%d').date()
        )
        CliController.populate_field(start_date_field)

        tasks = get_schedule_tasks(start_date_field.value)
        view = ScheduleView(tasks)
        view.display()

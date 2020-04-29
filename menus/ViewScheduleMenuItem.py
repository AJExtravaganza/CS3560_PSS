from datetime import datetime
from typing import Type, Union

from CliController import CliController
from DailyScheduleView import DailyScheduleView
from Field import Field
from Menu import Menu
from MenuItem import MenuItem
from MonthlyScheduleView import MonthlyScheduleView
from Task import Task
from TaskCollectionModel import TaskCollectionModel
from WeeklyScheduleView import WeeklyScheduleView
from field_validators import validate_date_string


class ViewScheduleMenuItem(MenuItem):
    def __init__(self, model: TaskCollectionModel):
        self.model = model
        super().__init__('View Schedule', self.view_schedule_through_ui)

    def view_schedule_through_ui(self):
        ScheduleViewType: Type[Union[DailyScheduleView,]] = Menu(
            [
                MenuItem('Daily Schedule', lambda: DailyScheduleView),
                MenuItem('Weekly Schedule', lambda: WeeklyScheduleView),
                MenuItem('Monthly Schedule', lambda: MonthlyScheduleView)
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

        view = ScheduleViewType(self.model.get_task_instances(), start_date_field.value)
        view.display()

from Menu import Menu
from TaskCollectionModel import TaskCollectionModel
from menus.CreateTaskMenuItem import CreateTaskMenuItem


class MainMenu(Menu):
    def __init__(self, model: TaskCollectionModel):
        self.model = model
        super().__init__([
            CreateTaskMenuItem(model),
            # ViewTaskMenuItem,
            # DeleteTaskMenuItem,
            # EditTaskMenuItem,
            # SaveScheduleMenuItem,
            # LoadScheduleMenuItem,
            # ViewScheduleMenuItem,
            # ExportScheduleMenuItem,
        ])

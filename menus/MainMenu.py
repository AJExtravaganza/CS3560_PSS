from Menu import Menu
from TaskCollectionModel import TaskCollectionModel
from menus.CreateTaskMenuItem import CreateTaskMenuItem
from menus.DeleteTaskMenuItem import DeleteTaskMenuItem
from menus.ViewTaskMenuItem import ViewTaskMenuItem


class MainMenu(Menu):
    def __init__(self, model: TaskCollectionModel):
        self.model = model
        super().__init__([
            CreateTaskMenuItem(model),
            ViewTaskMenuItem(model),
            DeleteTaskMenuItem(model),
            # EditTaskMenuItem,
            # SaveScheduleMenuItem,
            # LoadScheduleMenuItem,
            # ViewScheduleMenuItem,
            # ExportScheduleMenuItem,
        ])

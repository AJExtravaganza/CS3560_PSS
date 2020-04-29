from Menu import Menu
from TaskCollectionModel import TaskCollectionModel
from menus.CreateTaskMenuItem import CreateTaskMenuItem
from menus.DeleteTaskMenuItem import DeleteTaskMenuItem
from menus.EditTaskMenuItem import EditTaskMenuItem
from menus.ExportDataMenuItem import ExportDataMenuItem
from menus.ImportDataMenuItem import ImportDataMenuItem
from menus.ViewScheduleMenuItem import ViewScheduleMenuItem
from menus.ViewTaskMenuItem import ViewTaskMenuItem


class MainMenu(Menu):
    def __init__(self, model: TaskCollectionModel):
        self.model = model
        super().__init__([
            CreateTaskMenuItem(model),
            ViewTaskMenuItem(model),
            DeleteTaskMenuItem(model),
            EditTaskMenuItem(model),
            ExportDataMenuItem(model),
            ImportDataMenuItem(model),
            ViewScheduleMenuItem(model),
            # ExportScheduleMenuItem,
        ])

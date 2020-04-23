from TaskCollectionModel import TaskCollectionModel
from menus.main_menu import MainMenu

model = TaskCollectionModel()
user_has_requested_exit = False
main_menu = MainMenu(model)
while not user_has_requested_exit:
    main_menu.process()
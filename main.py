from TaskCollectionModel import TaskCollectionModel
from exceptions import PSSError
from menus.MainMenu import MainMenu

model = TaskCollectionModel()
user_has_requested_exit = False
main_menu = MainMenu(model)
while not user_has_requested_exit:
    try:
        main_menu.process()
    except PSSError as err:
        print(err)
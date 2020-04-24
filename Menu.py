from typing import List

from MenuItem import MenuItem
from MenuView import MenuView
from exceptions import PSSError, PSSInvalidOperationError


class InvalidUserMenuSelectionError(ValueError):
    pass

class Menu:
    def __init__(self, items: List[MenuItem], prompt: str = None):
        self.items = items
        self.prompt = prompt

    def process(self):
        view = MenuView(self.items, self.prompt)
        view.display()

        selection = None
        while selection is None:
            try:
                selection = self.get_user_selection()
            except InvalidUserMenuSelectionError:
                view.display_invalid_selection_error()

        try:
            return self.items[selection].process()
        except PSSInvalidOperationError as err:
            view.display_exception(err)

    def get_user_selection(self) -> int:
        def valid_selection(raw_selection: int):
            lower_selection_bound = 0
            upper_selection_bound = len(self.items) - 1
            return lower_selection_bound <= raw_selection <= upper_selection_bound

        try:
            selection = int(input('Please make a selection: '))
            if not valid_selection(selection):
                raise ValueError
        except ValueError:
            raise InvalidUserMenuSelectionError()

        return selection

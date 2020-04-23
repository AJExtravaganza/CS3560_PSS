from typing import List

from MenuItem import MenuItem


class MenuView:
    def __init__(self, items: List[MenuItem], prompt:str = None):
        self.items = items
        self.prompt = prompt

    def display(self):
        if self.prompt is not None:
            print(self.prompt)

        for idx, item in enumerate(self.items):
            print(f'{idx}) {item}')

        print('Please make a selection: ')

    def display_invalid_selection_error(self):
        print('Invalid selection.')

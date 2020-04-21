from typing import List

from MenuItem import MenuItem


class Menu:
    def __init__(self, items: List[MenuItem]):
        self.items = items

    def display(self):
        def valid_selection(raw_selection: int):
            lower_selection_bound = 0
            upper_selection_bound = len(self.items) - 1
            return lower_selection_bound <= raw_selection <= upper_selection_bound

        for idx, item in enumerate(self.items):
            print(f'{idx}) {item}')

        selection = None
        while selection is None:
            try:
                rawSelection = int(input('Please make a selection'))
                if valid_selection(rawSelection):
                    selection = rawSelection
                else:
                    raise ValueError
            except ValueError:
                print('Invalid selection.')

        self.items[selection].do()

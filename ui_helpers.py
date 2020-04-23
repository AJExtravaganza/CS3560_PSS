from typing import List

from Field import Field


def populate_fields_with_user_input(fields: List[Field]):
    for field in fields:
        while field.value is None:
            try:
                field.set(input(f'Enter value for {field.name}'))
            except ValueError as err:
                print(err)
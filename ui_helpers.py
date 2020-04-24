from typing import List

from Field import Field


# TODO: This breaks MVC - figure out how to fix this
def populate_fields(fields: List[Field]):
    for field in fields:
        while field.value is None:
            try:
                field.set(input(f'Enter value for {field.name}: '))
            except ValueError as err:
                print(err)
    

def fields_as_dict(fields: List[Field]) -> dict:
    result = {}
    for field in fields:
        result.update({field.name: field.value})
    
    return result
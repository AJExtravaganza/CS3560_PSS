from typing import List

from Field import Field


class CliController:

    @staticmethod
    def populate_field(field: Field, **kwargs):
        allow_blank = kwargs.get('allow_blank', False)

        while field.value is None:
            try:
                raw_input = input(f'Enter value for {field.name}: ')
                if allow_blank and raw_input == '':
                    return

                field.set(raw_input)
            except ValueError as err:
                print(err)

    @staticmethod
    def populate_fields(fields: List[Field], **kwargs):
        allow_blank = kwargs.get('allow_blank', False)

        for field in fields:
            CliController.populate_field(field, allow_blank=allow_blank)

    @staticmethod
    def fields_as_dict(fields: List[Field]) -> dict:
        result = {}
        for field in fields :
            if field.value is not None:
                result.update({field.name: field.value})

        return result

class Field:
    def __init__(self, name: str, display_name: str, validator=None, validation_pattern_message=None):
        self.name = name
        self.display_name = display_name
        self.validator = validator
        self.validation_pattern_message = validation_pattern_message
        self.value = None

    def set(self, value):
        try:
            self.validator(value)
            self.value = value
        except ValueError:
            raise ValueError(f'Value {value} does not conform to {self.validation_pattern_message}')


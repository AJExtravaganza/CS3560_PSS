from typing import List

from Field import Field
from Task import Task


class TransientTask(Task):
    valid_types = {
        'Visit',
        'Shopping',
        'Appointment',
    }

    @classmethod
    def get_input_fields(cls) -> List[Field]:
        return super().get_input_fields()

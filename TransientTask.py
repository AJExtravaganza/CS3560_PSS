from Task import Task


class TransientTask(Task):
    valid_types = {
        'Visit',
        'Shopping',
        'Appointment',
    }

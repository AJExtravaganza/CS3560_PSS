from Task import Task


class RecurringTaskInstance(Task):
    valid_types = {
        'Class',
        'Study',
        'Sleep',
        'Exercise',
        'Work',
        'Meal',
    }
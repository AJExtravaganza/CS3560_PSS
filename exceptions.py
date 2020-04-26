# Exceptions arising from expected exceptional behaviour when attempting to perform PSS-specific operations
class PSSError(Exception):
    pass


class PSSInvalidOperationError(PSSError):
    pass


class PSSValidationError(PSSError):
    pass


class InvalidJsonTaskDefinition(PSSValidationError):
    pass


class TaskInsertionError(PSSValidationError):
    pass


class TaskNameNotUniqueError(TaskInsertionError):
    pass


class TaskOverlapError(TaskInsertionError):
    pass


class NoAntiTaskMatchError(TaskInsertionError):
    pass


class PSSNoExistingTaskMatchError(PSSValidationError):
    pass

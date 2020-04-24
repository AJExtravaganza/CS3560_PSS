from AntiTask import AntiTask
from RecurringTask import RecurringTask
from Task import Task
from TransientTask import TransientTask
from exceptions import InvalidJsonTaskDefinition


class TaskFactory:
    @staticmethod
    def from_dict(json: dict) -> Task:
        try:
            if json['Type'] in TransientTask.valid_types:
                return TransientTask(json)
            elif json['Type'] in RecurringTask.valid_types:
                return RecurringTask(json)
            elif json['Type'] in AntiTask.valid_types:
                return AntiTask(json)
            else:
                raise InvalidJsonTaskDefinition()
        except KeyError:
            raise InvalidJsonTaskDefinition('Task definition lacks required key "Type"')

import json
from typing import List

from Task import Task
from TaskFactory import TaskFactory


class FileHandler:
    def __init__(self, filename):
        self.filename = filename

    def read_tasks(self) -> List[Task]:
        with open(self.filename, 'r') as input_file:
            data = input_file.read()

        records = json.loads(data)['tasks']

        return [TaskFactory.from_dict(record) for record in records]

    def write_tasks(self, tasks: List[Task]):
        with open(self.filename, 'w') as output_file:
            output_file.write(json.dumps({
                'tasks': [task.as_dict() for task in tasks]
            }))

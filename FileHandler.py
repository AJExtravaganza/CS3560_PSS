import json
from typing import List

from Task import Task
from TaskFactory import TaskFactory


class FileHandler:
    def __init__(self, filename = 'schedule.json'):
        self.filename = filename

    def read_tasks(self) -> List[Task]:
        with open(self.filename, 'r') as input_file:
            data = input_file.read()

        records = json.loads(data)['tasks']

        return [TaskFactory.from_dict(record) for record in records]

import json
from datetime import datetime

from AntiTask import AntiTask
from FileHandler import FileHandler
from RecurringTask import RecurringTask
from TaskCollectionModel import TaskCollectionModel
from TransientTask import TransientTask


def test_equal(value, expected):
    try:
        assert value == expected
    except AssertionError as err:
        raise AssertionError(f'{err} Expected {expected}, got {value}')


class Tests():
    @staticmethod
    def test_input_file_parse():
        file_handler = FileHandler('test_inputs/test_input_file_parse.json')
        tasks = file_handler.read_tasks()
        assert len(tasks) == 3

        transient_task = tasks[0]
        recurring_task = tasks[1]
        anti_task = tasks[2]

        test_equal(transient_task.__class__, TransientTask)
        test_equal(recurring_task.__class__, RecurringTask)
        test_equal(anti_task.__class__, AntiTask)

    @staticmethod
    def test_load_data():
        collection_model = TaskCollectionModel()
        collection_model.load(filename='test_inputs/test_input_file_parse.json')

        test_equal(len(collection_model.transient_tasks), 1)
        test_equal(len(collection_model.recurring_tasks), 1)
        test_equal(len(collection_model.recurring_tasks[0].cancellations), 1)
        test_equal(collection_model.recurring_tasks[0].generate_recurrence_datetimes(), [
            datetime(year=2020, month=1, day=31, hour=10),
            datetime(year=2020, month=2, day=29, hour=10),
            datetime(year=2020, month=3, day=31, hour=10),
        ])

    @staticmethod
    def test_output_file_write():
        _collection_model = TaskCollectionModel()
        _collection_model.load(filename='test_inputs/test_input_file_parse.json')
        _collection_model.save(filename='test_inputs/test_output_file_write.json')

        with open('test_inputs/test_input_file_parse.json', 'r') as input_file, \
                open('test_inputs/test_output_file_write.json', 'r') as output_file:
            input = json.loads(input_file.read())
            output = json.loads(output_file.read())
            test_equal(output['tasks'], input['tasks'])


Tests.test_input_file_parse()
Tests.test_load_data()
Tests.test_output_file_write()

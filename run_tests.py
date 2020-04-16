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


def test_load_data():
    collection_model = TaskCollectionModel()
    collection_model.load(filename='test_inputs/test_load_data.json')

    test_equal(len(collection_model.transient_tasks), 1)
    test_equal(len(collection_model.recurring_tasks), 1)
    test_equal(len(collection_model.recurring_tasks[0].cancellations), 1)
    test_equal(collection_model.recurring_tasks[0].generate_recurrences(), [
        datetime(year=2020, month=1, day=31, hour=10),
        datetime(year=2020, month=2, day=29, hour=10),
        datetime(year=2020, month=3, day=31, hour=10),
    ])


test_input_file_parse()
test_load_data()
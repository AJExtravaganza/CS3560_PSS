from AntiTask import AntiTask
from FileHandler import FileHandler
from RecurringTask import RecurringTask
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


test_input_file_parse()

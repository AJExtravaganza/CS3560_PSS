import json
from datetime import datetime, timedelta

from AntiTask import AntiTask
from FileHandler import FileHandler
from RecurringTask import RecurringTask
from RecurringTaskInstance import RecurringTaskInstance
from Task import Task
from TaskCollectionModel import TaskCollectionModel
from TransientTask import TransientTask


def test(expr: bool):
    try:
        assert expr == True
    except AssertionError as err:
        raise AssertionError(f'{err} Expected True, got {expr}')


def test_equal(value, expected):
    try:
        assert value == expected
    except AssertionError as err:
        raise AssertionError(f'{err} Expected {expected}, got {value}')


class Tests():
    @staticmethod
    def test_input_file_parse():
        file_handler = FileHandler('unit_test_inputs/test_input_file_parse.json')
        tasks = file_handler.read_tasks()
        assert len(tasks) == 3

        transient_task = tasks[0]
        recurring_task = tasks[1]
        anti_task = tasks[2]

        test_equal(transient_task.__class__, TransientTask)
        test_equal(recurring_task.__class__, RecurringTask)
        test_equal(anti_task.__class__, AntiTask)

    @staticmethod
    def test_add_tasks_to_model():
        collection_model = TaskCollectionModel()
        collection_model.import_tasks_from_file(
            filename='unit_test_inputs/test_input_file_parse.json',
            revert_changes_on_error=False)

        test_equal(len(collection_model.transient_tasks), 1)
        test_equal(len(collection_model.recurring_tasks), 1)
        test_equal(len(collection_model.recurring_tasks[0].cancellations), 1)
        test_equal(collection_model.recurring_tasks[0].generate_recurrence_datetimes(), [
            datetime(year=2020, month=1, day=31, hour=10),
            datetime(year=2020, month=2, day=29, hour=10),
        ])

    @staticmethod
    def test_recurring_task_instance_generation():
        collection_model = TaskCollectionModel()
        collection_model.import_tasks_from_file(
            filename='unit_test_inputs/test_recurring_task_instance_generation.json',
            revert_changes_on_error=False)

        daily_task = collection_model.recurring_tasks[0]
        weekly_task = collection_model.recurring_tasks[1]
        monthly_task = collection_model.recurring_tasks[2]

        daily_task_0_start = datetime(year=2020, month=1, day=1, hour=00)
        daily_task_1_start = datetime(year=2020, month=1, day=2, hour=00)

        weekly_task_0_start = datetime(year=2020, month=2, day=1, hour=00)
        weekly_task_1_start = datetime(year=2020, month=2, day=8, hour=00)

        monthly_task_0_start = datetime(year=2020, month=3, day=1, hour=00)
        monthly_task_1_start = datetime(year=2020, month=4, day=1, hour=00)

        test_equal(daily_task.generate_recurrence_datetimes(), [
            daily_task_0_start,
            daily_task_1_start
        ])
        test_equal(weekly_task.generate_recurrence_datetimes(), [
            weekly_task_0_start,
            weekly_task_1_start
        ])
        test_equal(monthly_task.generate_recurrence_datetimes(), [
            monthly_task_0_start,
            monthly_task_1_start
        ])

        test_equal(RecurringTaskInstance.generate_instances(daily_task)[0].start, daily_task_0_start)
        test_equal(RecurringTaskInstance.generate_instances(daily_task)[1].start, daily_task_1_start)
        test_equal(RecurringTaskInstance.generate_instances(weekly_task)[0].start, weekly_task_0_start)
        test_equal(RecurringTaskInstance.generate_instances(weekly_task)[1].start, weekly_task_1_start)
        test_equal(RecurringTaskInstance.generate_instances(monthly_task)[0].start, monthly_task_0_start)
        test_equal(RecurringTaskInstance.generate_instances(monthly_task)[1].start, monthly_task_1_start)

    @staticmethod
    def test_remove_tasks_from_model():
        collection_model = TaskCollectionModel()
        collection_model.import_tasks_from_file(
            filename='unit_test_inputs/test_input_file_parse.json',
            revert_changes_on_error=False)

        test_equal(len(collection_model.transient_tasks), 1)
        collection_model.remove_task(collection_model.transient_tasks[0])
        test_equal(len(collection_model.transient_tasks), 0)

        test_equal(len(collection_model.recurring_tasks), 1)
        test_equal(len(collection_model.recurring_tasks[0].cancellations), 1)
        recurring_task = collection_model.recurring_tasks[0]
        anti_task = AntiTask.from_recurring_task(recurring_task, recurring_task.cancellations[0])
        collection_model.remove_cancellation(anti_task.name)
        test_equal(len(collection_model.recurring_tasks[0].cancellations), 0)
        test_equal(collection_model.recurring_tasks[0].generate_recurrence_datetimes(), [
            datetime(year=2020, month=1, day=31, hour=10),
            datetime(year=2020, month=2, day=29, hour=10),
            datetime(year=2020, month=3, day=31, hour=10),
        ])

        collection_model.remove_task(collection_model.recurring_tasks[0])
        test_equal(len(collection_model.recurring_tasks), 0)

    @staticmethod
    def test_output_file_write():
        collection_model = TaskCollectionModel()
        collection_model.import_tasks_from_file(
            filename='unit_test_inputs/test_input_file_parse.json',
            revert_changes_on_error=False)
        collection_model.save(filename='unit_test_inputs/test_output_file_write.json')

        with open('unit_test_inputs/test_input_file_parse.json', 'r') as input_file, \
                open('unit_test_inputs/test_output_file_write.json', 'r') as output_file:
            input = json.loads(input_file.read())
            output = json.loads(output_file.read())
            test_equal(output['tasks'], input['tasks'])

    @staticmethod
    def test_name_conflict():
        collection_model = TaskCollectionModel()
        collection_model.import_tasks_from_file(
            filename='unit_test_inputs/test_name_conflict.json',
            revert_changes_on_error=False)
        test_equal(len(collection_model.transient_tasks), 1)
        test_equal(len(collection_model.recurring_tasks), 1)

    @staticmethod
    def test_task_overlap_detection():
        now = datetime.now()

        class TestStructure:
            def __init__(self, start_offset, end_offset):
                self.start = now + timedelta(minutes=start_offset)
                self.duration_minutes = start_offset + end_offset

        a = TestStructure(0, 5)
        b = TestStructure(2, 7)
        c = TestStructure(5, 10)

        test(Task.overlaps(a, b))
        test(Task.overlaps(b, a))
        test(Task.overlaps(b, c))
        test(Task.overlaps(c, b))
        test(not Task.overlaps(a, c))
        test(not Task.overlaps(c, a))

    @staticmethod
    def test_task_overlap_conflict():
        collection_model = TaskCollectionModel()
        collection_model.import_tasks_from_file(
            filename='unit_test_inputs/test_overlapping_tasks.json',
            revert_changes_on_error=False)
        test_equal(len(collection_model.transient_tasks), 1)
        test_equal(len(collection_model.recurring_tasks), 1)


Tests.test_input_file_parse()
Tests.test_add_tasks_to_model()
Tests.test_recurring_task_instance_generation()
Tests.test_remove_tasks_from_model()
Tests.test_output_file_write()
Tests.test_name_conflict()
Tests.test_task_overlap_detection()
Tests.test_task_overlap_conflict()

print('Unit tests complete')

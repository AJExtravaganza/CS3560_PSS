from AntiTask import AntiTask
from Menu import Menu
from MenuItem import MenuItem
from RecurringTask import RecurringTask
from TaskCollectionModel import TaskCollectionModel
from TransientTask import TransientTask


class CreateTaskMenuItem(MenuItem):
    on_select = 'something'

    def __init__(self, model: TaskCollectionModel):
        self.model = model
        super().__init__('Create Task', self.create_task_through_ui)

    def create_task_through_ui(self):
        task_create_type = Menu(
            [
                MenuItem('Transient Task', lambda: TransientTask),
                MenuItem('Recurring Task', lambda: RecurringTask),
                MenuItem('Cancellation', lambda: AntiTask)
            ],
            'What type of task would you like to create?',
        ).process()

        if task_create_type == TransientTask:
            self.create_transient_task_through_ui()
        elif task_create_type == RecurringTask:
            pass
            # self.create_recurring_task_through_ui()
        elif task_create_type == AntiTask:
            pass
            # self.create_cancellation_through_ui()
        else:
            raise RuntimeError('Invalid task type resulting from CreateTaskMenuItem.create_task_through_ui()')

    def create_transient_task_through_ui(self):
        pass

    def create_recurring_task_through_ui(self):
        pass

    def create_cancellation_task_through_ui(self):
        pass
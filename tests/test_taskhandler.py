import unittest
from unittest.mock import Mock, MagicMock
from datetime import datetime, timedelta
from task_handler import TaskHandler


class TestTaskHandler(unittest.TestCase):
    def setUp(self):
        self.bot = Mock()
        self.db = Mock()
        self.handler = TaskHandler(self.bot, self.db)

    def test_add_task(self):
        message = Mock()
        message.chat.id = 123
        self.bot.send_message.return_value = Mock()

        self.handler.add_task(message)

        self.bot.send_message.assert_called_once_with(123, "Введите задачу:")
        self.bot.register_next_step_handler.assert_called_once()

    def test_save_task(self):
        message = Mock()
        message.chat.id = 123
        message.text = "Test Task"
        self.db.add_task.return_value = None

        self.handler.save_task(message)

        self.db.add_task.assert_called_once()
        self.db.add_task.assert_called_with(self.handler.get_user_id(123), "Test Task")
        self.bot.send_message.assert_called_once_with(123, "Задача 'Test Task' добавлена!")

    def test_list_tasks_empty(self):
        message = Mock()
        message.chat.id = 123
        self.db.get_tasks.return_value = []

        self.handler.list_tasks(message)

        self.bot.send_message.assert_called_once_with(123, "Список задач пуст.")

    def test_list_tasks_with_data(self):
        message = Mock()
        message.chat.id = 123
        task = Mock(task="Test Task", task_id=1)
        self.db.get_tasks.return_value = [task]

        self.handler.list_tasks(message)

        self.bot.send_message.assert_called_once()
        self.assertIn("Список задач:", self.bot.send_message.call_args[0][1])

    def test_mark_task_done_no_tasks(self):
        message = Mock()
        message.chat.id = 123
        self.db.get_tasks.return_value = []

        self.handler.mark_task_done(message)

        self.bot.send_message.assert_called_once_with(123,
                                                      "Список задач пуст. Невозможно отметить задачу как выполненную.")

    def test_mark_task_done(self):
        message = Mock()
        message.chat.id = 123
        task = Mock(task="Test Task", task_id=1)
        self.db.get_tasks.return_value = [task]
        message.text = "1"

        self.handler.complete_task(message)

        self.db.mark_task_done.assert_called_once_with(1)
        self.bot.send_message.assert_called_once_with(123, "Задача 'Test Task' выполнена!")

    def test_set_reminder(self):
        message = Mock()
        message.chat.id = 123
        task = Mock(task="Test Task", task_id=1)
        self.db.get_tasks.return_value = [task]

        self.handler.set_reminder(message)

        self.bot.send_message.assert_called_once()
        self.bot.register_next_step_handler.assert_called_once()

    def test_schedule_reminder_valid_input(self):
        message = Mock()
        message.text = "1"
        task = Mock(task="Test Task", task_id=1)
        tasks = [task]
        self.handler.schedule_reminder(message, tasks)

        self.bot.send_message.assert_called_once_with(message.chat.id,
                                                      "Введите дату и время напоминания в формате 'YYYY-MM-DD HH:MM':")
        self.bot.register_next_step_handler.assert_called_once()

    def test_schedule_reminder_invalid_input(self):
        message = Mock()
        message.text = "1"
        task = Mock(task="Test Task", task_id=1)
        tasks = [task]

        self.handler.schedule_reminder(message, tasks)

        invalid_message = Mock()
        invalid_message.text = "invalid date"

        with self.assertRaises(ValueError):
            self.handler.set_reminder_time(invalid_message, task)

        self.bot.send_message.assert_called_with(invalid_message.chat.id,
                                                 "Пожалуйста, введите дату и время в правильном формате 'YYYY-MM-DD HH:MM'.")

    def test_delete_task(self):
        message = Mock()
        message.chat.id = 123
        task = Mock(task="Test Task", task_id=1)
        self.db.get_tasks.return_value = [task]
        message.text = "1"

        self.handler.remove_task(message)

        self.db.delete_task.assert_called_once_with(1)
        self.bot.send_message.assert_called_once_with(123, "Задача 'Test Task' удалена!")

    def test_delete_all_tasks(self):
        message = Mock()
        message.chat.id = 123
        self.handler.delete_all_tasks(message)

        self.db.delete_all_tasks.assert_called_once_with(self.handler.get_user_id(123))
        self.bot.send_message.assert_called_once_with(123, "Все задачи удалены!")


if __name__ == '__main__':
    unittest.main()



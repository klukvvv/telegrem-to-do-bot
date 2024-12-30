import unittest
from unittest.mock import MagicMock, patch
from bot import main, start_message, help_message, handle_add_task, handle_list_tasks, handle_mark_task_done, handle_set_reminder, handle_delete_task, handle_delete_all_tasks


class TestTelegramBot(unittest.TestCase):
    def setUp(self):
        self.logger_mock = MagicMock()
        self.bot_mock = MagicMock()
        self.db_mock = MagicMock()
        self.task_handler_mock = MagicMock()
        self.message_mock = MagicMock()

        # Патчим зависимости
        patch('bot.setup_logger', return_value=self.logger_mock).start()
        patch('bot.telebot.TeleBot', return_value=self.bot_mock).start()
        patch('bot.Database', return_value=self.db_mock).start()
        patch('bot.TaskHandler', return_value=self.task_handler_mock).start()

    def tearDown(self):
        patch.stopall()

    def test_start_message(self):
        self.message_mock.chat.id = 12345
        self.bot_mock.send_message = MagicMock()
        markup_mock = MagicMock()

        start_message(self.message_mock, self.bot_mock, self.logger_mock, markup_mock)

        self.bot_mock.send_message.assert_called_once_with(12345, "СТАРТУЕМ", reply_markup=markup_mock)
        self.logger_mock.info.assert_called_once_with("Пользователь 12345 запустил бота.")

    def test_help_message(self):
        self.message_mock.chat.id = 12345
        self.bot_mock.send_message = MagicMock()

        help_message(self.message_mock, self.bot_mock, self.logger_mock)

        self.bot_mock.send_message.assert_called_once_with(12345, 'текст')
        self.logger_mock.info.assert_called_once_with("Пользователь 12345 запросил помощь.")

    def test_handle_add_task(self):
        self.message_mock.text = "Добавить задачу"

        handle_add_task(self.message_mock, self.task_handler_mock)

        self.task_handler_mock.add_task.assert_called_once_with(self.message_mock)

    def test_handle_list_tasks(self):
        self.message_mock.text = "Список задач"

        handle_list_tasks(self.message_mock, self.task_handler_mock)

        self.task_handler_mock.list_tasks.assert_called_once_with(self.message_mock)

    def test_handle_mark_task_done(self):
        self.message_mock.text = "Выполнить задачу"

        handle_mark_task_done(self.message_mock, self.task_handler_mock)

        self.task_handler_mock.mark_task_done.assert_called_once_with(self.message_mock)

    def test_handle_set_reminder(self):
        self.message_mock.text = "Установить напоминание"

        handle_set_reminder(self.message_mock, self.task_handler_mock)

        self.task_handler_mock.set_reminder.assert_called_once_with(self.message_mock)

    def test_handle_delete_task(self):
        self.message_mock.text = "Удалить задачу"

        handle_delete_task(self.message_mock, self.task_handler_mock)

        self.task_handler_mock.delete_task.assert_called_once_with(self.message_mock)

    def test_handle_delete_all_tasks(self):
        self.message_mock.text = "Удалить все задачи"

        handle_delete_all_tasks(self.message_mock, self.task_handler_mock)

        self.task_handler_mock.delete_all_tasks.assert_called_once_with(self.message_mock)


if __name__ == "__main__":
    unittest.main()

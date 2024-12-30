import unittest
import tempfile
import  time
from data import Database
from models import User, Task


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем временную базу данных для тестов
        cls.db_url = tempfile.mktemp(suffix='.db')
        cls.db = Database(cls.db_url)
        cls.db.create_connection()

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)

    def setUp(self):
        # Очищаем таблицы перед каждым тестом
        with self.db.create_connection() as connection:
            with connection:
                connection.execute('DELETE FROM users')
                connection.execute('DELETE FROM tasks')

    def test_add_user(self):
        self.db.add_user(chat_id=12345, username='testuser')
        user = self.db.get_user_by_chat_id(12345)
        self.assertIsNotNone(user)
        self.assertEqual(user.chat_id, 12345)
        self.assertEqual(user.username, 'testuser')

    def test_add_duplicate_user(self):
        self.db.add_user(chat_id=12345, username='testuser')
        self.db.add_user(chat_id=12345, username='anotheruser')  # Дубликат
        user = self.db.get_user_by_chat_id(12345)
        self.assertEqual(user.username, 'testuser')  # Имя пользователя не должно измениться

    def test_add_task(self):
        self.db.add_user(chat_id=12345, username='testuser')
        user = self.db.get_user_by_chat_id(12345)
        self.db.add_task(user.user_id, 'Test Task')
        tasks = self.db.get_tasks(user.user_id)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].task, 'Test Task')
        self.assertFalse(tasks[0].completed)

    def test_mark_task_done(self):
        self.db.add_user(chat_id=12345, username='testuser')
        user = self.db.get_user_by_chat_id(12345)
        self.db.add_task(user.user_id, 'Test Task')
        tasks = self.db.get_tasks(user.user_id)
        self.assertFalse(tasks[0].completed)
        self.db.mark_task_done(tasks[0].task_id)
        tasks = self.db.get_tasks(user.user_id)
        self.assertTrue(tasks[0].completed)

    def test_delete_task(self):
        self.db.add_user(chat_id=12345, username='testuser')
        user = self.db.get_user_by_chat_id(12345)
        self.db.add_task(user.user_id, 'Test Task')
        tasks = self.db.get_tasks(user.user_id)
        self.assertEqual(len(tasks), 1)
        self.db.delete_task(tasks[0].task_id)
        tasks = self.db.get_tasks(user.user_id)
        self.assertEqual(len(tasks), 0)

    def test_delete_all_tasks(self):
        self.db.add_user(chat_id=12345, username='testuser')
        user = self.db.get_user_by_chat_id(12345)
        self.db.add_task(user.user_id, 'Task 1')
        self.db.add_task(user.user_id, 'Task 2')
        tasks = self.db.get_tasks(user.user_id)
        self.assertEqual(len(tasks), 2)
        self.db.delete_all_tasks(user.user_id)
        tasks = self.db.get_tasks(user.user_id)
        self.assertEqual(len(tasks), 0)



if __name__ == '__main__':
    unittest.main()

import sqlite3
from contextlib import closing
from models import User, Task


class Database:
    def __init__(self, db_url):
        self.db_url = db_url
        self.create_tables()

    def create_connection(self):
        return sqlite3.connect(self.db_url)

    def create_tables(self):
        with closing(self.create_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        chat_id INTEGER UNIQUE,
                        username TEXT
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        task TEXT,
                        completed BOOLEAN,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                connection.commit()

    def add_user(self, chat_id, username=None):
        with closing(self.create_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute('INSERT OR IGNORE INTO users (chat_id, username) VALUES (?, ?)', (chat_id, username))
                connection.commit()
                return cursor.lastrowid

    def get_user_by_chat_id(self, chat_id):
        with closing(self.create_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute('SELECT id, chat_id, username FROM users WHERE chat_id = ?', (chat_id,))
                user_data = cursor.fetchone()
                if user_data:
                    return User(user_data[0], user_data[1], user_data[2])
                return None

    def add_task(self, user_id, task_text):
        with closing(self.create_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute('INSERT INTO tasks (user_id, task, completed) VALUES (?, ?, ?)', (user_id, task_text, False))
                connection.commit()

    def get_tasks(self, user_id):
        with closing(self.create_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute('SELECT id, user_id, task, completed FROM tasks WHERE user_id = ?', (user_id,))
                tasks_data = cursor.fetchall()
                return [Task(task[0], task[1], task[2], task[3]) for task in tasks_data]

    def mark_task_done(self, task_id):
        with closing(self.create_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (True, task_id))
                connection.commit()

    def delete_task(self, task_id):
        with closing(self.create_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
                connection.commit()

    def delete_all_tasks(self, user_id):
        with closing(self.create_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute('DELETE FROM tasks WHERE user_id = ?', (user_id,))
                connection.commit()

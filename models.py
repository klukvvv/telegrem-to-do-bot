class Task:
    def __init__(self, task_id, user_id, task, completed=False):
        self.task_id = task_id
        self.user_id = user_id
        self.task = task
        self.completed = completed

    def __str__(self):
        return f"{self.task} - {'Выполнена' if self.completed else 'Не выполнена'}"


class User:
    def __init__(self, user_id, chat_id, username):
        self.user_id = user_id
        self.chat_id = chat_id
        self.username = username

    def __str__(self):
        return f"Пользователь: {self.username} (ID: {self.user_id})"

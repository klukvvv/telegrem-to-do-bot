from telebot import types
from data import Database
from models import User, Task
from utils.decorators import log_execution
from utils.iterators import TaskIterator
from datetime import datetime
import threading

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add('Добавить задачу')
markup.add('Список задач')
markup.add('Выполнить задачу')
markup.add('Установить напоминание')
markup.add('Удалить задачу')
markup.add('Удалить все задачи')


class TaskHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @log_execution
    def add_task(self, message):
        msg = self.bot.send_message(message.chat.id, "Введите задачу:")
        self.bot.register_next_step_handler(msg, self.save_task)

    @log_execution
    def save_task(self, message):
        task_text = message.text
        user_id = self.get_user_id(message.chat.id)
        self.db.add_task(user_id, task_text)
        self.bot.send_message(message.chat.id, f"Задача '{task_text}' добавлена!")

    @log_execution
    def list_tasks(self, message):
        user_id = self.get_user_id(message.chat.id)
        tasks = self.db.get_tasks(user_id)
        if not tasks:
            self.bot.send_message(message.chat.id, "Список задач пуст.")
        else:
            tasks_list = "\n".join([f"{i + 1}. {str(task)}" for i, task in enumerate(TaskIterator(tasks))])
            self.bot.send_message(message.chat.id, f"Список задач:\n{tasks_list}")

    @log_execution
    def mark_task_done(self, message):
        user_id = self.get_user_id(message.chat.id)
        tasks = self.db.get_tasks(user_id)
        if not tasks:
            self.bot.send_message(message.chat.id, "Список задач пуст. Невозможно отметить задачу как выполненную.")
            return

        tasks_list = "\n".join([f"{i + 1}. {task.task}" for i, task in enumerate(TaskIterator(tasks))])
        msg = self.bot.send_message(message.chat.id, f"Текущий список задач:\n{tasks_list}\nВведите номер задачи, "
                                                     f"которую хотите отметить как выполненной:")
        self.bot.register_next_step_handler(msg, self.complete_task)

    @log_execution
    def complete_task(self, message):
        try:
            task_index = int(message.text) - 1
            user_id = self.get_user_id(message.chat.id)
            tasks = self.db.get_tasks(user_id)
            if 0 <= task_index < len(tasks):
                task_id = tasks[task_index].task_id
                self.db.mark_task_done(task_id)
                self.bot.send_message(message.chat.id, f"Задача '{tasks[task_index].task}' выполнена!")
            else:
                self.bot.send_message(message.chat.id, "Неверный номер задачи.")
        except ValueError:
            self.bot.send_message(message.chat.id, "Пожалуйста, введите корректный номер задачи.")

    @log_execution
    def set_reminder(self, message):
        user_id = self.get_user_id(message.chat.id)
        tasks = self.db.get_tasks(user_id)
        if not tasks:
            self.bot.send_message(message.chat.id, "Список задач пуст. Невозможно установить напоминание.")
            return

        tasks_list = "\n".join([f"{i + 1}. {task.task}" for i, task in enumerate(TaskIterator(tasks))])
        msg = self.bot.send_message(message.chat.id, f"Текущий список задач:\n{tasks_list}\nВведите номер задачи для "
                                                     f"установки напоминания:")
        self.bot.register_next_step_handler(msg, lambda m: self.schedule_reminder(m, tasks))

    @log_execution
    def schedule_reminder(self, message, tasks):
        try:
            task_index = int(message.text) - 1
            if 0 <= task_index < len(tasks):
                task = tasks[task_index]
                msg = self.bot.send_message(message.chat.id, "Введите дату и время напоминания в формате 'YYYY-MM-DD "
                                                             "HH:MM':")
                self.bot.register_next_step_handler(msg, lambda m: self.set_reminder_time(m, task))
            else:
                self.bot.send_message(message.chat.id, "Неверный номер задачи.")
        except ValueError:
            self.bot.send_message(message.chat.id, "Пожалуйста, введите корректный номер задачи.")

    @log_execution
    def set_reminder_time(self, message, task):
        try:
            reminder_time = datetime.strptime(message.text, '%Y-%m-%d %H:%M')
            delay = (reminder_time - datetime.now()).total_seconds()
            if delay > 0:
                threading.Timer(delay, self.send_reminder, args=(task, message.chat.id)).start()
                self.bot.send_message(message.chat.id, f"Напоминание установлено для задачи '{task.task}' на {reminder_time}.")
            else:
                self.bot.send_message(message.chat.id, "Время напоминания должно быть в будущем.")
        except ValueError:
            print("ValueError raised")
            self.bot.send_message(message.chat.id,
                                      "Пожалуйста, введите дату и время в правильном формате 'YYYY-MM-DD HH:MM'.")
            raise

    def send_reminder(self, task, chat_id):
        self.bot.send_message(chat_id, f"НАПОМИНАЕМ: задача '{task.task}' должна быть выполнена!")

    @log_execution
    def delete_task(self, message):
        user_id = self.get_user_id(message.chat.id)
        tasks = self.db.get_tasks(user_id)
        if not tasks:
            self.bot.send_message(message.chat.id, "Список задач пуст. Невозможно удалить задачу.")
            return

        tasks_list = "\n".join([f"{i + 1}. {task.task}" for i, task in enumerate(TaskIterator(tasks))])
        msg = self.bot.send_message(message.chat.id, f"Текущий список задач:\n{tasks_list}\nВведите номер задачи, "
                                                     f"которую хотите удалить:")
        self.bot.register_next_step_handler(msg, self.remove_task)

    @log_execution
    def remove_task(self, message):
        try:
            task_index = int(message.text) - 1
            user_id = self.get_user_id(message.chat.id)
            tasks = self.db.get_tasks(user_id)
            if 0 <= task_index < len(tasks):
                task_id = tasks[task_index].task_id
                self.db.delete_task(task_id)
                self.bot.send_message(message.chat.id, f"Задача '{tasks[task_index].task}' удалена!")
            else:
                self.bot.send_message(message.chat.id, "Неверный номер задачи.")
        except ValueError:
            self.bot.send_message(message.chat.id, "Пожалуйста, введите корректный номер задачи.")

    @log_execution
    def delete_all_tasks(self, message):
        user_id = self.get_user_id(message.chat.id)
        self.db.delete_all_tasks(user_id)
        self.bot.send_message(message.chat.id, "Все задачи удалены!")

    def get_user_id(self, chat_id):
        user = self.db.get_user_by_chat_id(chat_id)
        if user:
            return user.user_id
        else:
            user_id = self.db.add_user(chat_id)
            return user_id

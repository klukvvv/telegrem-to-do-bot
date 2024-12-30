import telebot
from telebot import types
from datetime import datetime
import threading
from logger import setup_logger
from config import API_TOKEN
from data import Database
from task_handler import TaskHandler


def main():
    logger = setup_logger()
    bot = telebot.TeleBot(API_TOKEN)
    db = Database('tasks.db')
    task_handler = TaskHandler(bot, db)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_add_task = types.KeyboardButton("Добавить задачу")
    button_list_tasks = types.KeyboardButton("Список задач")
    button_mark_task_done = types.KeyboardButton("Выполнить задачу")
    button_set_reminder = types.KeyboardButton("Установить напоминание")
    button_delete_task = types.KeyboardButton("Удалить задачу")
    button_delete_all_tasks = types.KeyboardButton("Удалить все задач")
    markup.add(button_add_task, button_list_tasks, button_mark_task_done,
                    button_set_reminder, button_delete_task, button_delete_all_tasks)
    # bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

    # def show_main_menu(message):
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     button_add_task = types.KeyboardButton("Добавить задачу")
    #     button_list_tasks = types.KeyboardButton("Список задач")
    #     button_mark_task_done = types.KeyboardButton("Выполнить задачу")
    #     button_set_reminder = types.KeyboardButton("Установить напоминание")
    #     button_delete_task = types.KeyboardButton("Удалить задачу")
    #     button_delete_all_tasks = types.KeyboardButton("Удалить все задач")
    #     markup.add(button_add_task, button_list_tasks, button_mark_task_done,
    #                button_set_reminder, button_delete_task, button_delete_all_tasks)
    #     bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
    #
    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, "СТАРТУЕМ", reply_markup=markup)
        logger.info(f"Пользователь {message.chat.id} запустил бота.")

    @bot.message_handler(commands=['help'])
    def help_message(message):
        help_text = 'текст'
        bot.send_message(message.chat.id, help_text)
        logger.info(f"Пользователь {message.chat.id} запросил помощь.")

    @bot.message_handler(func=lambda message: message.text == "Добавить задачу")
    def handle_add_task(message):
        task_handler.add_task(message)

    @bot.message_handler(func=lambda message: message.text == "Список задач")
    def handle_list_tasks(message):
        task_handler.list_tasks(message)

    @bot.message_handler(func=lambda message: message.text == "Выполнить задачу")
    def handle_mark_task_done(message):
        task_handler.mark_task_done(message)

    @bot.message_handler(func=lambda message: message.text == "Установить напоминание")
    def handle_set_reminder(message):
        task_handler.set_reminder(message)

    @bot.message_handler(func=lambda message: message.text == "Удалить задачу")
    def handle_delete_task(message):
        task_handler.delete_task(message)

    @bot.message_handler(func=lambda message: message.text == "Удалить все задачи")
    def handle_delete_all_tasks(message):
        task_handler.delete_all_tasks(message)

    bot.polling()


if __name__ == "__main__":
    main()


#
# def send_reminder(chat_id, task):
#     bot.send_message(chat_id, f"НАПОМИНАЕМ: {task}")
#
#
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     welcome_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     welcome_keyboard.add(types.KeyboardButton("Добавить задачу"),
#                          types.KeyboardButton("Список задач"),
#                          types.KeyboardButton("Выполнить задачу"),
#                          types.KeyboardButton("Установить напоминание"),
#                          types.KeyboardButton("Удалить задачу"),
#                          types.KeyboardButton("Удалить все задачи"),
#                          types.KeyboardButton("/help"))
#     bot.send_message(message.chat.id, "СТРАТУЕМ!!!", reply_markup=welcome_keyboard)
#
#
# @bot.message_handler(commands=['help'])
# def help_message(message):
#     help_text = "что-то"
#     bot.send_message(message.chat.id, help_text)
#
#
# @bot.message_handler(func=lambda message: message.text == "Добавить задачу")
# def add_task(message):
#     msg = bot.send_message(message.chat.id, "Введите задачу:")
#     bot.register_next_step_handler(msg, save_task)
#
#
# def save_task(message):
#     task = message.text
#     tasks[message.chat.id] = tasks.get(message.chat.id, []) + [task]
#     bot.send_message(message.chat.id, f"Задача '{task}' добавлена!")
#
#
# @bot.message_handler(func=lambda message: message.text == "Список задач")
# def list_tasks(message):
#     user_tasks = tasks.get(message.chat.id, [])
#     if not user_tasks:
#         bot.send_message(message.chat.id, "Список задач пуст.")
#     else:
#         tasks_list = "\n".join([f"{i + 1}. {task}" for i, task in enumerate(user_tasks)])
#         bot.send_message(message.chat.id, f"Список задач:\n{tasks_list}")
#
#
# @bot.message_handler(func=lambda message: message.text == "Выполнить задачу")
# def mark_task_done(message):
#     user_tasks = tasks.get(message.chat.id, [])
#     if not user_tasks:
#         bot.send_message(message.chat.id, "Список задач пуст. Невозможно отметить задачу как выполненную.")
#         return
#
#     tasks_list = "\n".join([f"{i + 1}. {task}" for i, task in enumerate(user_tasks)])
#     msg = bot.send_message(message.chat.id,
#                            f"Текущий список задач:\n{tasks_list}\nВведите номер задачи, которую хотите отметить как выполненной:")
#     bot.register_next_step_handler(msg, complete_task)
#
#
# def complete_task(message):
#     try:
#         task_index = int(message.text) - 1
#         user_tasks = tasks.get(message.chat.id, [])
#         if 0 <= task_index < len(user_tasks):
#             completed_task = user_tasks.pop(task_index)
#             bot.send_message(message.chat.id, f"Задача '{completed_task}' выполнена!")
#         else:
#             bot.send_message(message.chat.id, "Неверный номер задачи.")
#     except ValueError:
#         bot.send_message(message.chat.id, "Пожалуйста, введите корректный номер задачи.")
#
#
# @bot.message_handler(func=lambda message: message.text == "Установить напоминание")
# def set_reminder(message):
#     user_tasks = tasks.get(message.chat.id, [])
#     if not user_tasks:
#         bot.send_message(message.chat.id, "Список задач пуст. Невозможно установить напоминание.")
#         return
#
#     tasks_list = "\n".join([f"{i + 1}. {task}" for i, task in enumerate(user_tasks)])
#     msg = bot.send_message(message.chat.id,
#                            f"Текущий список задач:\n{tasks_list}\nВведите номер задачи для установки напоминания:")
#     bot.register_next_step_handler(msg, schedule_reminder)
#
#
# def schedule_reminder(message):
#     try:
#         task_index = int(message.text) - 1
#         user_tasks = tasks.get(message.chat.id, [])
#         if 0 <= task_index < len(user_tasks):
#             task = user_tasks[task_index]
#             msg = bot.send_message(message.chat.id, "Введите дату и время напоминания в формате 'YYYY-MM-DD HH:MM':")
#             bot.register_next_step_handler(msg, lambda m: set_reminder_time(m, task))
#         else:
#             bot.send_message(message.chat.id, "Неверный номер задачи.")
#     except ValueError:
#         bot.send_message(message.chat.id, "Пожалуйста, введите корректный номер задачи.")
#
#
# def set_reminder_time(message, task):
#     try:
#         reminder_time = datetime.strptime(message.text, '%Y-%m-%d %H:%M')
#         delay = (reminder_time - datetime.now()).total_seconds()
#         if delay > 0:
#             threading.Timer(delay, send_reminder, args=(message.chat.id, task)).start()
#             bot.send_message(message.chat.id, f"Напоминание для задачи '{task}' установлено на {reminder_time}.")
#         else:
#             bot.send_message(message.chat.id, "Время напоминания должно быть в будущем.")
#     except ValueError:
#         bot.send_message(message.chat.id, "Неверный формат даты и времени. Пожалуйста, используйте 'YYYY-MM-DD HH:MM'.")
#
#
# @bot.message_handler(func=lambda message: message.text == "Удалить задачу")
# def delete_task(message):
#     user_tasks = tasks.get(message.chat.id, [])
#     if not user_tasks:
#         bot.send_message(message.chat.id, "Список задач пуст. Невозможно удалить задачу")
#         return
#
#     tasks_list = "\n".join([f"{i + 1}. {task}" for i, task in enumerate(user_tasks)])
#     msg = bot.send_message(message.chat.id,
#                            f"Текущий список задач:\n{tasks_list}\nВведите номер задачи, которую хотите удалить:")
#     bot.register_next_step_handler(msg, remove_task)
#
#
# def remove_task(message):
#     try:
#         task_index = int(message.text) - 1
#         user_tasks = tasks.get(message.chat.id, [])
#         if 0 <= task_index < len(user_tasks):
#             deleted_task = user_tasks.pop(task_index)
#             bot.send_message(message.chat.id, f"Задача '{deleted_task}' удалена!")
#         else:
#             bot.send_message(message.chat.id, "Неверный номер задачи.")
#     except ValueError:
#         bot.send_message(message.chat.id, "Пожалуйста, введите корректный номер задачи.")
#
#
# @bot.message_handler(func=lambda message: message.text == "Удалить все задачи")
# def delete_all_tasks(message):
#     tasks[message.chat.id] = []
#     bot.send_message(message.chat.id, "Все задачи удалены!")
#
#
# bot.polling()

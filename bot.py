import telebot
from telebot import types
from datetime import datetime
import threading
from logger import setup_logger
from config import API_TOKEN
from data import Database
from task_handler import TaskHandler


def start_message(message, bot, logger, markup):
    bot.send_message(message.chat.id, "СТАРТУЕМ", reply_markup=markup)
    logger.info(f"Пользователь {message.chat.id} запустил бота.")


def help_message(message, bot, logger):
    help_text = 'текст'
    bot.send_message(message.chat.id, help_text)
    logger.info(f"Пользователь {message.chat.id} запросил помощь.")


def handle_add_task(message, task_handler):
    task_handler.add_task(message)


def handle_list_tasks(message, task_handler):
    task_handler.list_tasks(message)


def handle_mark_task_done(message, task_handler):
    task_handler.mark_task_done(message)


def handle_set_reminder(message, task_handler):
    task_handler.set_reminder(message)


def handle_delete_task(message, task_handler):
    task_handler.delete_task(message)


def handle_delete_all_tasks(message, task_handler):
    task_handler.delete_all_tasks(message)


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
    button_delete_all_tasks = types.KeyboardButton("Удалить все задачи")
    markup.add(button_add_task, button_list_tasks, button_mark_task_done,
                button_set_reminder, button_delete_task, button_delete_all_tasks)

    @bot.message_handler(commands=['start'])
    def start_cmd(message):
        start_message(message, bot, logger, markup)

    @bot.message_handler(commands=['help'])
    def help_cmd(message):
        help_message(message, bot, logger)

    @bot.message_handler(func=lambda message: message.text == "Добавить задачу")
    def add_task_cmd(message):
        handle_add_task(message, task_handler)

    @bot.message_handler(func=lambda message: message.text == "Список задач")
    def list_tasks_cmd(message):
        handle_list_tasks(message, task_handler)

    @bot.message_handler(func=lambda message: message.text == "Выполнить задачу")
    def mark_task_done_cmd(message):
        handle_mark_task_done(message, task_handler)

    @bot.message_handler(func=lambda message: message.text == "Установить напоминание")
    def set_reminder_cmd(message):
        handle_set_reminder(message, task_handler)

    @bot.message_handler(func=lambda message: message.text == "Удалить задачу")
    def delete_task_cmd(message):
        handle_delete_task(message, task_handler)

    @bot.message_handler(func=lambda message: message.text == "Удалить все задачи")
    def delete_all_tasks_cmd(message):
        handle_delete_all_tasks(message, task_handler)

    bot.polling()


if __name__ == "__main__":
    main()


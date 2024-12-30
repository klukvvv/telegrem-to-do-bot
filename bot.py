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

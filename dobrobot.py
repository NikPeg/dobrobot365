from telebot import TeleBot
from threading import Thread
from time import sleep
from datetime import datetime
from collections import deque
from locals import TOKEN
from telebot import types


bot = TeleBot(TOKEN)
users_ids = []
posts = deque(['Пост1', 'Пост2', 'Пост3', 'Пост4', 'Пост5'])
events = deque(['Ивент1', 'Ивент2', 'Ивент3', 'Ивент4', 'Ивент5'])
scores = {}
HOUR = 3600
FOR_TESTS = 5
DEBUG = True

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    project_button = types.KeyboardButton("О проекте")
    account_button = types.KeyboardButton("Личный кабинет")
    events_button = types.KeyboardButton("Мероприятия этого месяца/календарь")
    help_buttton = types.KeyboardButton("Помощь/список команд")
    feedback_button = types.KeyboardButton("Связь с организаторами")
    markup.add(project_button, account_button, events_button, help_buttton, feedback_button)
    bot.reply_to(message, f'Привет, {message.from_user.first_name}!\n' +
                 'Это бот проекта "365 добрых дел". Он поможет тебе ' +
                 'ввести благотворительность в привычку!\n' +
                 'Список команд:\n/start\n/help\n/events', reply_markup=markup)
    
    users_ids.append(message.from_user.id)

@bot.message_handler(commands=['done'])
def done_event(message):
    bot.reply_to(message, 'Спасибо, что выполнил этот ивент!\n' +
                 'Число выполненных ивентов можешь посмотреть по команде' +
                 ' /events')
    id = message.from_user.id
    scores[id] = scores.get(id, 0) + 1


@bot.message_handler(commands=['events'])
def events_count(message):
    count = scores.get(message.from_user.id, 0)
    if count == 0:
        bot.reply_to(message, 'Ты пока не выполнил ни одного ивента. ' +
                     'Все впереди!')
    else:
        bot.reply_to(message, f'Ты выполнил уже целых {count} ' +
                     'ивентов! Так держать!')


@bot.message_handler(commands=['cancel'])
def events_count(message):
    bot.reply_to(message, 'Надеюсь, следующий ивент заинтересует тебя '
                 + 'сильнее!')


@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.reply_to(message, 'Прости, но я пока не знаю такой команды. ' +
                 'Попробуй /help')


def send_post():
    while True:
        if DEBUG:
            sleep(FOR_TESTS)
        else:
            sleep(HOUR)
        if posts and datetime.now().hour == 21:
            post = posts.popleft()
            for id in users_ids:
                bot.send_message(id, post)
        if events and datetime.now().hour == 20:
            event = events.popleft()
            for id in users_ids:
                bot.send_message(id, event + '\nОтветь /done, если выполнил' +
                                 ' ивент или /cancel, если не выполнил!')


th = Thread(target=send_post)
th.start()
bot.polling(none_stop=True)

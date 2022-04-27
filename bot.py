import threading
import time
import schedule as schedule
from dbFunctions import *
from sinoptikParser import *
import telebot
from secrets import *

bot = telebot.TeleBot(superSecretProdBotToken)


# event handlers
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Привіт, ' + message.from_user.first_name)
    bot.send_message(message.chat.id, 'Введіть назву міста')


@bot.message_handler(commands=["addschedule"])
def addSchedule(message):
    if userExistsInDB(message.chat.id):
        bot.send_message(message.chat.id, 'Ви вже підписані на розсилку. Спочатку видаліть поточну розсилку командою \n'
                                          '/removeschedule')
    else:
        bot.send_message(message.chat.id, 'Додаємо розсилку. Введіть назву міста, для якого ви хочете '
                                          'отримувати прогнози')

        bot.register_next_step_handler(message, addUserToDB)


@bot.message_handler(commands=["removeschedule"])
def removeSchedule(message):
    if userExistsInDB(message.chat.id):
        removeUserFromDB(message.chat.id)
        bot.send_message(message.chat.id, 'Ви успішно відписані від розсилки. Знову підписатися можна командою \n '
                                          '/addschedule')
    else:
        bot.send_message(message.chat.id, 'Ви і так не підписані на розсилку. Спочатку підпишіться командою \n '
                                          '/addschedule')


@bot.message_handler(commands=["10days"])
def forecast10days(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Київ', callback_data='Київ'))
    markup.add(telebot.types.InlineKeyboardButton(text='Хмельницький', callback_data='Хмельницький'))
    markup.add(telebot.types.InlineKeyboardButton(text='Кропивницький', callback_data='Кропивницький'))
    markup.add(telebot.types.InlineKeyboardButton(text='Львів', callback_data='Львів'))
    markup.add(telebot.types.InlineKeyboardButton(text='Кривий Ріг', callback_data='Кривий Ріг'))
    bot.send_message(message.chat.id, text="Виберіть місто зі списку", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text=call.data + '? ОК!')
    answer = ''
    if call.data == 'Київ':
        answer = 'Київ'
    elif call.data == 'Хмельницький':
        answer = 'Хмельницький'
    elif call.data == 'Кропивницький':
        answer = 'Кропивницький'
    elif call.data == 'Львів':
        answer = 'Львів'
    elif call.data == 'Кривий Ріг':
        answer = 'Кривий Ріг'

    answer = answer.replace(" ", "-")
    bot.send_message(call.message.chat.id, get10DaysWeatherForecast(getWeatherData(answer), answer))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    inputText = message.text
    try:
        city = inputText.replace(" ", "-")
        bot.send_message(message.chat.id, getWeatherTextMessage(getWeatherData(city), city))
    except:
        bot.send_message(message.chat.id, 'Нормально введіть назву міста')


# functions
def send10daysWeatherForecast(message):
    cityName = message.text
    bot.send_message(message.from_user.id, get10DaysWeatherForecast(getWeatherData(cityName), cityName));


def addUserToDB(message):
    inputText = message.text.replace(" ", "-")
    if requests.get('https://ua.sinoptik.ua/погода-' + inputText + '/10-днів').status_code == 404:
        bot.send_message(message.chat.id, 'Міста в базі немає. Введіть нормальне місто')
        bot.register_next_step_handler(message, addUserToDB)
    else:
        bot.send_message(message.chat.id, 'Додаємо місто до розсилки...')
        time.sleep(0.6)
        addUser(message.from_user.id, message.from_user.username, message.from_user.first_name,
                message.from_user.last_name, inputText)
        bot.send_message(message.chat.id, 'Місто ' + inputText[0].upper() + inputText[1:] + 'додано до розсилки кожен '
                                                                                            'день о 11:00. ')


def sendForecastToDBUsers():
    usersList = getUsersFromDB()
    for user in usersList:
        try:
            bot.send_message(user[1], getWeatherTextMessage(getWeatherData(user[5]), user[5]))
        finally:
            pass


# Scheduled forecast sending
def runScheduledSender():
    schedule.every().day.at("11:00").do(sendForecastToDBUsers)
    while True:
        schedule.run_pending()
        time.sleep(1)


scheduleThread = threading.Thread(target=runScheduledSender)
scheduleThread.start()

# bot start
bot.polling(none_stop=True, interval=0)

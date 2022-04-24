from sinoptikParser import *
import telebot

bot = telebot.TeleBot('5309180153:AAF4JjUKn0dMM_3dT41zLsetvxwGWsac33w')


# prod token
# token = "5399602109:AAG_JUQOsU0sjbfghULDuZ3ZolBj6Pq_5v0"


# event handlers
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Введіть назву міста')


@bot.message_handler(commands=["10days"])
def forecast10days(message):
    bot.send_message(message.from_user.id, 'Введіть назву міста')
    bot.register_next_step_handler(message, send10daysWeatherForecast)


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


# bot start
bot.polling(none_stop=True, interval=0)

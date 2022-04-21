import time
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

from bs4 import BeautifulSoup
import requests

def getWeatherInfo(cityName):
    outputCity = cityName[0].upper() + cityName[1:]
    sinoptikURL = 'https://ua.sinoptik.ua/погода-' + cityName + '/10-днів'
    sinoptikHTML = requests.get(sinoptikURL).text
    soup = BeautifulSoup(sinoptikHTML, "html.parser")

    temperatureDataArray = []

    for dayNumber in range(1, 11):
        currentDayDiv = soup.find("div", {"id": "bd" + str(dayNumber)})
        date = currentDayDiv.find("p", {"class": "date"}).getText()
        month = currentDayDiv.find("p", {"class": "month"}).getText()
        minTemp = currentDayDiv.find("div", {"class": "min"}).find("span").getText()
        maxTemp = currentDayDiv.find("div", {"class": "max"}).find("span").getText()
        weatherInfo = currentDayDiv.find("div", {"class": "weatherIco"}).get('title')

        temperatureDataArray.append({
            'date': date,
            'month': month,
            'minTemp': minTemp,
            'maxTemp': maxTemp,
            'weatherInfo': weatherInfo
        })
    weatherInfo = 'Погода у місті ' + outputCity + "\n" \
                  + "Сьогодні " + temperatureDataArray[0].get('date') + " " \
                  + temperatureDataArray[0].get('month') + "\n" \
                  + "Від " \
                  + temperatureDataArray[0].get('minTemp') \
                  + " до " \
                  + temperatureDataArray[0].get('maxTemp') + ". " \
                  + temperatureDataArray[0].get('weatherInfo') + "\n" \
                  + "Завтра  " + "\n" \
                  + "Від " \
                  + temperatureDataArray[1].get('minTemp') \
                  + " до " \
                  + temperatureDataArray[1].get('maxTemp') + ". " \
                  + temperatureDataArray[0].get('weatherInfo')

    return weatherInfo


token = "5399602109:AAG_JUQOsU0sjbfghULDuZ3ZolBj6Pq_5v0"
updater = Updater(token, use_context=True)


def on_start(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="Введіть назву міста")


def on_kyiv(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=getWeatherInfo('київ'))


def on_lviv(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=getWeatherInfo('львів'))


def on_kropinitsky(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=getWeatherInfo('кропивницький'))


def on_kriviyrih(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=getWeatherInfo('кривий-ріг'))


def on_khmelnitskiy(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=getWeatherInfo('хмельницький'))


def on_bnr(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=getWeatherInfo('белгород'))
    context.bot.send_message(chat_id=chat.id, text="Слава БНР!")
    time.sleep(1)
    for i in range(0, 7):
        context.bot.send_message(chat_id=chat.id, text="Слава БНР!")
        time.sleep(0.5)


def on_message(update, context):
    chat = update.effective_chat
    text = update.message.text
    if text == 'москва' or text == 'Москва':
        context.bot.send_message(chat_id=chat.id, text='Погода у місті Москва \n'
                                                       'Сьогодні\n'
                                                       'Від +800° до +900°. ' \
                                                       'Масово горять сраки руснявих виблядків\n'
                                                       'Завтра\n'
                                                       'Не настане'
                                 )
    elif text == 'белгород' or text == 'Белгород':
        context.bot.send_message(chat_id=chat.id, text=getWeatherInfo('белгород'))
        context.bot.send_message(chat_id=chat.id, text="Слава БНР!")
        time.sleep(1)
        for i in range(0, 7):
            context.bot.send_message(chat_id=chat.id, text="Слава БНР!")
            time.sleep(0.5)
    else:
        try:
            city = text.replace(" ", "-")
            context.bot.send_message(chat_id=chat.id, text=getWeatherInfo(city))
        except:
            context.bot.send_message(chat_id=chat.id, text="Нормально введи назву міста")



# event handlers
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", on_start))
dispatcher.add_handler(CommandHandler("khmelnitskiy", on_khmelnitskiy))
dispatcher.add_handler(CommandHandler("kyiv", on_kyiv))
dispatcher.add_handler(CommandHandler("lviv", on_lviv))
dispatcher.add_handler(CommandHandler("kropinitsky", on_kropinitsky))
dispatcher.add_handler(CommandHandler("kriviyrih", on_kriviyrih))
dispatcher.add_handler(CommandHandler("bnr", on_bnr))

dispatcher.add_handler(MessageHandler(Filters.all, on_message))

updater.start_polling()
updater.idle()

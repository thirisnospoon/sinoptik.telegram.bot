from sinoptikParser import *
import time


def on_bnr(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=getWeatherTextMessage(getWeatherData('белгород'), 'белгород'))
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
        context.bot.send_message(chat_id=chat.id, text=getWeatherTextMessage(getWeatherData('белгород'), 'белгород'))
        context.bot.send_message(chat_id=chat.id, text="Слава БНР!")
        time.sleep(1)
        for i in range(0, 7):
            context.bot.send_message(chat_id=chat.id, text="Слава БНР!")
            time.sleep(0.5)
    else:
        try:
            city = text.replace(" ", "-")
            context.bot.send_message(chat_id=chat.id, text=getWeatherTextMessage(getWeatherData(city), city))
        except:
            context.bot.send_message(chat_id=chat.id, text="Нормально введи назву міста")

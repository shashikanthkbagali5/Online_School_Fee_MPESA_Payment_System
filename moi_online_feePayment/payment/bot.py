import telebot
# from telebot import types
import time
import json
import requests
# from .models import Student

bot_token = '976849928:AAHTJSwepFUezNNcamCUMquJc2jdRF-B-JQ'

bot = telebot.TeleBot(token=bot_token)

@bot.message_handler(commands=['start'])
def welcome_student(message):
	bot.reply_to(message, 'Hello, welcome to musoEdu fee console, click or type "/help" for help')
# def start(bot, update):
# 	keyboard = [telegram.]


@bot.message_handler(commands=['help'])
def display_help(message):
	bot.reply_to(message, 'To check your fee balance simply click or type "/fee_balance" and share your phone number')

# need to write a function that allows the user to send the
# phone number they have registered their phone number with


@bot.message_handler(commands=['fee_balance'])
def return_fees(message):
	# fee = str(Student.objects.get(phone_no__contains='711836533').fee_balance)
	keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
	contact = telebot.types.KeyboardButton(text='Share Phone Number', request_contact=True)
	keyboard.add(contact)
	msg = 'Share your phone number to proceed'
	bot.reply_to(message, msg, reply_markup=keyboard)

# try and ident this line to see if it will only respond to just the message above...
# or maybe find a way to link the chat ID and the contact if they correspone then
# call the handler, otherwise send back an error message.

@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    print(message.contact.phone_number)
    pn = message.contact.phone_number
    # print(type(pn))
    url ='http://localhost:8000/api/student/?q=' +pn[4:]
    response = requests.get(url)
    print(response.text)
    rt = json.loads(response.text)
    msg = ''
    # we are expecting only one so if we get more... i.e len(rt)>1, then we have a problem
    try:
    	dic = rt[0]
    	fee = dic['fee_balance']
    	msg += 'Your Fee balance: ' +fee
    except:
    	msg += 'visit our website to register with a student account'
    bot.reply_to(message, msg)
bot.polling(none_stop=True)

# while True:
# 	try:
# 		bot.polling(none_stop=True)
# 	except Exception:
# 		time.sleep(15)
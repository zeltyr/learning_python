import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types # для указание типов
from decouple import config

token = config('token', default = '')
bot = telebot.TeleBot(token)

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Привет", callback_data="hello"),
                               InlineKeyboardButton("No", callback_data="cb_no"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Привет")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот".format(message.from_user), reply_markup=markup)
    

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "hello":
        bot.answer_callback_query(call.id, "привет")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет", reply_markup=gen_markup())
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)
import sqlite3
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from logic import *
from config import *

bot = TeleBot(bot_token)


def card_of_item(bot, message, row):

    info = f"""
Товар:   {row[1]}
Цвет:  {row[3]}
Цена:  {row[2]} рублей
"""
    with open(f'{row[4]}', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, info, reply_markup=gen_markup(row[0]))


def gen_markup(id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton(
        "Добавить в корзину", callback_data=f'buy_{id}'))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("buy"):
        id = call.data[call.data.find("_")+1:]
        user_id = call.message.chat.id
        manager.add_item_to_cart(user_id, id)
        bot.send_message(call.message.chat.id, "Товар добавлен в корзину")


@bot.message_handler(commands=['show_store'])
def show_store(message):
    res = manager.show_items()
    for row in res:
        card_of_item(bot, message, row)


@bot.message_handler(commands=['show_cart'])
def show_cart(message):
    user_id = message.chat.id
    rows = manager.show_cart(user_id)
    for row in rows:
        name = manager.get_name_of_item(row[1])[0][0]
        count = row[1]
        bot.send_message(message.chat.id, f"{name} - {count} шт.")


@bot.message_handler(commands=['delete_cart'])
def delete_history(message):
    manager.delete_cart()
    bot.send_message(message.chat.id, "Товары успешно очищены!")


if __name__ == '__main__':
    manager = StoreManager("store.db")
    bot.infinity_polling()

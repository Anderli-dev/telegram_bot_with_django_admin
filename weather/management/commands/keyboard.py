from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton


def main_keyboard():
    keyboard = ReplyKeyboardMarkup([]).from_row(["Weather", "WeatherPass", "Random Img"])
    keyboard.resize_keyboard = True

    return keyboard


def weather_pass_keyboard():
    subscribe = InlineKeyboardButton('Subscribe', callback_data='sub')
    unsubscribe = InlineKeyboardButton('Unsubscribe', callback_data='unsub')
    keyboard = InlineKeyboardMarkup([[subscribe, unsubscribe]])

    return keyboard

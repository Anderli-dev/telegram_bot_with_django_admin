import telegram.ext
from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Bot
from telegram import Update
from telegram.utils.request import Request
from telegram.ext import CallbackContext, CallbackQueryHandler, Filters, MessageHandler, Updater, CommandHandler

from .data import get_temp
from .keyboard import main_keyboard, weather_pass_keyboard

import random

from weather.models import User

updater = Updater(settings.TOKEN, use_context=True)


def weather_pass_msg(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=context.job.context, text='Weather in city ' + str(get_temp()))


def weather_pass(update: telegram.Update, context: telegram.ext.CallbackContext):
    jq = context.job_queue.run_repeating(weather_pass_msg, 10, context=update.effective_message.chat_id)
    return jq.job_queue


def start_func(update: Update, context: CallbackContext):

    p, _ = User.objects.get_or_create(
        external_id=update.message.chat_id,
        defaults={
            'username': update.message.from_user.first_name,
        }
    )

    username = update.message.from_user.first_name
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Hi '+str(username),
                             reply_markup=main_keyboard())


def sub_func(update: Update, context: CallbackContext):
    is_pass = User.objects.get(external_id=update.effective_message.chat_id).weather_pass

    if is_pass:
        context.bot.send_message(chat_id=update.effective_message.chat_id, text='You are subscribed',
                                 reply_markup=main_keyboard())
    else:
        p, _ = User.objects.update_or_create(
            external_id=update.effective_message.chat_id,
            defaults={
                'weather_pass': True,
            }
        )
        context.bot.send_message(chat_id=update.effective_message.chat_id, text='You was subscribed',
                                 reply_markup=main_keyboard())
        weather_pass(update, context).start()


def unsub_func(update: Update, context: CallbackContext):
    is_pass = User.objects.get(external_id=update.effective_message.chat_id).weather_pass

    if is_pass:
        p, _ = User.objects.update_or_create(
            external_id=update.effective_message.chat_id,
            defaults={
                'weather_pass': False,
            }
        )
        context.bot.send_message(chat_id=update.effective_message.chat_id, text='You was unsubscribed',
                                 reply_markup=main_keyboard())
        weather_pass(update, context).stop()
    else:
        context.bot.send_message(chat_id=update.effective_message.chat_id, text='You are not subscribed',
                                 reply_markup=main_keyboard())


def main_func(update: Update, context: CallbackContext):
    p, _ = User.objects.get_or_create(
        external_id=update.message.chat_id,
        defaults={
            'username': update.message.from_user.first_name,
        }
    )

    text = update.message.text.lower()
    if text == 'weather':
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Weather in city ' + str(get_temp()),
                                 reply_markup=main_keyboard())

    elif text == 'random img':
        random_id = random.randint(1, 100000)
        random_img_url = 'https://source.unsplash.com/random/1280x720?sig=' + str(random_id)

        context.bot.send_photo(chat_id=update.message.chat_id, photo=random_img_url)

    elif text == 'weatherpass':
        context.bot.send_message(chat_id=update.message.chat_id, text='What do you want to do', reply_markup=weather_pass_keyboard())

        p, _ = User.objects.update_or_create(
            external_id=update.message.chat_id,
            defaults={
                'username': update.message.from_user.first_name,
            }
        )


class Command(BaseCommand):

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.1,
            read_timeout=0.1,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        start_handler = CommandHandler('start', start_func)
        updater.dispatcher.add_handler(start_handler)

        massage_handler = MessageHandler(Filters.text, main_func)
        updater.dispatcher.add_handler(massage_handler)

        updater.dispatcher.add_handler(CallbackQueryHandler(sub_func, pattern='sub'))
        updater.dispatcher.add_handler(CallbackQueryHandler(unsub_func, pattern='unsub'))

        updater.start_polling()
        updater.idle()

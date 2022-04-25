# Booking telegram bot
import venv

from telegram import ReplyKeyboardRemove, ParseMode, Update
from telegram.ext import Updater,CallbackQueryHandler,CommandHandler, CallbackContext
import logging

import pbotcalendar as pbc
from settings import TOKEN
#TOKEN = ''

'''
Logging mode
'''
logging.basicConfig(format='%(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
'''
-========== Bot work ==========-
'''
WELCOM_MSG = 'Для выбора даты для бронирования спользуйте команду: /calendar'
CALENDAR_MSG = 'Выберите дату'
RESULT_MSG = 'Выбрана дата - '

def start(update, context):
    context.bot.send_message(
        chat_id = update.message.chat_id,
        text = WELCOM_MSG,
        parse_mode = ParseMode.HTML)

def calendar_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text = CALENDAR_MSG,
        reply_markup = pbc.create_calendar()
    )

def inline_calendar_handler(update: Update, context: CallbackContext):
    selected, date = pbc.process_calendar_selection(context.bot, update)
    if selected:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                text = RESULT_MSG + date,
                reply_markup = ReplyKeyboardRemove())

if TOKEN == '':
    print('Please write TOKEN into file')
else:
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('calendar', calendar_handler))
    dispatcher.add_handler(CallbackQueryHandler(inline_calendar_handler))

    updater.start_polling()
    updater.idle()
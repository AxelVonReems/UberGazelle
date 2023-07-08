from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes, ConversationHandler
    )
from telegram_bot_pagination import InlineKeyboardPaginator

from utils import intro_keyboard, regions_keyboard, vehicle_types_keyboard


class RegionPaginator(InlineKeyboardPaginator):
    first_page_label = '<<'
    previous_page_label = '<'
    current_page_label = '-{}-'
    next_page_label = '>'
    last_page_label = '>>'


async def driver_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_driver_text = '''
Для начала выберите регионы, из которых вы готовы принимать заказы. Возможно
выбрать несколько регионов. Выбирайте необходимые регионы с помощью экранной
клавиатуры. Для подтверждения выбора регионов нажмите кнопку "Продолжить".
        '''
    nxtkboard = [[KeyboardButton('Продолжить')]]
    await update.message.reply_text(
        text=new_driver_text,
        reply_markup=ReplyKeyboardMarkup(
            nxtkboard, resize_keyboard=True
        )
    )
    return 'driver_id'


async def driver_regions(update: Update, context: ContextTypes):
    context.user_data['new_driver'] = {'driver_id': update.effective_user.id}
    await update.message.reply_text(
        text='Выберите регион',
        reply_markup=ReplyKeyboardMarkup(
            regions_keyboard, resize_keyboard=True, one_time_keyboard=True
        )
    )
    return 'regions'


async def driver_vehicle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['new_driver']['regions'] = update.message.text
    await update.message.reply_text(
        text='Выберите тип вашего ТС',
        reply_markup=ReplyKeyboardMarkup(
            vehicle_types_keyboard, resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    return 'driver_summary'


async def driver_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['new_driver']['vehicle_types'] = update.message.text
    summary = f'''
Благодарим за реистрацию в сервисе.
Ваш ID: {context.user_data['new_driver']['driver_id']}.
Выбранные регионы: {context.user_data['new_driver']['regions']}.
Выбранный тип ТС: {context.user_data['new_driver']['vehicle_types']}
    '''
    await update.message.reply_text(
        text=summary, reply_markup=ReplyKeyboardMarkup(
            intro_keyboard, resize_keyboard=True
        )
    )
    return ConversationHandler.END


async def driver_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    unknown_answer = ('''
Я вас не понимаю. Пожалуйста, используйте кнопки экранной клавиатуры при
создании профиля.
    ''')
    await update.message.reply_text(
        text=unknown_answer
    )

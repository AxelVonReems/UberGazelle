from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes, ConversationHandler
    )

from utils import intro_keyboard, regions_keyboard, vehicle_types_keyboard


async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_driver_text = '''
Для создания нового заказа вводите данные о вашем отправлении в соответствии с
моими подсказками.
        '''
    nxtkboard = [[KeyboardButton('Продолжить')]]
    await update.message.reply_text(
        text=new_driver_text,
        reply_markup=ReplyKeyboardMarkup(
            nxtkboard, resize_keyboard=True, one_time_keyboard=True
        )
    )
    return 'order_weight'


async def order_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['new_order'] = {'customer_id': update.effective_user.id}
    await update.message.reply_text(
        text='Введите массу груза в килограммах с коруглением до целых чисел'
    )
    return 'order_length'


async def order_length(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['new_order']['order_weight'] = int(update.message.text)
    await update.message.reply_text(
        text='Введите длину груза в метрах с коруглением до целых чисел'
    )
    return 'order_width'


async def order_width(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['new_order']['order_length'] = int(update.message.text)
    await update.message.reply_text(
        text='Введите ширину груза в метрах с коруглением до целых чисел'
    )
    return 'order_height'


async def order_height(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['new_order']['order_width'] = int(update.message.text)
    await update.message.reply_text(
        text='Введите высоту груза в метрах с коруглением до целых чисел'
    )
    return 'order_pickup_region'


async def order_pickup_region(
        update: Update, context: ContextTypes.DEFAULT_TYPE
        ):
    context.user_data['new_order']['order_height'] = int(update.message.text)
    await update.message.reply_text(
        text='Выберите регион отправки груза',
        reply_markup=ReplyKeyboardMarkup(
            regions_keyboard, resize_keyboard=True, one_time_keyboard=True
        )
    )
    return 'order_pickup_address'


async def order_pickup_address(
        update: Update, context: ContextTypes.DEFAULT_TYPE
        ):
    context.user_data['new_order']['pickup_region'] = update.message.text
    await update.message.reply_text(
        text='Введите адрес отправки груза'
    )
    return 'order_delivery_region'


async def order_delivery_region(
        update: Update, context: ContextTypes.DEFAULT_TYPE
        ):
    context.user_data['new_order']['pickup_address'] = update.message.text
    await update.message.reply_text(
        text='Выберите регион доставки груза',
        reply_markup=ReplyKeyboardMarkup(
            regions_keyboard, resize_keyboard=True, one_time_keyboard=True
        )
    )
    return 'order_delivery_address'


async def order_delivery_address(
        update: Update, context: ContextTypes.DEFAULT_TYPE
        ):
    context.user_data['new_order']['delivery_region'] = update.message.text
    await update.message.reply_text(
        text='Введите адрес доставки груза'
    )
    return 'order_vehicle_type'


async def order_vehicle_type(
        update: Update, context: ContextTypes.DEFAULT_TYPE
        ):
    context.user_data['new_order']['delivery_address'] = update.message.text
    await update.message.reply_text(
        text='Выберите необходимый тип ТС',
        reply_markup=ReplyKeyboardMarkup(
            vehicle_types_keyboard, resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    return 'order_description'


async def order_description(
        update: Update, context: ContextTypes.DEFAULT_TYPE
        ):
    context.user_data['new_order']['vehicle_type'] = update.message.text
    order_descr_text = '''
Введите описание груза. Для ускорения поиска водителя описывайте груз
максимально подробно.
    '''
    await update.message.reply_text(
        text=order_descr_text
    )
    return 'order_summary'


async def order_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['new_order']['order_description'] = update.message.text
    summary_text = f'''
Заказ успешно создан. Ожидайте сообщений с предложениями о перевозке от
водителей, зарегистрированных в сервисе.
Данные вашего заказа:
Ваш ID: {context.user_data['new_order']['customer_id']}.
Масса груза, кг: {context.user_data['new_order']['order_weight']}.
Длина груза, м: {context.user_data['new_order']['order_length']}.
Ширина груза, м: {context.user_data['new_order']['order_width']}.
Высота груза, м: {context.user_data['new_order']['order_height']}.
Регион отправки груза: {context.user_data['new_order']['pickup_region']}.
Адрес отправки груза: {context.user_data['new_order']['pickup_address']}.
Регион доставки груза: {context.user_data['new_order']['delivery_region']}.
Адрес доставки груза: {context.user_data['new_order']['delivery_address']}.
Выбранный тип ТС: {context.user_data['new_order']['vehicle_type']}.
Описание груза: {context.user_data['new_order']['order_description']}.
    '''
    await update.message.reply_text(
        text=summary_text, reply_markup=ReplyKeyboardMarkup(
            intro_keyboard, resize_keyboard=True
        ))
    return ConversationHandler.END


async def order_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    unknown_answer = ('''
Я вас не понимаю. Для создания заказа следуйте моим инструкциям.
    ''')
    await update.message.reply_text(
        text=unknown_answer
    )

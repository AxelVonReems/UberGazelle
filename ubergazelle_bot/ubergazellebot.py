import logging
# import os

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    filters, ApplicationBuilder, ContextTypes, CommandHandler,
    ConversationHandler, MessageHandler
    )

# from dotenv import load_dotenv
from ug_drivers import (
    driver_regions, driver_start, driver_summary, driver_vehicle,
    driver_unknown
)
from ug_neworder import (
    order_delivery_address, order_delivery_region, order_description,
    order_height, order_length, order_pickup_address, order_pickup_region,
    order_start, order_summary, order_weight, order_width, order_vehicle_type,
    order_unknown
)
from utils import intro_keyboard, vehicle_types, region_list
from secrets_tokens import BOT_SECRET_TOKEN

# load_dotenv()

# secret_token = os.getenv('BOT_SECRET_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='UG_logs.log',
    level=logging.DEBUG
)

secret_token = BOT_SECRET_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_chat.first_name
    intro_text = (f'''
Добрый день, {user_name}! Я могу помочь Вам найти небольшой грузовик или
микроавтобус для перевозки грузов. Для создания нового заказа нажмите кнопку
"Создать заказ". Если Вы хотите зарегистрироваться в качестве водителя нажмите
кнопку "Зарегистрироваться как водитель".
        ''')
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=intro_text,
            reply_markup=ReplyKeyboardMarkup(
                intro_keyboard, resize_keyboard=True
                )
            )


async def kifflom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await context.bot.send_message(
        chat_id=chat.id, text=(
            'Kifflom! the tract is not yet written!'
        )
    )


async def delete_driver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await context.bot.send_message(
        chat_id=chat.id, text=(
            'Для удаления своей учетной записи следуйте моим подсказкам.'
        )
    )


def main():
    application = ApplicationBuilder().token(secret_token).build()

    create_order = ConversationHandler(
        entry_points=[MessageHandler(
            filters.Regex('^(Создать заказ)$'), order_start
            )],
        states={
            'order_weight': [
                MessageHandler(filters.Text('Продолжить'), order_weight)
            ],
            'order_length': [
                MessageHandler(filters.Regex('^\\d+$'), order_length)
            ],
            'order_width': [
                MessageHandler(filters.Regex('^\\d+$'), order_width)
            ],
            'order_height': [
                MessageHandler(filters.Regex('^\\d+$'), order_height)
            ],
            'order_pickup_region': [
                MessageHandler(filters.Regex('^\\d+$'), order_pickup_region)
            ],
            'order_pickup_address': [
                MessageHandler(filters.Text(region_list), order_pickup_address)
            ],
            'order_delivery_region': [MessageHandler(
                filters.TEXT, order_delivery_region
            )],
            'order_delivery_address': [MessageHandler(
                filters.Text(region_list), order_delivery_address
            )],
            'order_vehicle_type': [
                MessageHandler(filters.TEXT, order_vehicle_type)
            ],
            'order_description': [
                MessageHandler(filters.Text(vehicle_types), order_description)
            ],
            'order_summary': [
                MessageHandler(filters.TEXT, order_summary)
            ],
        },
        fallbacks=[
            MessageHandler(
                filters.TEXT | filters.Regex('^\\d+$') |
                filters.Text(region_list) | filters.Text(vehicle_types),
                order_unknown
            )
        ],
    )

    create_driver = ConversationHandler(
        entry_points=[MessageHandler(
            filters.Regex('^(Зарегистрироваться как водитель)$'), driver_start
            )],
        states={
            'driver_id': [
                MessageHandler(filters.Text('Продолжить'), driver_regions)
            ],
            'regions': [
                MessageHandler(filters.Text(region_list), driver_vehicle)
            ],
            'vehicle_types': [
                MessageHandler(filters.TEXT, driver_summary)
            ],
            'driver_summary': [
                MessageHandler(filters.Text(vehicle_types), driver_summary)
            ]
        },
        fallbacks=[MessageHandler(filters.TEXT, driver_unknown)],
    )

    application.add_handler(CommandHandler('start', start))

    application.add_handler(create_order)
    application.add_handler(create_driver)

    application.add_handler(
        MessageHandler(
            filters.Regex('^(Удалить учетную запись)$'), delete_driver
        )
    )

    application.add_handler(
        MessageHandler(
            filters.Regex('^(Kifflom!)$'), kifflom
        )
    )

    application.run_polling()


if __name__ == '__main__':
    main()

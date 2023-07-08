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


async def new_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await context.bot.send_message(
        chat_id=chat.id,
        text=(
            'Для создания заказа вводите данные в соответствии с '
            'моими подсказками.'
        )
    )


async def delete_driver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await context.bot.send_message(
        chat_id=chat.id,
        text=(
            'Для удаления своей учетной записи следуйте моим подсказкам.'
        )
    )


def main():
    application = ApplicationBuilder().token(secret_token).build()

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
        fallbacks=[MessageHandler(
            filters.TEXT, driver_unknown
            )
        ],
    )

    application.add_handler(create_driver)

    application.add_handler(CommandHandler('start', start))
    application.add_handler(
        MessageHandler(filters.Regex('^(Создать заказ)$'), new_order)
    )
    application.add_handler(
        MessageHandler(
            filters.Regex('^(Удалить учетную запись)$'), delete_driver
        )
    )

    application.run_polling()


if __name__ == '__main__':
    main()

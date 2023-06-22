import logging
# import os

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (
    filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
    )

# from dotenv import load_dotenv

from secrets_tokens import BOT_SECRET_TOKEN

# load_dotenv()

# secret_token = os.getenv('BOT_SECRET_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='UG_logs.log',
    level=logging.DEBUG
)

secret_token = BOT_SECRET_TOKEN

NEW_ORDER_TEXT = 'Создать заказ'
NEW_DRIVER_TEXT = 'Зарегистрироваться как водитель'
DELETE_DRIVER_TEXT = 'Удалить учетную запись'

BUTTONS = [
    [KeyboardButton(NEW_ORDER_TEXT)],
    [KeyboardButton(NEW_DRIVER_TEXT), KeyboardButton(DELETE_DRIVER_TEXT)],
    ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_chat.first_name
    intro_text = (
        f'Добрый день, {user_name}! Я могу помочь Вам найти небольшой '
        f'грузовик или микроавтобус для перевозки грузов. Для создания нового '
        f'заказа нажмите кнопку "Создать заказ". Если Вы хотите '
        f'зарегистрироваться в качестве водителя нажмите кнопку '
        f'"Зарегистрироваться как водитель".'
    )
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=intro_text,
            reply_markup=ReplyKeyboardMarkup(BUTTONS, resize_keyboard=True)
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


async def new_driver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await context.bot.send_message(
        chat_id=chat.id,
        text=(
            'Для регистрации в сервисе вводите данные в соответствии с '
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

    application.add_handler(CommandHandler('start', start))
    application.add_handler(
        MessageHandler(filters.Regex('^(Создать заказ)$'), new_order)
    )
    application.add_handler(
        MessageHandler(
            filters.Regex('^(Зарегистрироваться как водитель)$'), new_driver
        )
    )
    application.add_handler(
        MessageHandler(
            filters.Regex('^(Удалить учетную запись)$'), delete_driver
        )
    )

    application.run_polling()


if __name__ == '__main__':
    main()

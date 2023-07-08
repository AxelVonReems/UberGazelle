from telegram import KeyboardButton

NEW_ORDER_TEXT = 'Создать заказ'
NEW_DRIVER_TEXT = 'Зарегистрироваться как водитель'
DELETE_DRIVER_TEXT = 'Удалить учетную запись'

intro_keyboard = [
    [KeyboardButton(NEW_ORDER_TEXT)],
    [KeyboardButton(NEW_DRIVER_TEXT), KeyboardButton(DELETE_DRIVER_TEXT)],
    ]

REGION_1 = 'Санкт-Петербург'
REGION_2 = 'Ленинградская область'
REGION_3 = 'Псковская область'
REGION_4 = 'Новгородская область'

regions_keyboard = [
    [KeyboardButton(REGION_1), KeyboardButton(REGION_2)],
    [KeyboardButton(REGION_3), KeyboardButton(REGION_4)]
    ]

vehicle_types = ['Бортовой автомобиль', 'Тентованный автомобиль', 'Фургон']

vehicle_types_keyboard = [
        [KeyboardButton('Бортовой автомобиль')],
        [KeyboardButton('Тентованный автомобиль')],
        [KeyboardButton('Фургон')],
    ]

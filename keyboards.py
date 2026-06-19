from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Отправить телефон", request_contact=True)],
            [KeyboardButton(text="Ввести номер вручную")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def services_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍽 Заказ / доставка")],
            [KeyboardButton(text="🎓 Обучение / курс")],
            [KeyboardButton(text="🏥 Запись / консультация")],
            [KeyboardButton(text="🛒 Товар / покупка")],
            [KeyboardButton(text="Другое")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
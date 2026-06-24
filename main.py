import asyncio
import logging
import re

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import load_config
from database import init_db, save_lead
from google_sheets import try_append_lead_to_google_sheets
from keyboards import phone_keyboard, services_keyboard
from states import LeadForm


config = load_config()
router = Router()


def is_valid_phone(phone: str) -> bool:
    digits = re.sub(r"\D", "", phone)
    return 7 <= len(digits) <= 15


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(LeadForm.name)

    await message.answer(
        "Здравствуйте! 👋\n\n"
        "Я помогу оставить заявку.\n\n"
        "Как вас зовут?",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()

    await message.answer(
        "Заявка отменена.\n\n"
        "Чтобы начать заново, нажмите /start",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(LeadForm.name, F.text)
async def name_handler(message: Message, state: FSMContext) -> None:
    name = message.text.strip()

    if len(name) < 2:
        await message.answer("Введите имя минимум из 2 символов.")
        return

    await state.update_data(name=name)
    await state.set_state(LeadForm.phone)

    await message.answer(
        "Введите номер телефона или нажмите кнопку ниже.",
        reply_markup=phone_keyboard(),
    )


@router.message(LeadForm.phone)
async def phone_handler(message: Message, state: FSMContext) -> None:
    if message.contact:
        phone = message.contact.phone_number
    elif message.text:
        phone = message.text.strip()
    else:
        await message.answer("Пожалуйста, отправьте номер телефона текстом.")
        return

    if phone == "Ввести номер вручную":
        await message.answer(
            "Введите номер телефона, например:\n+998 90 123 45 67",
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    if not is_valid_phone(phone):
        await message.answer(
            "Номер телефона выглядит неправильно.\n\n"
            "Пример:\n+998 90 123 45 67"
        )
        return

    await state.update_data(phone=phone)
    await state.set_state(LeadForm.service)

    await message.answer(
        "Какая услуга или товар вас интересует?",
        reply_markup=services_keyboard(),
    )


@router.message(LeadForm.service, F.text)
async def service_handler(message: Message, state: FSMContext) -> None:
    service = message.text.strip()

    if len(service) < 2:
        await message.answer("Напишите услугу или товар.")
        return

    await state.update_data(service=service)
    await state.set_state(LeadForm.comment)

    await message.answer(
        "Напишите комментарий к заявке.\n\n"
        "Например: удобное время, адрес, вопрос или детали заказа.",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(LeadForm.comment, F.text)
async def comment_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    comment = message.text.strip()

    if len(comment) < 1:
        comment = "-"

    data = await state.get_data()

    user = message.from_user
    telegram_user_id = user.id if user else None
    telegram_username = user.username if user and user.username else None

    lead_id = save_lead(
        database_path=config.database_path,
        telegram_user_id=telegram_user_id,
        telegram_username=telegram_username,
        name=data["name"],
        phone=data["phone"],
        service=data["service"],
        comment=comment,
    )

    try_append_lead_to_google_sheets(
        config=config,
        name=data["name"],
        phone=data["phone"],
        service=data["service"],
        comment=comment,
    )

    admin_text = (
        f"🔔 Новая заявка #{lead_id}\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"📌 Услуга: {data['service']}\n"
        f"💬 Комментарий: {comment}\n\n"
        f"Telegram user ID: {telegram_user_id}\n"
        f"Username: @{telegram_username if telegram_username else '-'}"
    )

    await bot.send_message(config.admin_id, admin_text)

    await message.answer(
        "Спасибо! ✅\n\n"
        "Ваша заявка принята. Мы скоро свяжемся с вами.",
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.clear()


@router.message()
async def fallback_handler(message: Message) -> None:
    await message.answer(
        "Я вас не понял.\n\n"
        "Чтобы оставить заявку, нажмите /start"
    )


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    init_db(config.database_path)

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Кнопки для головного меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.row(KeyboardButton("🔋 Заправитись"), KeyboardButton("📋 Мої заявки"))
main_menu.row(KeyboardButton("💰 Актуальна ціна"), KeyboardButton("ℹ️ Допомога"))

# Авторизація користувача
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("📱 Надати номер телефону", request_contact=True)
    )
    await message.answer("Привіт! Для початку роботи авторизуйся, поділися своїм номером телефону:",
                         reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def phone_handler(message: types.Message):
    user_phone = message.contact.phone_number
    user_id = message.from_user.id
    # Тут можна перевіряти номер в базі даних
    await message.answer("Дякую! Тепер ти можеш використовувати всі функції бота.", reply_markup=main_menu)

# Обробка кнопки "Заправитись"
@dp.message_handler(lambda message: message.text == "🔋 Заправитись")
async def request_fuel(message: types.Message):
    fuel_menu = ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton("АЗС №1"), KeyboardButton("АЗС №2"), KeyboardButton("АЗС №3")
    )
    await message.answer("Вибери свою заправку:", reply_markup=fuel_menu)

# Запуск бота
async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())










































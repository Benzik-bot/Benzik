import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.enums import ContentType, ParseMode
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота та диспетчера
bot = Bot(token=TOKEN, default=ParseMode.HTML)
dp = Dispatcher()

# Головне меню
def get_main_menu():
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row(KeyboardButton("🔋 Заправитись"), KeyboardButton("📋 Мої заявки"))
    menu.row(KeyboardButton("💰 Актуальна ціна"), KeyboardButton("ℹ️ Допомога"))
    return menu

# Меню АЗС
def get_fuel_menu():
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row(KeyboardButton("АЗС №1"), KeyboardButton("АЗС №2"), KeyboardButton("АЗС №3"))
    return menu

# Меню вибору літражу
def get_liters_menu():
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row(KeyboardButton("10 л"), KeyboardButton("20 л"), KeyboardButton("50 л"))
    menu.row(KeyboardButton("🔙 Назад"))
    return menu

# Авторизація користувача
@dp.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("📱 Надати номер телефону", request_contact=True)
    )
    await message.answer(
        f"Привіт, {hbold(message.from_user.full_name)}! Для початку роботи авторизуйся, поділися своїм номером телефону:",
        reply_markup=keyboard
    )

# Обробка номера телефону
@dp.message(F.content_type == ContentType.CONTACT)
async def phone_handler(message: types.Message):
    user_phone = message.contact.phone_number
    await message.answer("Дякую! Тепер ти можеш використовувати всі функції бота.", reply_markup=get_main_menu())

# Обробка кнопки "Заправитись"
@dp.message(F.text == "🔋 Заправитись")
async def request_fuel(message: types.Message):
    await message.answer("Вибери свою заправку:", reply_markup=get_fuel_menu())

# Вибір літражу після АЗС
@dp.message(F.text.in_(["АЗС №1", "АЗС №2", "АЗС №3"]))
async def select_liters(message: types.Message):
    await message.answer("Вибери кількість літрів:", reply_markup=get_liters_menu())

# Підтвердження замовлення
@dp.message(F.text.in_(["10 л", "20 л", "50 л"]))
async def confirm_order(message: types.Message):
    await message.answer(f"✅ Твоя заявка на {message.text} пального прийнята!", reply_markup=get_main_menu())

# Обробка кнопки "Мої заявки"
@dp.message(F.text == "📋 Мої заявки")
async def my_orders(message: types.Message):
    await message.answer("У тебе поки немає активних заявок.")

# Обробка кнопки "Актуальна ціна"
@dp.message(F.text == "💰 Актуальна ціна")
async def fuel_price(message: types.Message):
    await message.answer("Сьогодні ціна пального: 45 грн/л")

# Обробка кнопки "Допомога"
@dp.message(F.text == "ℹ️ Допомога")
async def help_info(message: types.Message):
    await message.answer("Я допоможу тобі заправити авто! Обери 'Заправитись' та слідуй інструкціям.")

# Запуск бота
async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Помилка запуску бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8656922621:AAHpd5fuIs6vSrnzIwJXUlYDgXOyzuKDCs"

dp = Dispatcher()

# Asosiy menyu tugmalari
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇨🇳 Xitoy tili alifbosi"),
            KeyboardButton(text="📝 Pro testlar"),
        ],
        [
            KeyboardButton(text="🎓 Kurslar haqida"),
            KeyboardButton(text="📞 Biz bilan aloqa"),
        ]
    ],
    resize_keyboard=True
)

# Start komandasi
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Salom, {html.bold(message.from_user.full_name)}! Xitoy tili PRO botiga xush kelibsiz!\n\n"
        f"Kerakli bo'limni tanlang:",
        reply_markup=main_menu
    )

# 🇨🇳 Xitoy tili alifbosi bo'limi
@dp.message(F.text == "🇨🇳 Xitoy tili alifbosi")
async def alphabet_handler(message: Message):
    text = (
        "🇨🇳 **Xitoy tili alifbosi va asoslari**\n\n"
        "Bilasizmi, xitoy tilida oddiy harflar yo'q. Uning o'rniga **Iyerogliflar** va ularning o'qilishini bildiruvchi **Pinyin** tizimi mavjud.\n\n"
        "1. **Pinyin (Lotincha o'qilishi):** Xitoycha so'zlarni lotin harflari yordamida o'qish uchun ishlatiladi.\n"
        "2. **Ohanglar (Tones):** Xitoy tilida 4 ta asosiy ohang bor. Ohang o'zgarsa, so'zning ma'nosi ham o'zgarib ketadi!\n\n"
        "Tez orada bu yerda batafsil darslar va mashqlar qo'shiladi! 🚀"
    )
    await message.answer(text, parse_mode="Markdown")

# 📝 Pro testlar bo'limi (Saytga yo'naltiruvchi tugma bilan)
@dp.message(F.text == "📝 Pro testlar")
async def pro_tests_handler(message: Message):
    # SAYT_MANZILINGIZ degan joyga o'z veb-saytingiz havolasini yozasiz (masalan: https://sardorbek.uz/tests)
    pro_test_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌐 Saytda boshlash (PRO)", url="https://SIZNING_SAYT_MANZILINGIZ.uz")
            ]
        ]
    )
    
    text = (
        "💎 **Xitoy tili PRO Testlar bo'limi**\n\n"
        "Bu bo'limda siz o'z bilimingizni HSK imtihonlari darajasida sinab ko'rishingiz mumkin.\n\n"
        "🚀 **Afzalliklari:**\n"
        "• Real imtihon savollari\n"
        "• Xatolaringiz tahlili va tushuntirishi\n"
        "• Reyting tizimi\n\n"
        "Barcha PRO testlar rasmiy veb-saytimizda ishga tushdi! Marhamat, quyidagi tugma orqali o'tib, o'z bilimingizni sinang:"
    )
    await message.answer(text, reply_markup=pro_test_kb, parse_mode="Markdown")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

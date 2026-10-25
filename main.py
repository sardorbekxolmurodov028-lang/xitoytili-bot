import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8656922621:AAHpd5fuIs6vSrnzIwjXUlYDgXOyzuKDCts"

dp = Dispatcher()

# Asosiy menyu tugmalari
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇨🇳 Xitoy tili alifbosi"),
            KeyboardButton(text="📝 Testlar")
        ],
        [
            KeyboardButton(text="🎓 Kurslar haqida"),
            KeyboardButton(text="📞 Biz bilan aloqa")
        ]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Salom, {html.bold(message.from_user.full_name)}! Xitoy tili PRO botiga xush kelibsiz!\n\n"
        f"Kerakli bo'limni tanlang:",
        reply_markup=main_menu
    )

@dp.message(F.text == "🇨🇳 Xitoy tili alifbosi")
async def alphabet_handler(message: Message):
    await message.answer("Bu bo'limda tez orada Xitoy tili alifbosi joylashtiriladi!")

@dp.message(F.text == "📝 Testlar")
async def tests_handler(message: Message):
    await message.answer("Bu bo'limda xitoy tilidan testlar bo'ladi!")

# Kurslar haqida batafsil ma'lumot va faqat kursga yozilish tugmasi
@dp.message(F.text == "🎓 Kurslar haqida")
async def courses_handler(message: Message):
    kurslar_matni = (
        "<b>🎓 Bizning Xitoy tili kurslarimiz:</b>\n\n"
        "1. <b>Boshlang'ich daraja (HSK 1-2):</b>\n"
        "   • Davomiyligi: 3 oy\n"
        "   • Narxi: 50,000 so'm / oy\n"
        "   • Nima o'rganasiz: 300+ so'z, oddiy muloqot va alifbo.\n\n"
        "2. <b>O'rta daraja (HSK 3-4):</b>\n"
        "   • Davomiyligi: 4 oy\n"
        "   • Narxi: 100,000 so'm / oy\n"
        "   • Nima o'rganasiz: Erkin gaplashish va murakkab matnlar.\n\n"
        "Pastdagi tugma orqali kursga yozilishingiz mumkin!"
    )
    
    inline_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✍️ Kursga yozilish", url="https://t.me/sardor_officiall_88")]
        ]
    )
    
    await message.answer(kurslar_matni, reply_markup=inline_menu, parse_mode=ParseMode.HTML)

@dp.message(F.text == "📞 Biz bilan aloqa")
async def contact_handler(message: Message):
    await message.answer("Savollar bo'lsa @sardor_officiall_88 ga yozishingiz mumkin.")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
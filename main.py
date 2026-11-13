import asyncio
import logging
import sys
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8656922621:AAHpd5FuIs6vSrnzIwJXU1YDgXOyzuKDCs"

dp = Dispatcher()

# Asosiy menyu tugmalari
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇨🇳 Xitoy tili alifbosi"),
            KeyboardButton(text="📝 Pro testlar"),
        ],
        [
            KeyboardButton(text="ℹ️ Bot haqida"),
        ]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = (
        f"Salom, {html.bold(message.from_user.full_name)}! 👋\n\n"
        "Xitoy tili o'rganish botiga xush kelibsiz! Marhamat, quyidagi tugmalardan birini tanlang:"
    )
    await message.answer(text, reply_markup=main_menu, parse_mode="HTML")

@dp.message(F.text == "ℹ️ Bot haqida")
async def about_handler(message: Message):
    text = (
        "ℹ️ **Bot haqida batafsil ma'lumot**\n\n"
        "Ushbu bot xitoy tilini noldan boshlab o'rganish, HSK imtihonlariga tayyorgarlik ko'rish va o'z bilimingizni sinovdan o'tkazish uchun maxsus yaratilgan.\n\n"
        "🛠 **Asosiy imkoniyatlari:**\n"
        "• Xitoy tili alifbosi va asosiy qoidalari bilan tanishish\n"
        "• PRO darajadagi maxsus testlar va imtihon topshiriqlari\n"
        "• Qulay va tushunarli interfeys\n\n"
        "Muvaffaqiyatli o'qishni tilaymiz! 🚀"
    )
    await message.answer(text, reply_markup=main_menu, parse_mode="Markdown")

@dp.message(F.text == "🇨🇳 Xitoy tili alifbosi")
async def alphabet_handler(message: Message):
    text = (
        "🇨🇳 **Xitoy tili alifbosi va asoslari**\n\n"
        "Bilasizmi, xitoy tilida oddiy harflar yo'q. Uning o'rniga **Ierogliflar** va ularning o'qilishini bildiruvchi **Pinyin** tizimi mavjud:\n\n"
        "1. **Pinyin (Lotincha o'qilishi):** Xitoycha so'zlarni lotin harflari yordamida o'qish va talaffuz qilish uchun ishlatiladi.\n"
        "2. **Ohanglar (Tones):** Xitoy tilida 4 ta asosiy ohang bor. Ohang o'zgarsa, so'zning ma'nosi ham butunlay o'zgarib ketadi!\n\n"
        "📚 *Tez arada bu bo'limda batafsil darslar va ovozli misollar qo'shiladi!*"
    )
    await message.answer(text, reply_markup=main_menu, parse_mode="Markdown")

@dp.message(F.text == "📝 Pro testlar")
async def pro_tests_handler(message: Message):
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

# Render port talabini bajarish uchun veb-server
async def handle(request):
    return web.Response(text="Bot is running and alive!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # Veb-serverni ishga tushiramiz (Render uchun)
    await start_web_server()
    # Botni ishga tushiramiz
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

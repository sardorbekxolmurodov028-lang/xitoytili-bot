import asyncio
import logging
import sys
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

TOKEN = "8656922621:AAHpd5FuIs6vSrnzIwJXU1YDgXOyzuKDCs"

dp = Dispatcher()

# Professional va eng kerakli asosiy menyu
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💬 Kunlik iboralar"),
            KeyboardButton(text="🎯 Pro Testlar"),
        ],
        [
            KeyboardButton(text="🌐 Veb-saytimiz"),
            KeyboardButton(text="📞 Admin bilan aloqa"),
        ]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = (
        f"Salom, {html.bold(message.from_user.full_name)}! 👋\n\n"
        "🇨🇳 <b>Xitoy tili Pro</b> botiga xush kelibsiz!\n\n"
        "Bu yerda siz tilni noldan o'rganishingiz, testlar yordamida o'z bilimingizni sinashingiz va saytimizdagi qiziqarli materiallardan foydalanishingiz mumkin. Kerakli bo'limni tanlang:"
    )
    await message.answer(text, reply_markup=main_menu)

@dp.message(F.text == "💬 Kunlik iboralar")
async def daily_phrases_handler(message: Message):
    text = (
        "💬 <b>Bugungi foydali xitoycha ibora:</b>\n\n"
        "🇨🇳 <b>认识你很高兴 (Rènshi nǐ hěn gāoxìng)</b>\n"
        "🇺🇿 <b>Ma'nosi:</b> Siz bilan tanishganimdan xursandman!\n\n"
        "💡 <i>Har kuni botga kirib, yangi iboralarni yodlab boring!</i>"
    )
    await message.answer(text, reply_markup=main_menu)

@dp.message(F.text == "🎯 Pro Testlar")
async def pro_tests_handler(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧠 HSK 1 - Daraja testi", callback_data="hsk1_test")],
            [InlineKeyboardButton(text="🧠 HSK 2 - Daraja testi", callback_data="hsk2_test")]
        ]
    )
    text = (
        "🎯 <b>PRO Testlar bo'limi</b>\n\n"
        "O'z bilimingizni sinab ko'rish uchun quyidagi testlardan birini tanlang:"
    )
    await message.answer(text, reply_markup=kb)

@dp.callback_query(F.data == "hsk1_test")
async def hsk1_test(callback: CallbackQuery):
    quiz_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="A) Salom", callback_data="wrong_ans")],
            [InlineKeyboardButton(text="B) Rahmat", callback_data="correct_ans")],
            [InlineKeyboardButton(text="C) Hayr", callback_data="wrong_ans")]
        ]
    )
    await callback.message.edit_text(
        "📝 <b>HSK 1 Viktorina:</b>\n\n"
        "Xitoy tilida <b>'谢谢 (Xièxie)'</b> so'zi qanday ma'noni anglatadi?",
        reply_markup=quiz_kb
    )
    await callback.answer()

@dp.callback_query(F.data == "hsk2_test")
async def hsk2_test(callback: CallbackQuery):
    quiz_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="A) Do'st", callback_data="wrong_ans")],
            [InlineKeyboardButton(text="B) Maktab", callback_data="correct_ans")],
            [InlineKeyboardButton(text="C) Kitob", callback_data="wrong_ans")]
        ]
    )
    await callback.message.edit_text(
        "📝 <b>HSK 2 Viktorina:</b>\n\n"
        "Xitoy tilida <b>'学校 (xuéxiào)'</b> so'zining ma'nosi nima?",
        reply_markup=quiz_kb
    )
    await callback.answer()

@dp.callback_query(F.data == "correct_ans")
async def correct_handler(callback: CallbackQuery):
    await callback.message.edit_text("✅ <b>Ajoyib, to'g'ri javob!</b> 🏆\n\nBilimingizni yanada oshiring!")
    await callback.answer("To'g'ri javob!")

@dp.callback_query(F.data == "wrong_ans")
async def wrong_handler(callback: CallbackQuery):
    await callback.message.edit_text("❌ <b>Afsus, noto'g'ri javob.</b>\n\nLekin xafa bo'lmang, yana urinib ko'rishingiz mumkin! 💪")
    await callback.answer("Noto'g'ri javob")

@dp.message(F.text == "🌐 Veb-saytimiz")
async def website_handler(message: Message):
    site_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Saytga o'tish (PRO)", url="https://xitoytili-bot-1.onrender.com")]
        ]
    )
    text = (
        "🌐 <b>Rasmiy Veb-saytimiz</b>\n\n"
        "Barcha qo'shimcha darslar, lug'atlar va foydali materiallar veb-saytimizda joylashgan. Marhamat, quyidagi tugma orqali o'ting:"
    )
    await message.answer(text, reply_markup=site_kb)

@dp.message(F.text == "📞 Admin bilan aloqa")
async def contact_handler(message: Message):
    text = (
        "📞 <b>Bog'lanish uchun:</b>\n\n"
        "Savollar, takliflar yoki hamkorlik uchun adminga murojaat qiling:\n"
        "👉 @Sardorbek_Kholmurodov"
    )
    await message.answer(text, reply_markup=main_menu)

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
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

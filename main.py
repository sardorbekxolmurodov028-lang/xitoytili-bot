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

# Bot tokeni
TOKEN = "8656922621:AAHpd5fuIs6vSrnzIwjXUlYDgXOyzuKDCts"

dp = Dispatcher()

# Professional asosiy menyu (Tugmalar dizayni)
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
        f"Assalomu alaykum, {html.bold(message.from_user.full_name)}! 👋\n\n"
        "🇨🇳 <b>Xitoy tili Pro</b> rasmiy ta'lim botiga xush kelibsiz!\n\n"
        "Ushbu bot yordamida siz xitoy tilini noldan o'rganishingiz, kundalik iboralarni o'zlashtirishingiz va HSK daraja testlaridan o'tishingiz mumkin.\n\n"
        "👇 Kerakli bo'limni tanlang:"
    )
    await message.answer(text, reply_markup=main_menu)

@dp.message(F.text == "💬 Kunlik iboralar")
async def daily_phrases_handler(message: Message):
    text = (
        "💬 <b>Bugungi foydali xitoycha ibora:</b>\n\n"
        "🇨🇳 <b>认识你很高兴 (Rènshi nǐ hěn gāoxìng)</b>\n"
        "🇺🇿 <b>Ma'nosi:</b> Siz bilan tanishganimdan xursandman!\n\n"
        "📌 <i>Pinyin talaffuzi:</i> [Renshi ni hen gaosin]\n"
        "💡 <i>Tavsiya:</i> Kuniga kamida 1 tadan ibora yodlash til o'rganishni tezlashtiradi!"
    )
    await message.answer(text, reply_markup=main_menu)

@dp.message(F.text == "🎯 Pro Testlar")
async def pro_tests_handler(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧠 HSK 1 - Daraja sinovi", callback_data="hsk1_test")],
            [InlineKeyboardButton(text="🧠 HSK 2 - Daraja sinovi", callback_data="hsk2_test")]
        ]
    )
    text = (
        "🎯 <b>PRO Imtihon va Testlar markazi</b>\n\n"
        "O'z bilimingizni professional darajada sinab ko'ring. O'zingizga kerakli darajadagi testni tanlang:"
    )
    await message.answer(text, reply_markup=kb)

@dp.callback_query(F.data == "hsk1_test")
async def hsk1_test(callback: CallbackQuery):
    quiz_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="A) Salom", callback_data="wrong_ans")],
            [InlineKeyboardButton(text="B) Rahmat", callback_data="correct_ans")],
            [InlineKeyboardButton(text="C) Xayr", callback_data="wrong_ans")]
        ]
    )
    await callback.message.edit_text(
        "📝 <b>HSK 1 Daraja testi (1-savol):</b>\n\n"
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
        "📝 <b>HSK 2 Daraja testi (1-savol):</b>\n\n"
        "Xitoy tilida <b>'学校 (xuéxiào)'</b> so'zining ma'nosi nima?",
        reply_markup=quiz_kb
    )
    await callback.answer()

@dp.callback_query(F.data == "correct_ans")
async def correct_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "✅ <b>Ajoyib, javobingiz to'g'ri!</b> 🏆\n\n"
        "Siz xitoy tili asoslarini yaxshi o'zlashtirmoqdasiz. Keyingi testlarda ko'rishguncha!"
    )
    await callback.answer("To'g'ri javob! 🎉")

@dp.callback_query(F.data == "wrong_ans")
async def wrong_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "❌ <b>Afsuski, bu noto'g'ri javob.</b>\n\n"
        "Lekin tushkunlikka tushmang! Lug'atlarni takrorlab, yana urinib ko'rishingiz mumkin 💪"
    )
    await callback.answer("Noto'g'ri javob ⚠️")

@dp.message(F.text == "🌐 Veb-saytimiz")
async def website_handler(message: Message):
    site_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Rasmiy saytni ochish (PRO)", url="https://xitoytili-bot-1.onrender.com")]
        ]
    )
    text = (
        "🌐 <b>Xitoy Tili PRO Veb-sayti</b>\n\n"
        "Barcha turdagi video darsliklar, audio materiallar va qo'llanmalar bizning rasmiy platformamizda joylashgan.\n\n"
        "🔗 Saytga o'tish uchun quyidagi tugmani bosing:"
    )
    await message.answer(text, reply_markup=site_kb)

@dp.message(F.text == "📞 Admin bilan aloqa")
async def contact_handler(message: Message):
    text = (
        "📞 <b>Murojaat va Hamkorlik uchun:</b>\n\n"
        "Bot yuzasidan savollaringiz bo'lsa yoki takliflar bermoqchi bo'lsangiz, adminga yozishingiz mumkin:\n\n"
        "👉 <b>Asosiy admin:</b> @Sardorbek_Kholmurodov\n"
        "⏱ <i>Tez orada javob beramiz!</i>"
    )
    await message.answer(text, reply_markup=main_menu)

# Render platformasi talabini bajarish uchun veb-server
async def handle(request):
    return web.Response(text="Xitoy Tili Pro Bot is running smoothly!")

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
    # Veb-serverni ishga tushiramiz
    await start_web_server()
    # Botni ishga tushiramiz
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

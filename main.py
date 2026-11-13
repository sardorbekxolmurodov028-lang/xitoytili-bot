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

TOKEN = "8656922621:AAHpd5fuIs6vSrnzIwjXUlYDgXOyzuKDCts"

dp = Dispatcher()

# Yangi va foydali asosiy menyu tugmalari
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💬 Kunlik iboralar"),
            KeyboardButton(text="🎯 Tezkor viktorina"),
        ],
        [
            KeyboardButton(text="ℹ️ Bot haqida"),
            KeyboardButton(text="📞 Admin bilan aloqa"),
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
    await message.answer(text, reply_markup=main_menu)

@dp.message(F.text == "ℹ️ Bot haqida")
async def about_handler(message: Message):
    text = (
        "ℹ️ <b>Bot haqida batafsil ma'lumot</b>\n\n"
        "Ushbu bot xitoy tilini noldan boshlab o'rganish, kundalik so'zlashuv iboralarini o'zlashtirish va qiziqarli testlar orqali bilimni oshirish uchun yaratilgan.\n\n"
        "🛠 <b>Asosiy imkoniyatlari:</b>\n"
        "• 💬 Kunlik muhim iboralar va ularning Pinyin transkripsiyasi\n"
        "• 🎯 Interaktiv tezkor testlar\n"
        "• 📱 Qulay va sodda interfeys\n\n"
        "Muvaffaqiyatli o'qishni tilaymiz! 🚀"
    )
    await message.answer(text, reply_markup=main_menu)

@dp.message(F.text == "💬 Kunlik iboralar")
async def daily_phrases_handler(message: Message):
    text = (
        "💬 <b>Bugungi foydali xitoycha ibora:</b>\n\n"
        "🇨🇳 <b>你好 (Nǐ hǎo)</b>\n"
        "🇺🇿 <b>Ma'nosi:</b> Salom / Assalomu alaykum\n\n"
        "💡 <i>Izoh:</i> Xitoy tilida salomlashishning eng ommabop shakli. 'Nǐ' — sen, 'hǎo' — yaxshi degan ma'noni bildiradi."
    )
    await message.answer(text, reply_markup=main_menu)

@dp.message(F.text == "🎯 Tezkor viktorina")
async def quiz_handler(message: Message):
    quiz_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="A) Salom", callback_data="wrong")],
            [InlineKeyboardButton(text="B) Rahmat", callback_data="correct")],
            [InlineKeyboardButton(text="C) Xayr", callback_data="wrong")]
        ]
    )
    text = "🎯 <b>Mini-test:</b>\n\nXitoy tilida <b>'谢谢 (Xièxie)'</b> so'zi qanday ma'noni anglatadi?"
    await message.answer(text, reply_markup=quiz_kb)

@dp.message(F.text == "📞 Admin bilan aloqa")
async def contact_handler(message: Message):
    text = (
        "📞 <b>Bog'lanish uchun:</b>\n\n"
        "Savollar, takliflar yoki murojaatlar bo'yicha adalinga yozishingiz mumkin:\n"
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

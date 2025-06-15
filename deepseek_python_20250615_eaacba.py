import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from analysis import generate_analysis
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("""
👋 أهلاً بك في بوت التحليل الفني المتقدم!
↪️ أرسل رمز الأداة المالية مثل:
- EURUSD (فوركس)
- XAUUSD (الذهب)
- USOIL (النفط)
- GBPJPY (أزواج أخرى)

📊 سيقدم لك تحليلاً كاملاً بالمؤشرات والأنماط
""")

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("""
🆘 المساعدة:
/start - بدء البوت
/help - عرض هذه المساعدة
/analyze <رمز> - تحليل فوري (مثال: /analyze EURUSD)
""")

@dp.message(Command("health"))
async def health_check(message: types.Message):
    await message.answer("✅ البوت يعمل بشكل طبيعي")

@dp.message(Command("analyze"))
async def analyze_command(message: types.Message):
    try:
        symbol = message.text.split()[1].strip().upper()
        await process_analysis(message, symbol)
    except IndexError:
        await message.answer("⚠️ يرجى تحديد رمز الأداة. مثال: /analyze EURUSD")

@dp.message()
async def handle_message(message: types.Message):
    symbol = message.text.strip().upper()
    await process_analysis(message, symbol)

async def process_analysis(message: types.Message, symbol: str):
    await message.answer(f"⏳ جاري تحليل {symbol}...")
    result = generate_analysis(symbol)
    await message.answer(result)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
import groq
import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
TOKEN = os.getenv('TOKEN')
print(api_key)
print(TOKEN)
client = groq.Client(api_key=api_key)




dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! How can I help you?")


@dp.message()
async def echo_handler(message: Message) -> None:
    chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": message.text,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )

    await message.answer(chat_completion.choices[0].message.content)



async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


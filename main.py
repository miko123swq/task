import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from db import Database
import time


logging.basicConfig(level=logging.INFO)

bot = Bot(token='6426343658:AAGEAj1p_FPYtwhw8lTIRsBzO6E1p_YYVFY')
dp = Dispatcher()
db = Database("mydb")

@dp.message(F.text == "/start")
async def start(message:types.Message):
    if message.chat.type == "private":
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "welcome")

# @dp.message(Command("sendall"))
# async def sendall(message:types.Message):
#     if message.chat.type == "private":
#         if message.from_user.id == 6432327874:
#             text = message.text[9:]
#             users = db.get_all_users()
#             for row in users:
#                 print(row)
#                 try:
#                     await bot.send_message(chat_id=row[1], text="Spandknas")
#                 except:
#                     print(f'Ошибка: бот заблокирован для пользователя {users[0]}')




@dp.message(Command("sendall"))
async def send_all(message: types.Message):
    if message.chat.type == "private" and message.from_user.id == 6432327874:
        text = message.text[9:]
        users = db.get_all_users()


        async def send_message_to_user(user_id):
            try:
                await bot.send_message(chat_id=user_id, text="random texts")
            except Exception as e:
                print(f'Ошибка: бот заблокирован для пользователя {user_id}')

        tasks = [send_message_to_user(row[1]) for row in users]

        start_time = time.time()


        await asyncio.gather(*tasks)

        end_time = time.time()

        total_time = end_time - start_time

        print(f"Рассылка завершена. Время выполнения: {total_time} секунд.")


async def main():
    await dp.start_polling(bot)


asyncio.run(main())


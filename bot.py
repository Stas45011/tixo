import os
import asyncio
from datetime import timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список запрещённых слов
BAD_WORDS = ["дурак", "лох", "мат", "сука", "блядь"]

# === Фильтр мата ===
@dp.message()
async def filter_messages(message: types.Message):
    if message.text:
        text = message.text.lower()
        if any(word in text for word in BAD_WORDS):
            try:
                await message.delete()
                await message.answer(f"⚠️ {message.from_user.full_name}, соблюдайте правила чата!")
            except Exception as e:
                print(f"Ошибка удаления: {e}")

# === Команда /mute с указанием времени ===
@dp.message(Command("mute"))
async def mute_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("⚠️ Ответьте на сообщение пользователя, которого хотите замутить")
        return

    args = message.text.split()
    duration = None
    if len(args) > 1:
        # Пример: 1ч, 30м
        time_str = args[1]
        if "ч" in time_str:
            duration = timedelta(hours=int(time_str.replace("ч", "")))
        elif "м" in time_str:
            duration = timedelta(minutes=int(time_str.replace("м", "")))

    try:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=types.ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            ),
            until_date=(message.date + duration) if duration else None
        )
        text = f"🔇 Пользователь {message.reply_to_message.from_user.full_name} замучен"
        if duration:
            text += f" на {args[1]}"
        await message.answer(text)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

# === Команда /unmute ===
@dp.message(Command("unmute"))
async def unmute_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("⚠️ Ответьте на сообщение пользователя, которого хотите размутить")
        return
    try:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=types.ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.answer(f"✅ Пользователь {message.reply_to_message.from_user.full_name} размучен")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

# === Команда /ban ===
@dp.message(Command("ban"))
async def ban_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("⚠️ Ответьте на сообщение пользователя, которого хотите забанить")
        return
    try:
        await bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id
        )
        await message.answer(f"⛔ Пользователь {message.reply_to_message.from_user.full_name} забанен")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

# === Команда /kick ===
@dp.message(Command("kick"))
async def kick_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("⚠️ Ответьте на сообщение пользователя, которого хотите кикнуть")
        return
    try:
        await bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id
        )
        await bot.unban_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id
        )
        await message.answer(f"👢 Пользователь {message.reply_to_message.from_user.full_name} кикнут")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

# === Запуск бота ===
async def main():
    print("🤖 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

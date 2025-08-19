import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = os.getenv("TOKEN")  # Токен хранится в Railway Variables
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список запрещённых слов (можешь расширять)
BAD_WORDS = ["дурак", "лох", "мат", "сука", "блядь"]

# === Автоматический фильтр мата ===
@dp.message()
async def filter_messages(message: types.Message):
    text = message.text.lower()

    # Проверка на мат
    if any(word in text for word in BAD_WORDS):
        try:
            await message.delete()  # удаляем сообщение
            await message.answer(
                f"⚠️ {message.from_user.full_name}, соблюдайте правила чата!"
            )
        except Exception as e:
            print(f"Ошибка удаления: {e}")
        return

    # Если это команда, обработчики ниже сработают
    # Если обычное сообщение без мата → игнорируем

# === Команда /mute ===
@dp.message(Command("mute"))
async def mute_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("⚠️ Ответьте на сообщение пользователя, которого хотите замутить")
        return

    try:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=types.ChatPermissions(can_send_messages=False)
        )
        await message.answer(f"🔇 Пользователь {message.reply_to_message.from_user.full_name} замучен")
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
            permissions=types.ChatPermissions(can_send_messages=True)
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

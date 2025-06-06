from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F
from services.favorites_storage import FavoritesStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.api_client import WeatherClient

router = Router()
mal_client = WeatherClient()

# инициализируем хранилище (файл рядом с bot.py: storage/favorites.json)
storage = FavoritesStorage("storage/favorites.json")

# ---- Добавить в избранное ----
# Использование: /add_fav <word>
@router.message(Command("add_fav"))
async def cmd_add_fav(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("You need to write a word: /add_fav buy")

    word = parts[1].strip()
    # опционально можно проверить существование через mal_client.anime_exists
    await storage.add(message.from_user.id, word)
    await message.reply(f"The word {word} was added to favorites")

# ---- Список избранного ----
@router.message(Command("favs"))
async def cmd_list_fav(message: Message):
    favs = await storage.list(message.from_user.id)
    if not favs:
        return await message.reply("There are no favorites yet 🙁")
    text = "Your favorites:\n" + "\n".join(f"- {a}" for a in favs)
    # кнопки для выбора каждого:
    kb = InlineKeyboardBuilder()
    for fav in favs:
        kb.button(text=f"Choose {fav}", callback_data=f"send_word_{fav}")
    kb.adjust(1)
    await message.reply(text, reply_markup=kb.as_markup())

# Выбрать по кнопке
@router.callback_query(lambda c: c.data.startswith("send_word_"))
async def cmd_change_word(query: CallbackQuery):
    word = query.data.split("_", 2)[2]
    if len(word) < 2:
        return await query.message.answer("You need to write a word /word buy")

    response = await mal_client.get_weather(word)
    try:
        response = response[0]
        return await query.message.answer(f"Word {response['word']}\ndefinition: {response['meanings'][0]['definitions'][0]['definition']}")   
    except:
        return await query.message.answer(f"Wrong!\n Code: {response['title']}\n Message: {response['message']}")

# ---- Удалить из избранного командой ----
@router.message(Command("del_fav"))
async def cmd_remove_fav(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("You need to write a word: /add_del buy")
    word = parts[1].strip()
    await storage.remove(message.from_user.id, word)
    await message.reply(f"❌ Word {word} deleted from favorites.")




from pyrogram import Client
from pyrogram.types import Message
from defs.pokedex import get_pokedex, get_strategy


async def pokedex_msg(_: Client, message: Message):
    name = message.text.replace("图鉴", "").strip()
    text, url = await get_pokedex(name)
    if url:
        try:
            await message.reply_photo(photo=url, caption=text, quote=True)
        except:
            await message.reply(text, quote=True)
    else:
        await message.reply(text, quote=True)


async def strategy_msg(_: Client, message: Message):
    name = message.text.replace("攻略", "").strip()
    text, url = await get_strategy(name)
    if url:
        try:
            await message.reply_photo(photo=url, caption=text, quote=True)
        except:
            await message.reply(text, quote=True)
    else:
        await message.reply(text, quote=True)

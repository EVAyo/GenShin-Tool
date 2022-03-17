from pyrogram import Client
from pyrogram.types import Message
from traceback import print_exc
from defs.char_adv import char_adv, weapon_adv


async def send_char_adv(client: Client, message: Message):
    try:
        name = message.text
        for i in ["用什么", "能用啥", "怎么养"]:
            name = name.replace(i, "").strip()
        im = await char_adv(name)
        await message.reply(im, quote=True)
    except Exception as e:
        print("获取建议失败。")
        print_exc()


async def send_weapon_adv(client: Client, message: Message):
    try:
        name = message.text
        for i in ["能给谁", "给谁用", "要给谁", "谁能用"]:
            name = name.replace(i, "").strip()
        im = await weapon_adv(name)
        await message.reply(im, quote=True)
    except Exception as e:
        print("获取建议失败。")
        print_exc()

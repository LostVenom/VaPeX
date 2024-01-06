from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram import __version__ as telever
from telethon import __version__ as tlhver

from TitanXManager import BOT_NAME, BOT_USERNAME, OWNER_ID, START_IMG, SUPPORT_CHAT, pbot


@pbot.on_message(filters.command("alive"))
async def awake(_, message: Message):
    TEXT = f"**ʜᴇʏ {message.from_user.mention},\n\nᴍʏsᴇʟғ {BOT_NAME}**\n\n"
    TEXT += f"**ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀᴄʜᴀ 👻**\n\n"
    
    await message.reply_photo(
        photo=START_IMG,
        caption=TEXT,
    )


__mod_name__ = "Aʟɪᴠᴇ"

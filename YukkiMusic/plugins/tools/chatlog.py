import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import LOG_GROUP_ID
from YukkiMusic import app 
from pyrogram.errors import RPCError
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont
import asyncio, os, aiohttp
from pathlib import Path
from pyrogram.enums import ParseMode

photo = [
    "https://telegra.ph//file/22c5299e459d8f2ab3697.jpg",
]

@app.on_message(filters.new_chat_members, group=2)
async def join_watcher(_, message):    
    chat = message.chat
    link = await app.export_chat_invite_link(chat.id)
    for member in message.new_chat_members:
        if member.id == app.id:
            count = await app.get_chat_members_count(chat.id)
            msg = (
                f"📝 <b>ᴍᴜsɪᴄ ʙᴏᴛ ᴀᴅᴅᴇᴅ ɪɴ ᴀ ɴᴇᴡ ɢʀᴏᴜᴘ</b>\n\n"
                f"____________________________________\n\n"
                f"📌<b> ᴄʜᴀᴛ ɴᴀᴍᴇ:</b> {chat.title}\n"
                f"🍂<b> ᴄʜᴀᴛ ɪᴅ:</b> {chat.id}\n"
                f"🔐<b> ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ:</b> @{chat.username}\n"
                f"📈<b> ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs:</b> {count}\n"
                f"🤔<b> ᴀᴅᴅᴇᴅ ʙʏ:</b> {message.from_user.mention}"
            )
            await app.send_photo(LOG_GROUP_ID, photo=random.choice(photo), caption=msg, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"sᴇᴇ ɢʀᴏᴜᴘ👀", url=f"{link}")]
            ]))

@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        remove_by = message.from_user.mention if message.from_user else "ᴛɪᴅᴀᴋ ᴅɪᴋᴇᴛᴀʜᴜɪ"
        title = message.chat.title
        username = f"@{message.chat.username}" if message.chat.username else "ɢʀᴏᴜᴘ ᴘʀɪᴘᴀᴛ"
        chat_id = message.chat.id
        left = f"✫ <b><u>#Left_Group</u></b> ✫\n\nNama Group : {title}\n\nID Group : {chat_id}\n\nDiHapus Oleh : {remove_by}\n\nBot : @{app.username}"
        await app.send_photo(LOG_GROUP_ID, photo=random.choice(photo), caption=left)
        

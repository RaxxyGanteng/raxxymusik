from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardMarkup, InlineQueryResultArticle, 
                             InputTextMessageContent, InlineKeyboardButton, CallbackQuery)
from datetime import datetime
import pytz
import asyncio

from YukkiMusic import app  # Assuming this is how you import your bot instance

hadir_list = {}

def get_hadir_list(group_id):
    if group_id in hadir_list:
        return "\n".join([f"👤 {user['mention']} - {user['jam']}" 
                         for user in hadir_list[group_id]])
    return ""

async def reset_hadir_list():
    global hadir_list
    while True:
        await asyncio.sleep(86400) 
        hadir_list = {}

loop = asyncio.get_event_loop()
loop.create_task(reset_hadir_list())

@app.on_message(filters.command("absen") & ~filters.private)
async def absen_command(c, m):
    if m.chat.type == "private":
        await m.reply("Perintah ini hanya dapat digunakan di grup.")
        return

    group_id = m.chat.id
    group_name = m.chat.title
    user_id = m.from_user.id
    mention = m.from_user.mention
    timestamp = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%d-%m-%Y")
    jam = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")

    if group_id not in hadir_list:
        hadir_list[group_id] = []

    hadir_list[group_id].append({"user_id": user_id, "mention": mention, "jam": jam})
    hadir_text = get_hadir_list(group_id)

    text = f"Daftar hadir untuk grup {group_name} pada tanggal {timestamp}:\n{hadir_text}"

    buttons = [[InlineKeyboardButton("Tambah Hadir", switch_inline_query_current_chat=f"absen_hadir_{group_id}")]]
    keyboard = InlineKeyboardMarkup(buttons)
    
    await m.reply(text, reply_markup=keyboard)

@app.on_message(filters.command("delabsen") & ~filters.private)
async def clear_absen_command(c, m):
    if m.chat.type == "private":
        await m.reply("Perintah ini hanya dapat digunakan di grup.")
        return

    group_id = m.chat.id
    if group_id in hadir_list:
        hadir_list[group_id].clear()

    await m.reply("Semua absen berhasil dihapus.")

@app.on_inline_query()
async def absen_inline(c, iq):
    query = iq.query
    if not query.startswith("absen_hadir_"):
        return
    
    group_id = int(query.split("_")[-1])
    user_id = iq.from_user.id
    mention = iq.from_user.mention
    timestamp = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%d-%m-%Y")
    jam = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")

    if group_id not in hadir_list:
        hadir_list[group_id] = []

    if any(user['user_id'] == user_id for user in hadir_list[group_id]):
        await iq.answer("Anda sudah melakukan absen sebelumnya.", show_alert=True)
    else:
        hadir_list[group_id].append({"user_id": user_id, "mention": mention, "jam": jam})
        hadir_text = get_hadir_list(group_id)
        text = f"Daftar hadir untuk grup pada tanggal {timestamp}:\n{hadir_text}"

        buttons = [[InlineKeyboardButton("Tambah Hadir", switch_inline_query_current_chat=f"absen_hadir_{group_id}")]]
        keyboard = InlineKeyboardMarkup(buttons)

        result = InlineQueryResultArticle(
            title="Daftar Hadir",
            description=f"Daftar hadir:\n{hadir_text}",
            input_message_content=InputTextMessageContent(text),
            reply_markup=keyboard
        )

        await c.answer_inline_query(iq.id, results=[result], cache_time=0)

@app.on_callback_query(filters.regex(r"^absen_hadir_"))
async def hadir_callback(c, cq: CallbackQuery):
    group_id = int(cq.data.split("_")[-1])
    group_name = cq.message.chat.title
    user_id = cq.from_user.id
    mention = cq.from_user.mention
    timestamp = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%d-%m-%Y")
    jam = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")

    if group_id not in hadir_list:
        hadir_list[group_id] = []

    if any(user['user_id'] == user_id for user in hadir_list[group_id]):
        await cq.answer("Anda sudah melakukan absen sebelumnya.", show_alert=True)
    else:
        hadir_list[group_id].append({"user_id": user_id, "mention": mention, "jam": jam})
        hadir_text = get_hadir_list(group_id)
        text = f"Daftar hadir untuk grup {group_name} pada tanggal {timestamp}:\n{hadir_text}"
        buttons = [[InlineKeyboardButton("Tambah Hadir", switch_inline_query_current_chat=f"absen_hadir_{group_id}")]]
        keyboard = InlineKeyboardMarkup(buttons)
        await cq.edit_message_text(text, reply_markup=keyboard)
           

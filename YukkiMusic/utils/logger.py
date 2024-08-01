#
# Copyright (C) 2023-2024 by YukkiOwner@Github, < https://github.com/YukkiOwner >.
#
# This file is part of < https://github.com/YukkiOwner/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/YukkiOwner/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

from config import LOG, LOG_GROUP_ID
from YukkiMusic import app
from YukkiMusic.utils.database import is_on_off


async def play_logs(message, streamtype):
    if await is_on_off(LOG):
        if message.chat.username:
            chatusername = f"@{message.chat.username}"
        else:
            chatusername = "GC Pripat"
        logger_text = f"""
❏ <b>ᴀʀᴀʙ-ʀᴏʙᴏᴛ ᴘʟᴀʏ ʟᴏɢ</b>

❏ <b>ᴄʜᴀᴛ:</b> {message.chat.title} [`{message.chat.id}`]
├ <b>ᴜꜱᴇʀ:</b> {message.from_user.mention}
├ <b>ᴜꜱᴇʀɴᴀᴍᴇ:</b> @{message.from_user.username}
├ <b>ᴜꜱᴇʀ ɪᴅ:</b> `{message.from_user.id}`
╰ ᴄʜᴀᴛ ʟɪɴᴋ: {chatusername}

❏ <b>Qᴜᴇʀʏ:</b> {message.text}

❏ <b>ꜱᴛʀᴇᴀᴍᴛʏᴘᴇ:</b> {streamtype}"""
        if message.chat.id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    LOG_GROUP_ID,
                    f"{logger_text}",
                    disable_web_page_preview=True,
                )
            except:
                pass
        return

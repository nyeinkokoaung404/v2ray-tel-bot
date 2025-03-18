import shutil
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_IDS

def setup_restart_handler(app: Client):
    @app.on_message(filters.command(["restart", "reboot", "reload"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def restart(_, message):
        if message.from_user.id not in ADMIN_IDS:
            await message.reply_text(
                "<b>❌ You are not authorized to use this command.</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("👨🏼‍💻 Developer", url='https://t.me/nkka404'),
                            InlineKeyboardButton("⚙️ Update Channel", url="https://t.me/SmartTool404")
                        ]
                    ]
                )
            )
            return

        response = await message.reply_text(
            "<b>Restarting Bot...</b>",
            parse_mode=ParseMode.HTML
        )
        
        # Active chats handling logic here if applicable
        # Example:
        # served_chats = await get_active_chats()
        # for x in served_chats:
        #     try:
        #         await app.send_message(
        #             x,
        #             "The bot is restarting for updating purposes. Sorry for the inconvenience."
        #         )
        #         await remove_active_chat(x)
        #     except Exception:
        #         pass

        # Directories to be removed
        directories = ["downloads", "temp", "temp_media"]
        for directory in directories:
            try:
                shutil.rmtree(directory)
            except FileNotFoundError:
                pass

        # Delete the botlogs.txt file if it exists
        if os.path.exists("data.json"):
            os.remove("data.json")

        await asyncio.sleep(6)

        await response.edit(
            "<b>Bot Successfully Started! 💥</b>",
            parse_mode=ParseMode.HTML
        )
        os.system(f"kill -9 {os.getpid()} && bash start.sh")

    @app.on_message(filters.command(["stop", "kill", "off"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def stop(_, message):
        if message.from_user.id not in ADMIN_IDS:
            await message.reply_text(
                "<b>❌ You are not authorized to use this command.</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("👨🏼‍💻 Developer", url='https://t.me/nkka404'),
                            InlineKeyboardButton("⚙️ Update Channel", url="https://t.me/SmartTool404")
                        ]
                    ]
                )
            )
            return

        await message.reply_text(
            "<b>Bot Off Successfully</b>",
            parse_mode=ParseMode.HTML
        )
        os.system("pkill -f main.py")

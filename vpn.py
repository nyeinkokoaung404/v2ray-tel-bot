import os
import re
import base64
import qrcode
import requests
from io import BytesIO
from PIL import Image
from pyzbar.pyzbar import decode
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram.enums import ParseMode, ChatType
from adminpanel import setup_adminpanel_handlers
import asyncio
from keys import *
from utils import account_info
from config import API_ID, API_HASH, BOT_TOKEN

# State management
user_state = {}
ACCOUNT_LINK_INPUT = 1
AFTER_QR_SENT = 2

# Application Information
WHAT_APP = {
    "Nekoray": {
        "name": "Nekoray",
        "desc": "Nekoray",
        "image_path": "images/nekoray.jpg"
    },
    "V2rayNG": {
        "name": "V2rayNG",
        "desc": "V2rayNG",
        "image_path": "images/v2rayng.jpg"
    },
    "OneClick": {
        "name": "OneClick",
        "desc": "OneClick",
        "image_path": "images/oneclick.jpg"
    },
    "NapsterNetV": {
        "name": "NapsterNetV",
        "desc": "NapsterNetV",
        "image_path": "images/napsternetv.jpg"
    },
}

# Helper Functions
def is_base64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False

def is_url(text):
    url_pattern = re.compile(
        r'^(https?://)?'  # http:// or https://
        r'([\da-z\.-]+)\.([a-z\.]{2,6})'  # domain
        r'([/\w \.-]*)*/?$',  # path
        re.IGNORECASE
    )
    return url_pattern.match(text) is not None

# Initialize Pyrogram Client
app = Client("cus_vpn_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

setup_adminpanel_handlers(app)

# Command Handlers
@app.on_message(filters.command(["start"], prefixes=["/", "."]) & (filters.private | filters.group))
async def start_message(client: Client, message: Message):
    chat_id = message.chat.id

    # Animation messages
    animation_message = await client.send_message(chat_id, "<b>Starting V2Ray Checker...</b>", parse_mode=ParseMode.HTML)
    await asyncio.sleep(0.4)
    await client.edit_message_text(chat_id, animation_message.id, "<b>Generating Session Keys Please Wait...</b>", parse_mode=ParseMode.HTML)
    await asyncio.sleep(0.4)
    await client.delete_messages(chat_id, animation_message.id)

    if message.chat.type == ChatType.PRIVATE:
        # Extract full name in private chat
        full_name = "User"
        if message.from_user:
            first_name = message.from_user.first_name or ""
            last_name = message.from_user.last_name or ""
            full_name = f"{first_name} {last_name}".strip()

        # Private Chat Message
        response_text = (
            f"<b>Hi {full_name}! Welcome To This Bot</b>\n"
            "<b>━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
            "<b><a href='tg://user?id=1273841502'>V2Ray Checker</a></b>: Subscription Link, QRCode, UUID, Vless, Vmess, Shadowsocks, and remark တို့ကို အသုံးပြု၍ အကောင့်အချက်အလက်ကို ရယူပါ။\n"
            "<b>━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
            "<b>Don't Forget To <a href='https://t.me/premium_channel_404'>Join Here</a> For Updates!</b>"
        )

    # Send message with inline buttons
    await client.send_message(
        chat_id=message.chat.id,
        text=response_text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

@app.on_message(filters.command(["help"], prefixes=["/", "."]))
async def help_command_handler(client: Client, message: Message):
    help_text = """
ကျေးဇူးပြု၍ အောက်ပါ commands များကို အသုံးပြုပါ:
/start - Bot ကို စတင်ရန်
/help - အကူအညီရယူရန်
/what - ဆော့ဝဲလ်အကြောင်းသိရန်
"""
    await message.reply_text(help_text)

@app.on_message(filters.command(["what"], prefixes=["/", "."]))
async def what_command_handler(client: Client, message: Message):
    keyboard = []
    for what_app, what_app_dict in WHAT_APP.items():
        keyboard.append([InlineKeyboardButton(what_app_dict["name"], callback_data=f"what_app|{what_app}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text("ကျေးဇူးပြု၍ ဆော့ဝဲလ်တစ်ခုကို ရွေးချယ်ပါ။", reply_markup=reply_markup)

# Callback Query Handler
@app.on_callback_query(filters.regex("^what_app"))
async def what_app_callback_handler(client: Client, callback_query: CallbackQuery):
    what_app = callback_query.data.split("|")[1]
    desc_app = f"{WHAT_APP[what_app]['desc']}"
    image_path = f"{WHAT_APP[what_app]['image_path']}"

    await callback_query.message.reply_photo(photo=image_path, caption=desc_app)
    await callback_query.message.delete()

# Account Information Handler
@app.on_message(filters.text | filters.photo)
async def account_info_handler(client: Client, message: Message):
    if message.photo:
        # Decode QR Code from photo
        photo = await message.download()
        img = Image.open(photo)
        decode_objects = decode(img)

        if decode_objects:
            decode_qrcode = decode_objects[0].data.decode("utf-8")
            acc_info = account_info(decode_qrcode)
        else:
            await message.reply_text("QRCode ပေးပို့ပါ။")
            return
    else:
        # Process text message
        client_msg = message.text

        if is_url(client_msg):
            try:
                res = requests.get(client_msg)
                res_content = res.content
                if is_base64(res_content):
                    accounts = base64.b64decode(res_content).decode('utf-8')
                else:
                    accounts = res_content.decode('utf-8')

                client_msg = accounts.split()[0]
            except requests.exceptions.RequestException as e:
                await message.reply_text("သင်၏ Sub Link ကို ဖတ်ရာတွင် ပြဿနာရှိနေသည်။")
                return

        acc_info = account_info(client_msg)

    if acc_info == 'not found':
        await message.reply_text("အကောင့်အချက်အလက်မတွေ့ပါ။")
        return

    status, account_name, up, down, used, total, traffic_remaining, expiry = acc_info
    rem_time, expiry = expiry

    keyboard = [
        [InlineKeyboardButton(f"အကောင့်အမည်: {account_name}", callback_data='1')],
        [InlineKeyboardButton(f"⚙️ အကောင့်အခြေအနေ: {status}", callback_data='1')],
        [
            InlineKeyboardButton(f"⬆️ {up} :Upload", callback_data='1'),
            InlineKeyboardButton(f"⬇️ {down} :Download", callback_data='1')
        ],
        [InlineKeyboardButton(f"{used} :အသုံးပြုမှူ့နှုန်း⏳", callback_data='1')],
        [InlineKeyboardButton(f"📡 လက်ကျန်ပမာဏ : {traffic_remaining}", callback_data='1')],
        [InlineKeyboardButton(f"🕒 ကျန်ရှိအချိန် : {rem_time}", callback_data='1')],
        [InlineKeyboardButton(f"🌐 စုစုပေါင်း: {total}", callback_data='1')],
        [InlineKeyboardButton(f"{expiry} 🔚", callback_data='1')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text("💠 သင်၏ဝန်ဆောင်မှုအချက်အလက် 💠", reply_markup=reply_markup)

# Run the Bot
if __name__ == "__main__":
    print("🚀 Telegram bot is running...")
    app.run()
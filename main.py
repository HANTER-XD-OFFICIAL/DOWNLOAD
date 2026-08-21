import os
import telebot
import requests
import json
import io
import re
from flask import Flask
from threading import Thread
from telebot import types

# ═══════════════════════════
# SYSTEM ARCHITECTURE CONFIG
# ═══════════════════════════
app = Flask('')
@app.route('/')
def home(): return "🛡️ ULTRA-SAVE PRO CORE ENGINE: OPERATIONAL"
def run_server(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))

# SYSTEM IDENTITY & CREDENTIALS
TOKEN = "8523953940:AAGzJRfKPepZypt320Wee-VReY_2KqOeYyM"
ADMIN_ID = 6204875999
bot = telebot.TeleBot(TOKEN)

# ASSETS & DATABASE NODES
USER_DB = "users.json"
BAN_DB = "blacklist.json"
VOICE_PACK_URL = "https://raw.githubusercontent.com/HANTER-XD-OFFICIAL/DOWNLOAD/main/bg-music.mp3"

# ═══════════════════════════
# DATABASE CORE LOGIC
# ═══════════════════════════
def load_db(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f: return json.load(f)
        except: return []
    return []

def save_db(file_path, data):
    with open(file_path, "w") as f: json.dump(data, f)

def is_authorized(user_id):
    blacklist = load_db(BAN_DB)
    return user_id not in blacklist

# ═══════════════════════════
# CORE API DECRYPTION (XOR - FROM HTML FILE)
# ═══════════════════════════
def decrypt_api_nodes():
    _k = 0x5A
    _fa = [0x32, 0x5A, 0x2E, 0x5A, 0x2E, 0x5A, 0x2A, 0x5A, 0x29, 0x5A, 0x60, 0x5A, 0x75, 0x5A, 0x75, 0x5A, 0x3C, 0x5A, 0x3C, 0x5A, 0x77, 0x5A, 0x33, 0x5A, 0x33, 0x5A, 0x74, 0x5A, 0x35, 0x5A, 0x34, 0x5A, 0x28, 0x5A, 0x3F, 0x5A, 0x34, 0x5A, 0x3E, 0x5A, 0x3F, 0x5A, 0x28, 0x5A, 0x74, 0x5A, 0x39, 0x5A, 0x35, 0x5A, 0x37, 0x5A]
    return "".join([chr(x ^ _k) for x in _fa if x != _k])

FB_BASE_NODE = decrypt_api_nodes()

# ═══════════════════════════
# PREMIUM INTERFACE BUILDER
# ═══════════════════════════
def get_main_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_dl = types.KeyboardButton("📥 Start Download")
    btn_sup = types.KeyboardButton("☎️ Support")
    markup.row(btn_dl, btn_sup)
    if user_id == ADMIN_ID: markup.row(types.KeyboardButton("📊 System Analytics"))
    return markup

# ═══════════════════════════
# BOT HANDLERS
# ═══════════════════════════

@bot.message_handler(commands=['start'])
def system_boot(message):
    user_id = message.chat.id
    if not is_authorized(user_id): return
    
    welcome_protocol = (
        f"🛡️ *ULTRA-SAVE PRO | CORE V2.5*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ Assalamu Alaikum, {message.from_user.first_name}!\n\n"
        f"Welcome to the elite media extraction node. Stay righteous and "
        f"perform your Salah on time. Success is only from Allah.\n\n"
        f"👤 Architect: [HANTER-XD](https://t.me/HANTER_XD_OFFICIAL)\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ Instruction: Use the menu buttons below to interact."
    )
    bot.send_message(user_id, welcome_protocol, parse_mode='Markdown', reply_markup=get_main_keyboard(user_id), disable_web_page_preview=True)
    
    try:
        audio_stream = requests.get(VOICE_PACK_URL).content
        bot.send_audio(user_id, io.BytesIO(audio_stream), caption="🎙️ *System Identity Verified*")
    except: pass

@bot.message_handler(func=lambda message: True)
def central_handler(message):
    chat_id = message.chat.id
    if not is_authorized(chat_id): return
    text = message.text

    if "Start Download" in text:
        msg = bot.send_message(chat_id, "✅ *Protocol Ready!*\nPlease paste your video link now:")
        bot.register_next_step_handler(msg, process_extraction)
    
    elif "Support" in text:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✈️ Telegram Support", url="https://t.me/HANTER_XD_OFFICIAL"))
        bot.send_message(chat_id, "🛡️ *Support Gateway Online:*", reply_markup=markup)
    
    elif "Analytics" in text:
        if chat_id == ADMIN_ID:
            count = len(load_db(USER_DB))
            bot.send_message(ADMIN_ID, f"📊 *Total Users:* `{count}`")

# ═══════════════════════════
# EXTRACTION ENGINE (CLEAN URL LOGIC)
# ═══════════════════════════
def process_extraction(message):
    input_text = message.text.strip()
    chat_id = message.chat.id
    
    # URL Cleaner: Extract ONLY the URL from the text (Fixes TikTok Lite issue)
    url_match = re.search(r'(https?://[^\s]+)', input_text)
    if not url_match:
        bot.send_message(chat_id, "❌ *Error:* No valid URL detected.")
        return
    url = url_match.group(1)

    wait_log = bot.send_message(chat_id, "⚡ *Decrypting Media Node...*", parse_mode='Markdown')
    try:
        # 1. TIKTOK (Exact Same API as your HTML)
        if "tiktok.com" in url:
            res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
            if res.get('code') == 0:
                data = res['data']
                bot.send_video(chat_id, data['play'], caption=f"✅ *TikTok Success*\n👤 @{data['author']['unique_id']}")
                if data.get('music'): bot.send_audio(chat_id, data['music'], caption="🎵 *Audio Pack*")
            else: raise Exception("API Error")

        # 2. FACEBOOK (Same POST logic as your HTML)
        elif "facebook.com" in url or "fb.watch" in url:
            res = requests.post(f"{FB_BASE_NODE}/api/download", json={"url": url}).json()
            v_url = res.get('hdplay') or res.get('play')
            bot.send_video(chat_id, v_url, caption="✅ *Facebook HD Decrypted*")

        # 3. YOUTUBE / INSTAGRAM
        elif any(x in url for x in ["youtube.com", "youtu.be", "instagram.com"]):
            res = requests.get(f"https://social-downloader-api.vercel.app/api/download?url={url}").json()
            bot.send_video(chat_id, res['play'], caption="✅ *Extraction Successful*")

    except:
        bot.send_message(chat_id, "⚠️ *Failure:* Content Private or Restricted.")
    finally:
        bot.delete_message(chat_id, wait_log.message_id)

if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.remove_webhook()
    bot.infinity_polling()
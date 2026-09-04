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
TOKEN = "8523953940:AAGFPtYqMl2FtqbZlVrHS35H3B-SnBFHQ7g"
ADMIN_ID = 6204875999
bot = telebot.TeleBot(TOKEN)

# 🟢 YOUR WORKER API NODE
WORKER_API = "https://muddy-scene-0ff7.alexraselchodhury.workers.dev/api/download"

USER_DB = "users.json"
BAN_DB = "blacklist.json"
VOICE_PACK_URL = "https://raw.githubusercontent.com/HANTER-XD-OFFICIAL/DOWNLOAD/main/bg-music.mp3"

# ═══════════════════════════
# DATA UTILITIES
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
# KEYBOARDS
# ═══════════════════════════
def get_main_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("📥 Start Download"), types.KeyboardButton("☎️ Support"))
    if user_id == ADMIN_ID: markup.row(types.KeyboardButton("📊 System Analytics"))
    return markup

# ═══════════════════════════
# MISSION HANDLERS
# ═══════════════════════════

@bot.message_handler(commands=['start'])
def system_boot(message):
    user_id = message.chat.id
    if not is_authorized(user_id): return
    
    users = load_db(USER_DB)
    if user_id not in users:
        users.append(user_id)
        save_db(USER_DB, users)
        bot.send_message(ADMIN_ID, f"🔔 *NEW ACCESS:* {message.from_user.first_name} (ID: `{user_id}`)")

    welcome_protocol = (
        f"🛡️ *ULTRA-SAVE PRO | CORE V2.5*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ Assalamu Alaikum, {message.from_user.first_name}!\n\n"
        f"Professional media extraction system. Send me any link and I will "
        f"send you the video file directly here.\n\n"
        f"👤 Architect: [HANTER-XD](https://t.me/HANTER_XD_OFFICIAL)\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(user_id, welcome_protocol, parse_mode='Markdown', reply_markup=get_main_keyboard(user_id))
    
    try:
        audio_stream = requests.get(VOICE_PACK_URL).content
        bot.send_audio(user_id, io.BytesIO(audio_stream), caption="🎙️ *Identity Verified*")
    except: pass

@bot.message_handler(func=lambda message: True)
def central_handler(message):
    chat_id = message.chat.id
    if not is_authorized(chat_id): return
    text = message.text

    if "Start Download" in text:
        msg = bot.send_message(chat_id, "✅ *Protocol Ready!*\nPlease send your video link now:")
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
# DIRECT FILE DELIVERY ENGINE
# ═══════════════════════════
def process_extraction(message):
    input_text = message.text.strip()
    chat_id = message.chat.id
    
    if "Support" in input_text or "Start Download" in input_text or "Analytics" in input_text:
        central_handler(message); return

    # URL Cleaner
    url_match = re.search(r'(https?://[^\s]+)', input_text)
    if not url_match:
        bot.send_message(chat_id, "❌ *Error:* No valid link detected.")
        return
    url = url_match.group(1)

    wait_log = bot.send_message(chat_id, "⚡ *Extracting Video File...*", parse_mode='Markdown')
    
    try:
        # Requesting your Worker API
        res = requests.post(WORKER_API, json={"url": url}, timeout=30).json()

        # Get direct links from your API response
        video_url = res.get('hdplay') or res.get('play')
        audio_url = res.get('music')
        images = res.get('images')

        if video_url:
            # ✅ DIRECTLY SENDING THE VIDEO FILE TO TELEGRAM
            bot.send_video(
                chat_id, 
                video_url, 
                caption=f"✅ *Success!* Your video is ready.\n\n_System by HANTER-XD_",
                parse_mode='Markdown'
            )
            if audio_url:
                bot.send_audio(chat_id, audio_url, caption="🎵 *Audio Track*")
        
        elif images:
            # Handle TikTok Slideshows
            for img in images:
                bot.send_photo(chat_id, img)
            bot.send_message(chat_id, "✅ *Slideshow Delivered.*")
            
        else:
            bot.send_message(chat_id, "⚠️ *Error:* API could not fetch playable media.")

    except Exception as e:
        bot.send_message(chat_id, "⚠️ *Failure:* Unable to process this link. Ensure it is public.")
    finally:
        bot.delete_message(chat_id, wait_log.message_id)

# ═══════════════════════════
# EXECUTION
# ═══════════════════════════
if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.remove_webhook()
    bot.infinity_polling()

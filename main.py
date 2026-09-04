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
def home():
    return "🛡️ ULTRA-SAVE PRO CORE ENGINE: OPERATIONAL"

def run_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))

# SYSTEM IDENTITY & CREDENTIALS
# 🟢 Final Token Integrated
TOKEN = "8523953940:AAGFPtYqMl2FtqbZlVrHS35H3B-SnBFHQ7g"
ADMIN_ID = 6204875999
bot = telebot.TeleBot(TOKEN)

# 🟢 YOUR UNIVERSAL WORKER API NODE
WORKER_API = "https://muddy-scene-0ff7.alexraselchodhury.workers.dev/api/download"

# ASSETS & DATABASE NODES
USER_DB = "users.json"
BAN_DB = "blacklist.json"
VOICE_PACK_URL = "https://raw.githubusercontent.com/HANTER-XD-OFFICIAL/DOWNLOAD/main/bg-music.mp3"

# ═══════════════════════════
# CORE DATA PERSISTENCE
# ═══════════════════════════
def load_db(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except: return []
    return []

def save_db(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f)

def register_system_access(user_id):
    users = load_db(USER_DB)
    if user_id not in users:
        users.append(user_id)
        save_db(USER_DB, users)
        return True 
    return False

def is_authorized(user_id):
    blacklist = load_db(BAN_DB)
    return user_id not in blacklist

# ═══════════════════════════
# PREMIUM INTERFACE BUILDER
# ═══════════════════════════
def get_main_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_dl = types.KeyboardButton("📥 Start Download")
    btn_sup = types.KeyboardButton("☎️ Support")
    markup.row(btn_dl, btn_sup)
    if user_id == ADMIN_ID:
        btn_adm = types.KeyboardButton("📊 System Analytics")
        markup.row(btn_adm)
    return markup

# ═══════════════════════════
# MISSION HANDLERS
# ═══════════════════════════

@bot.message_handler(commands=['start'])
def system_boot(message):
    user_id = message.chat.id
    if not is_authorized(user_id):
        bot.send_message(user_id, "❌ *System Alert: Access Forbidden.*")
        return

    first_name = message.from_user.first_name
    is_new = register_system_access(user_id)
    
    welcome_protocol = (
        f"🛡️ *ULTRA-SAVE PRO | CORE V2.5*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ Assalamu Alaikum, {first_name}!\n\n"
        f"Welcome to the elite media extraction node. Stay righteous "
        f"and perform your Salah on time. Success is only from Allah.\n\n"
        f"👤 Architect: [HANTER-XD](https://t.me/HANTER_XD_OFFICIAL)\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ Instruction: Use the menu buttons below to interact."
    )
    
    bot.send_message(user_id, welcome_protocol, parse_mode='Markdown', reply_markup=get_main_keyboard(user_id), disable_web_page_preview=True)
    
    # 🎙️ SEND SYSTEM VOICE PACK (DIRECT BUFFER)
    try:
        audio_stream = requests.get(VOICE_PACK_URL).content
        audio_file = io.BytesIO(audio_stream)
        audio_file.name = "system-voice.mp3"
        bot.send_audio(user_id, audio_file, caption="🎙️ *System Identity Verified*")
    except: pass

    if is_new:
        bot.send_message(ADMIN_ID, f"🔔 *NEW ACCESS GRANTED:* {first_name} (ID: `{user_id}`)")

@bot.message_handler(commands=['ban'])
def ban_handler(message):
    if message.chat.id == ADMIN_ID:
        try:
            tid = int(message.text.split()[1])
            bl = load_db(BAN_DB); bl.append(tid); save_db(BAN_DB, bl)
            bot.reply_to(message, f"✅ User `{tid}` blacklisted.")
        except: bot.reply_to(message, "Usage: `/ban ID`")

@bot.message_handler(commands=['unblock'])
def unblock_handler(message):
    if message.chat.id == ADMIN_ID:
        try:
            tid = int(message.text.split()[1])
            bl = load_db(BAN_DB)
            if tid in bl: bl.remove(tid); save_db(BAN_DB, bl)
            bot.reply_to(message, f"✅ Access restored for `{tid}`.")
        except: bot.reply_to(message, "Usage: `/unblock ID`")

# ═══════════════════════════
# MENU & EXTRACTION LOGIC
# ═══════════════════════════
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
            bot.send_message(ADMIN_ID, f"📊 *LIVE ANALYTICS*\n━━━━━━━━━━━━━━\n👥 Total Users: `{count}`", parse_mode='Markdown')

    elif text.startswith("http"):
        bot.reply_to(message, "❌ *Blocked:* You must click *📥 Start Download* first.", parse_mode='Markdown')

# ═══════════════════════════
# UNIFIED EXTRACTION ENGINE (UNIVERSAL WORKER)
# ═══════════════════════════
def process_extraction(message):
    input_text = message.text.strip()
    chat_id = message.chat.id
    
    # Allow user to switch back to menu buttons
    if "Support" in input_text or "Start Download" in input_text or "Analytics" in input_text:
        central_handler(message)
        return

    # URL Cleaner (Extract ONLY the URL to fix shared text issues)
    url_match = re.search(r'(https?://[^\s]+)', input_text)
    if not url_match:
        bot.send_message(chat_id, "❌ *Error:* No valid URL detected.")
        return
    url = url_match.group(1)

    wait_log = bot.send_message(chat_id, "⚡ *Decrypting Universal Media Node...*", parse_mode='Markdown')
    try:
        # POST Request to your specific Worker API
        payload = {"url": url}
        res = requests.post(WORKER_API, json=payload).json()

        video_url = res.get('hdplay') or res.get('play')
        audio_url = res.get('music')

        if video_url:
            caption = f"✅ *Extraction Successful*\n\n🔗 [Source Link]({url})\n\n_Engineered by HANTER-XD_"
            bot.send_video(chat_id, video_url, caption=caption, parse_mode='Markdown')
            if audio_url:
                bot.send_audio(chat_id, audio_url, caption="🎵 *Audio Core Extracted*")
        
        elif res.get('images'):
            # TikTok Slideshow Handling
            for img in res.get('images'):
                bot.send_photo(chat_id, img)
            bot.send_message(chat_id, "✅ *Slideshow Nodes Extracted.*")
            
        else:
            raise Exception("No playable media found")

    except Exception:
        bot.send_message(chat_id, "⚠️ *Failure:* Content Private, Dead, or Node Restricted.")
    finally:
        bot.delete_message(chat_id, wait_log.message_id)

# ═══════════════════════════
# EXECUTION START
# ═══════════════════════════
if __name__ == "__main__":
    Thread(target=run_server).start()
    print("ULTRA-SAVE PRO SYSTEM: ONLINE")
    
    # Safety reset to clear conflict error 409
    bot.remove_webhook()
    bot.infinity_polling()

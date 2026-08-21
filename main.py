import os
import telebot
import requests
import json
import io
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
TOKEN = "8523953940:AAGzJRfKPepZypt320Wee-VReY_2KqOeYyM"
ADMIN_ID = 6204875999
bot = telebot.TeleBot(TOKEN)

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
# CORE API DECRYPTION (XOR)
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
        f"👤 Architect: [HANTER-XD OFFICIAL](https://t.me/HANTER_XD_OFFICIAL)\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ Instruction: Use the menu buttons below to interact."
    )
    
    bot.send_message(user_id, welcome_protocol, parse_mode='Markdown', reply_markup=get_main_keyboard(user_id), disable_web_page_preview=True)
    
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
        # 🟢 DIRECT TELEGRAM LINK REDIRECTION
        markup = types.InlineKeyboardMarkup()
        tg_link = types.InlineKeyboardButton("🚀 Open Developer Profile", url="https://t.me/HANTER_XD_OFFICIAL")
        markup.add(tg_link)
        
        bot.send_message(
            chat_id, 
            "🛡️ *Identity Vault: Secure Support Node*\n\nClick the button below to open a direct encrypted chat with the developer on Telegram.",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    
    elif "Analytics" in text:
        if chat_id == ADMIN_ID:
            count = len(load_db(USER_DB))
            bot.send_message(ADMIN_ID, f"📊 *LIVE ANALYTICS*\n━━━━━━━━━━━━━━\n👥 Total Users: `{count}`", parse_mode='Markdown')

    elif text.startswith("http"):
        bot.reply_to(message, "❌ *Blocked:* You must click *📥 Start Download* first.", parse_mode='Markdown')

# ═══════════════════════════
# EXTRACTION ENGINE
# ═══════════════════════════
def process_extraction(message):
    url = message.text.strip()
    chat_id = message.chat.id
    
    if "Support" in url or "Start Download" in url or "Analytics" in url:
        central_handler(message)
        return

    if not url.startswith("http"):
        bot.send_message(chat_id, "❌ *Error:* Invalid Link. Extraction Terminated.")
        return

    wait_log = bot.send_message(chat_id, "⚡ *Decrypting Media Node...*", parse_mode='Markdown')
    try:
        # 1. TIKTOK
        if "tiktok.com" in url:
            res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
            data = res['data']
            caption = f"✅ *TikTok HD Success*\n\n👤 {data['author']['nickname']}\n🔗 [Source Link]({url})"
            bot.send_video(chat_id, data['play'], caption=caption, parse_mode='Markdown')
        
        # 2. YT / IG
        elif any(x in url for x in ["youtube.com", "youtu.be", "instagram.com"]):
            res = requests.get(f"https://social-downloader-api.vercel.app/api/download?url={url}").json()
            bot.send_video(chat_id, res['play'], caption="✅ *Extraction Successful*", parse_mode='Markdown')
        
        # 3. FACEBOOK
        elif any(x in url for x in ["facebook.com", "fb.watch", "fb.gg"]):
            res = requests.post(f"{FB_BASE_NODE}/api/download", json={"url": url}).json()
            v_url = res.get('hdplay') or res.get('play')
            bot.send_video(chat_id, v_url, caption="✅ *Facebook HD Decrypted*", parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "❌ *Protocol Error: Unknown Node.*")
    except:
        bot.send_message(chat_id, "⚠️ *Failure:* Content Private or Restricted.")
    finally:
        bot.delete_message(chat_id, wait_log.message_id)

# ═══════════════════════════
# EXECUTION START
# ═══════════════════════════
if __name__ == "__main__":
    Thread(target=run_server).start()
    print("ULTRA-SAVE PRO SYSTEM: ONLINE")
    
    bot.remove_webhook()
    bot.infinity_polling()
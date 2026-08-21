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
TOKEN = "8523953940:AAHJqzNbyPWK-aVEuotVks03kWJCCiloogo"
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
# INTERFACE BUILDER
# ═══════════════════════════
def get_main_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_dl = types.KeyboardButton("Start Download")
    btn_sup = types.KeyboardButton("Support")
    if user_id == ADMIN_ID:
        btn_adm = types.KeyboardButton("Analytics")
        markup.add(btn_dl, btn_sup, btn_adm)
    else:
        markup.add(btn_dl, btn_sup)
    return markup

def get_support_vault():
    markup = types.InlineKeyboardMarkup(row_width=2)
    tg = types.InlineKeyboardButton("✈️ Telegram", url="https://t.me/HANTER_XD_OFFICIAL")
    fb = types.InlineKeyboardButton("👤 Facebook", url="https://www.facebook.com/md.rasel.7.8.2.3.4")
    wa = types.InlineKeyboardButton("💬 WhatsApp", url="https://wa.me/8801882278234")
    ig = types.InlineKeyboardButton("📸 Instagram", url="https://instagram.com/mdrasel054281")
    mail = types.InlineKeyboardButton("📧 Contact Gmail", url="mailto:alexraselchodhury@gmail.com")
    markup.add(tg, fb, wa, ig, mail)
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
        f"Welcome to the high-performance media extraction node. Stay righteous "
        f"and perform your Salah on time. Success is only from Allah.\n\n"
        f"👤 Architect: [HANTER-XD](https://t.me/HANTER_XD_OFFICIAL)\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ Instruction: Use the bottom menu bar to interact with the core."
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

# ADMIN FIREWALL COMMANDS
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
        bot.send_message(chat_id, "✅ *Protocol Ready!*\nPlease paste your video link now:")
    
    elif "Support" in text:
        bot.send_message(chat_id, "🛡️ *Identity Vault Support Node:*", reply_markup=get_support_vault())
    
    elif "Analytics" in text:
        if chat_id == ADMIN_ID:
            count = len(load_db(USER_DB))
            bot.send_message(ADMIN_ID, f"📊 *LIVE ANALYTICS*\n━━━━━━━━━━━━━━\n👥 Total Users: `{count}`", parse_mode='Markdown')

    elif text.startswith("http"):
        wait_log = bot.send_message(chat_id, "⚡ *Decrypting Media Node...*", parse_mode='Markdown')
        try:
            # 1. TIKTOK
            if "tiktok.com" in text:
                res = requests.get(f"https://www.tikwm.com/api/?url={text}").json()
                bot.send_video(chat_id, res['data']['play'], caption="✅ *TikTok HD Success*")
            
            # 2. YT / IG
            elif any(x in text for x in ["youtube.com", "youtu.be", "instagram.com"]):
                res = requests.get(f"https://social-downloader-api.vercel.app/api/download?url={text}").json()
                bot.send_video(chat_id, res['play'], caption="✅ *Extraction Successful*")
            
            # 3. FACEBOOK
            elif any(x in text for x in ["facebook.com", "fb.watch", "fb.gg"]):
                res = requests.post(f"{FB_BASE_NODE}/api/download", json={"url": text}).json()
                v_url = res.get('hdplay') or res.get('play')
                bot.send_video(chat_id, v_url, caption="✅ *Facebook HD Decrypted*")
            
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
    
    # skip_pending_updates=True resolves the 409 Conflict Error
    bot.infinity_polling(skip_pending_updates=True)
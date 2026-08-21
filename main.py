import os
import telebot
import requests
import json
import io
from flask import Flask
from threading import Thread
from telebot import types

# ═══════════════════════════
# SYSTEM CORE ARCHITECTURE
# ═══════════════════════════
app = Flask('')
@app.route('/')
def home(): return "🛡️ ULTRA-SAVE PRO CORE ENGINE: OPERATIONAL"
def run_server(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))

# SYSTEM IDENTITY & SECURITY
TOKEN = "8523953940:AAGzJRfKPepZypt320Wee-VReY_2KqOeYyM"
ADMIN_ID = 6204875999
bot = telebot.TeleBot(TOKEN)

# DATABASES & ASSETS
USER_DB = "users.json"
BAN_DB = "blacklist.json"
# 🔊 Your Voice Pack URL
VOICE_PACK_URL = "https://raw.githubusercontent.com/HANTER-XD-OFFICIAL/DOWNLOAD/main/bg-music.mp3"

# ═══════════════════════════
# DATABASE LOGIC
# ═══════════════════════════
def load_db(file):
    if os.path.exists(file):
        try:
            with open(file, "r") as f: return json.load(f)
        except: return []
    return []

def save_db(file, data):
    with open(file, "w") as f: json.dump(data, f)

def register_system_user(user_id):
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
def decrypt_nodes():
    _k = 0x5A
    _fa = [0x32, 0x5A, 0x2E, 0x5A, 0x2E, 0x5A, 0x2A, 0x5A, 0x29, 0x5A, 0x60, 0x5A, 0x75, 0x5A, 0x75, 0x5A, 0x3C, 0x5A, 0x3C, 0x5A, 0x77, 0x5A, 0x33, 0x5A, 0x33, 0x5A, 0x74, 0x5A, 0x35, 0x5A, 0x34, 0x5A, 0x28, 0x5A, 0x3F, 0x5A, 0x34, 0x5A, 0x3E, 0x5A, 0x3F, 0x5A, 0x28, 0x5A, 0x74, 0x5A, 0x39, 0x5A, 0x35, 0x5A, 0x37, 0x5A]
    return "".join([chr(x ^ _k) for x in _fa if x != _k])

FB_BASE_NODE = decrypt_nodes()

# ═══════════════════════════
# INTERFACE BUILDER
# ═══════════════════════════
def get_main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_dl = types.KeyboardButton("Start Download")
    btn_sup = types.KeyboardButton("Support")
    if user_id == ADMIN_ID:
        btn_adm = types.KeyboardButton("Analytics")
        markup.add(btn_dl, btn_sup, btn_adm)
    else:
        markup.add(btn_dl, btn_sup)
    return markup

def get_support_inline():
    markup = types.InlineKeyboardMarkup(row_width=2)
    tg = types.InlineKeyboardButton("✈️ Telegram", url="https://t.me/HANTER_XD_OFFICIAL")
    fb = types.InlineKeyboardButton("👤 Facebook", url="https://www.facebook.com/md.rasel.7.8.2.3.4")
    wa = types.InlineKeyboardButton("💬 WhatsApp", url="https://wa.me/8801882278234")
    ig = types.InlineKeyboardButton("📸 Instagram", url="https://instagram.com/mdrasel054281")
    mail = types.InlineKeyboardButton("📧 Gmail", url="mailto:alexraselchodhury@gmail.com")
    markup.add(tg, fb, wa, ig, mail)
    return markup

# ═══════════════════════════
# BOT HANDLERS
# ═══════════════════════════

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.chat.id
    if not is_authorized(user_id):
        bot.send_message(user_id, "❌ *System Alert: Access Denied.*")
        return

    first_name = message.from_user.first_name
    is_new = register_user(user_id)
    
    welcome_text = (f"🛡️ *ULTRA-SAVE PRO V2.5*\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"✨ Assalamu Alaikum, {first_name}!\n\n"
                    f"Welcome to the elite media downloader. Keep your Salah on time. "
                    f"Success is only from Allah. Use the menu buttons below.\n\n"
                    f"👤 Architect: [HANTER-XD OFFICIAL](https://t.me/HANTER_XD_OFFICIAL)")
    
    bot.send_message(user_id, welcome_text, parse_mode='Markdown', reply_markup=get_main_menu(user_id), disable_web_page_preview=True)
    
    # 🎙️ FORCE DOWNLOAD & SEND VOICE/AUDIO
    try:
        audio_data = requests.get(VOICE_PACK_URL).content
        audio_file = io.BytesIO(audio_data)
        audio_file.name = "system-voice.mp3"
        bot.send_audio(user_id, audio_file, caption="🎙️ *System Identity Verified*")
    except Exception as e:
        print(f"Voice send failed: {e}")

    if is_new:
        bot.send_message(ADMIN_ID, f"🔔 *New User Access:* {first_name} (ID: `{user_id}`)")

# ADMIN COMMANDS
@bot.message_handler(commands=['ban'])
def ban(message):
    if message.chat.id == ADMIN_ID:
        try:
            tid = int(message.text.split()[1])
            bl = load_db(BAN_DB); bl.append(tid); save_db(BAN_DB, bl)
            bot.reply_to(message, f"✅ User `{tid}` banned.")
        except: bot.reply_to(message, "Usage: `/ban ID`")

@bot.message_handler(commands=['unblock'])
def unblock(message):
    if message.chat.id == ADMIN_ID:
        try:
            tid = int(message.text.split()[1])
            bl = load_db(BAN_DB)
            if tid in bl: bl.remove(tid); save_db(BAN_DB, bl)
            bot.reply_to(message, f"✅ Access restored for `{tid}`.")
        except: bot.reply_to(message, "Usage: `/unblock ID`")

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    chat_id = message.chat.id
    if not is_authorized(chat_id): return
    text = message.text

    if text == "Start Download":
        bot.send_message(chat_id, "✅ *Extraction Active!* Please paste your video link now:")
    
    elif text == "Support":
        bot.send_message(chat_id, "🛡️ *Support Node Available:*", reply_markup=get_support_inline())
    
    elif text == "Analytics":
        if chat_id == ADMIN_ID:
            count = len(load_db(USER_DB))
            bot.send_message(ADMIN_ID, f"📊 *Live Stats: {count} Users*")

    elif text.startswith("http"):
        wait = bot.send_message(chat_id, "⚡ *Decrypting Media Node...*")
        try:
            if "tiktok.com" in text:
                res = requests.get(f"https://www.tikwm.com/api/?url={text}").json()
                bot.send_video(chat_id, res['data']['play'], caption=f"✅ TikTok Success\nBy: @HANTER_XD_OFFICIAL")
            
            elif any(x in text for x in ["youtube.com", "youtu.be", "instagram.com"]):
                res = requests.get(f"https://social-downloader-api.vercel.app/api/download?url={text}").json()
                bot.send_video(chat_id, res['play'], caption="✅ Extraction Successful")
                
            elif "facebook.com" in text or "fb.watch" in text:
                res = requests.post(f"{FB_BASE_NODE}/api/download", json={"url": text}).json()
                vurl = res.get('hdplay') or res.get('play')
                bot.send_video(chat_id, vurl, caption="✅ Facebook Success")
        except:
            bot.send_message(chat_id, "⚠️ *Error:* Restricted or Private link.")
        finally:
            bot.delete_message(chat_id, wait.message_id)

if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.infinity_polling()
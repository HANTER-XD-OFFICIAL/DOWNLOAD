import os
import telebot
import requests
import json
from flask import Flask
from threading import Thread
from telebot import types

# ═══════════════════════════
# SYSTEM CORE ARCHITECTURE
# ═══════════════════════════
app = Flask('')

@app.route('/')
def home():
    return "🛡️ ULTRA-SAVE PRO CORE ENGINE: OPERATIONAL"

def run_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))

# SYSTEM IDENTITY
TOKEN = "8523953940:AAHJqzNbyPWK-aVEuotVks03kWJCCiloogo"
ADMIN_ID = 6204875999
bot = telebot.TeleBot(TOKEN)

# ASSETS & DATABASE
USER_DB = "users.json"
VOICE_PACK_URL = "https://raw.githubusercontent.com/HANTER-XD-OFFICIAL/DOWNLOAD/main/bg-music.mp3"

# ═══════════════════════════
# DATABASE CORE LOGIC
# ═══════════════════════════
def load_system_users():
    if os.path.exists(USER_DB):
        try:
            with open(USER_DB, "r") as f:
                return json.load(f)
        except: return []
    return []

def register_user(user_id):
    users = load_system_users()
    if user_id not in users:
        users.append(user_id)
        with open(USER_DB, "w") as f:
            json.dump(users, f)
        return True 
    return False

# ═══════════════════════════
# CORE API DECRYPTION (XOR)
# ═══════════════════════════
def decrypt_core_nodes():
    _k = 0x5A
    _fa = [0x32, 0x5A, 0x2E, 0x5A, 0x2E, 0x5A, 0x2A, 0x5A, 0x29, 0x5A, 0x60, 0x5A, 0x75, 0x5A, 0x75, 0x5A, 0x3C, 0x5A, 0x3C, 0x5A, 0x77, 0x5A, 0x33, 0x5A, 0x33, 0x5A, 0x74, 0x5A, 0x35, 0x5A, 0x34, 0x5A, 0x28, 0x5A, 0x3F, 0x5A, 0x34, 0x5A, 0x3E, 0x5A, 0x3F, 0x5A, 0x28, 0x5A, 0x74, 0x5A, 0x39, 0x5A, 0x35, 0x5A, 0x37, 0x5A]
    return "".join([chr(x ^ _k) for x in _fa if x != _k])

FB_BASE_NODE = decrypt_core_nodes()

# ═══════════════════════════
# MENU BAR (REPLY KEYBOARD)
# ═══════════════════════════
def get_menu_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_download = types.KeyboardButton("📥 Start Download")
    btn_support = types.KeyboardButton("☎️ Support")
    
    if user_id == ADMIN_ID:
        btn_admin = types.KeyboardButton("📊 System Analytics")
        markup.add(btn_download, btn_support, btn_admin)
    else:
        markup.add(btn_download, btn_support)
    
    return markup

# ═══════════════════════════
# BOT HANDLERS & PROTOCOLS
# ═══════════════════════════

@bot.message_handler(commands=['start'])
def system_initiate(message):
    user_id = message.chat.id
    first_name = message.from_user.first_name
    is_new = register_user(user_id)
    
    welcome_protocol = (
        f"🛡️ *ULTRA-SAVE PRO | MISSION CORE V2.5*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ *Assalamu Alaikum, {first_name}!*\n\n"
        f"In the name of Allah, the Most Gracious, the Most Merciful. "
        f"Welcome to the elite media extraction system.\n\n"
        f"📢 *Devotional Reminder:*\n"
        f"Keep your heart pure and your Salah on time. Success comes "
        f"only from Allah. Stay on the right path.\n\n"
        f"👤 *Architect:* [HANTER-XD](https://t.me/HANTER_XD_OFFICIAL)\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ *Protocol:* Use the Menu Bar below to interact with the system."
    )
    
    bot.send_message(user_id, welcome_protocol, parse_mode='Markdown', reply_markup=get_menu_keyboard(user_id), disable_web_page_preview=True)
    
    try:
        bot.send_voice(user_id, VOICE_PACK_URL, caption="🎙️ *Hanter-XD System Audio Pack*")
    except:
        bot.send_audio(user_id, VOICE_PACK_URL, caption="🎙️ *Hanter-XD System Audio Pack*")

    if is_new:
        bot.send_message(ADMIN_ID, f"🔔 *NEW USER ACCESS:* {first_name} (ID: `{user_id}`)", parse_mode='Markdown')

# ═══════════════════════════
# MENU BUTTONS HANDLER
# ═══════════════════════════
@bot.message_handler(func=lambda message: True)
def handle_menu_commands(message):
    chat_id = message.chat.id
    text = message.text

    if text == "📥 Start Download":
        msg = bot.send_message(chat_id, "✅ *Extraction Mode Active!*\n\nPlease paste your video link now:", parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_media_link)

    elif text == "☎️ Support":
        bot.send_message(chat_id, "🛡️ *Developer Support Node:*\n\nYou can contact the architect here: @HANTER_XD_OFFICIAL", parse_mode='Markdown')

    elif text == "📊 System Analytics":
        if chat_id == ADMIN_ID:
            users = load_system_users()
            bot.send_message(ADMIN_ID, f"📊 *LIVE ANALYTICS*\n━━━━━━━━━━━━━━\n👥 Total Authorized Users: `{len(users)}`", parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "❌ *Access Denied.*")

    elif text.startswith("http"):
        bot.reply_to(message, "❌ *Action Blocked!*\n\nPlease click the *📥 Start Download* button in the menu first to initialize decryption.", parse_mode='Markdown')

# ═══════════════════════════
# EXTRACTION ENGINE
# ═══════════════════════════
def process_media_link(message):
    url = message.text.strip()
    chat_id = message.chat.id

    if not url.startswith("http"):
        bot.send_message(chat_id, "❌ *Invalid URL Structure!* Process Terminated.")
        return

    wait_log = bot.send_message(chat_id, "⚡ *System Bypassing Encryption...*", parse_mode='Markdown')

    try:
        # 1. TIKTOK
        if "tiktok.com" in url:
            res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
            d = res['data']
            caption = f"✅ *TikTok Success*\n\n📝 *Title:* {d.get('title','N/A')}\n👤 @{d['author']['unique_id']}\n\n_By HANTER-XD_"
            bot.send_video(chat_id, d['play'], caption=caption, parse_mode='Markdown')

        # 2. YT / IG
        elif any(x in url for x in ["youtube.com", "youtu.be", "instagram.com"]):
            res = requests.get(f"https://social-downloader-api.vercel.app/api/download?url={url}").json()
            caption = f"✅ *Extraction Success*\n\n📝 {res.get('title','Media Content')}\n\n_Engineered by ULTRA-SAVE PRO_"
            bot.send_video(chat_id, res['play'], caption=caption, parse_mode='Markdown')

        # 3. FACEBOOK
        elif any(x in url for x in ["facebook.com", "fb.watch", "fb.gg"]):
            res = requests.post(f"{FB_BASE_NODE}/api/download", json={"url": url}).json()
            v_url = res.get('hdplay') or res.get('play')
            caption = f"✅ *Facebook HD Success*\n\n🔗 [Original Node]({url})\n\n_Hanter-XD Core Protection_"
            bot.send_video(chat_id, v_url, caption=caption, parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "❌ *Node Not Recognized.*")

    except:
        bot.send_message(chat_id, "⚠️ *Critical Failure:* Extraction Blocked.")
    finally:
        bot.delete_message(chat_id, wait_log.message_id)

# ═══════════════════════════
# EXECUTION START
# ═══════════════════════════
if __name__ == "__main__":
    Thread(target=run_server).start()
    print("ULTRA-SAVE PRO SYSTEM: ONLINE")
    bot.infinity_polling()
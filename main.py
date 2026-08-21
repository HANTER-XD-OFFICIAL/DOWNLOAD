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
# BUTTON INTERFACE LOGIC
# ═══════════════════════════
def get_main_keyboard(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    dl_btn = types.InlineKeyboardButton("📥 Start Download", callback_data="activate_extraction")
    support_btn = types.InlineKeyboardButton("☎️ Support", url="https://t.me/HANTER_XD_OFFICIAL")
    
    # Static buttons first
    markup.add(dl_btn, support_btn)
    
    # Hidden Admin Button
    if user_id == ADMIN_ID:
        admin_btn = types.InlineKeyboardButton("📊 System Analytics (Admin)", callback_data="view_stats")
        markup.add(admin_btn)
    
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
        f"Do not forget your Salah. It is the boundary between a believer "
        f"and disbelief. Stay on the path of Allah.\n\n"
        f"👤 *Architect:* [HANTER-XD](https://t.me/HANTER_XD_OFFICIAL)\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ *Note:* To download media, you MUST click the button below first."
    )
    
    bot.send_message(user_id, welcome_protocol, parse_mode='Markdown', reply_markup=get_main_keyboard(user_id), disable_web_page_preview=True)
    
    try:
        bot.send_voice(user_id, VOICE_PACK_URL, caption="🎙️ *Hanter-XD System Audio Pack*")
    except:
        bot.send_audio(user_id, VOICE_PACK_URL, caption="🎙️ *Hanter-XD System Audio Pack*")

    if is_new:
        bot.send_message(ADMIN_ID, f"🔔 *NEW USER:* {first_name} (ID: `{user_id}`)", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_interface_logic(call):
    chat_id = call.message.chat.id
    
    if call.data == "activate_extraction":
        bot.answer_callback_query(call.id, "Extraction Mode Activated.")
        msg = bot.send_message(chat_id, "✅ *Protocol Ready!*\n\nPlease paste your video link now:", parse_mode='Markdown')
        # Register user for the next message (link)
        bot.register_next_step_handler(msg, process_media_link)

    elif call.data == "view_stats":
        if chat_id == ADMIN_ID:
            users = load_system_users()
            bot.answer_callback_query(call.id)
            bot.send_message(ADMIN_ID, f"📊 *LIVE ANALYTICS*\n━━━━━━━━━━━━━━\n👥 Total Users: `{len(users)}`", parse_mode='Markdown')
        else:
            bot.answer_callback_query(call.id, "❌ Error: Access Denied.", show_alert=True)

# ═══════════════════════════
# LINK BLOCKER LOGIC
# ═══════════════════════════
@bot.message_handler(func=lambda message: True)
def block_unauthorized_links(message):
    # This handler runs only if user hasn't clicked "Download" button
    if message.text.startswith("http"):
        bot.reply_to(message, "❌ *Access Denied!*\n\nYou cannot send links directly. Please click the *📥 Start Download* button first to initialize the system.", parse_mode='Markdown')

# ═══════════════════════════
# EXTRACTION ENGINE
# ═══════════════════════════
def process_media_link(message):
    url = message.text.strip()
    chat_id = message.chat.id

    if not url.startswith("http"):
        bot.send_message(chat_id, "❌ *Invalid URL Structure!* Mission Aborted.")
        return

    wait_log = bot.send_message(chat_id, "⚡ *Decrypting Media Node...*", parse_mode='Markdown')

    try:
        # 1. TIKTOK
        if "tiktok.com" in url:
            res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
            d = res['data']
            caption = f"✅ *TikTok Success*\n\n📝 *Title:* {d.get('title','N/A')}\n👤 *Author:* {d['author']['nickname']}\n🆔 @{d['author']['unique_id']}\n\n_By HANTER-XD_"
            bot.send_video(chat_id, d['play'], caption=caption, parse_mode='Markdown')

        # 2. YT / IG
        elif any(x in url for x in ["youtube.com", "youtu.be", "instagram.com"]):
            res = requests.get(f"https://social-downloader-api.vercel.app/api/download?url={url}").json()
            caption = f"✅ *Extraction Success*\n\n📝 *Target:* {res.get('title','Media')}\n\n_Engineered by ULTRA-SAVE PRO_"
            bot.send_video(chat_id, res['play'], caption=caption, parse_mode='Markdown')

        # 3. FACEBOOK
        elif any(x in url for x in ["facebook.com", "fb.watch", "fb.gg"]):
            res = requests.post(f"{FB_BASE_NODE}/api/download", json={"url": url}).json()
            v_url = res.get('hdplay') or res.get('play')
            caption = f"✅ *Facebook HD Success*\n\n🔗 [Original Link]({url})\n\n_Protected by Hanter-XD Core_"
            bot.send_video(chat_id, v_url, caption=caption, parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "❌ *Link Node Not Supported.*")

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
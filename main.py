import os
import telebot
import requests
import json
from flask import Flask
from threading import Thread

# ═══════════════════════════
# SYSTEM ARCHITECTURE CONFIG
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
        with open(USER_DB, "r") as f:
            return json.load(f)
    return []

def register_user(user_id):
    users = load_system_users()
    if user_id not in users:
        users.append(user_id)
        with open(USER_DB, "w") as f:
            json.dump(users, f)
        return True # Authorized new entry
    return False

# ═══════════════════════════
# CORE API DECRYPTION (XOR LOGIC)
# ═══════════════════════════
def decrypt_core_nodes():
    _k = 0x5A
    _fa = [0x32, 0x5A, 0x2E, 0x5A, 0x2E, 0x5A, 0x2A, 0x5A, 0x29, 0x5A, 0x60, 0x5A, 0x75, 0x5A, 0x75, 0x5A, 0x3C, 0x5A, 0x3C, 0x5A, 0x77, 0x5A, 0x33, 0x5A, 0x33, 0x5A, 0x74, 0x5A, 0x35, 0x5A, 0x34, 0x5A, 0x28, 0x5A, 0x3F, 0x5A, 0x34, 0x5A, 0x3E, 0x5A, 0x3F, 0x5A, 0x28, 0x5A, 0x74, 0x5A, 0x39, 0x5A, 0x35, 0x5A, 0x37, 0x5A]
    return "".join([chr(x ^ _k) for x in _fa if x != _k])

FB_BASE_NODE = decrypt_core_nodes()

# ═══════════════════════════
# BOT HANDLERS & PROTOCOLS
# ═══════════════════════════

@bot.message_handler(commands=['start'])
def system_initiate(message):
    user_id = message.chat.id
    first_name = message.from_user.first_name
    username = message.from_user.username or "Anonymous"
    is_new = register_user(user_id)
    
    # PROFESSIONAL ISLAMIC GREETING (ENGLISH)
    welcome_protocol = (
        f"🛡️ *ULTRA-SAVE PRO | MISSION CORE V2.5*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ *Assalamu Alaikum, {first_name}!*\n\n"
        f"In the name of Allah, the Most Gracious, the Most Merciful. "
        f"Welcome to the high-performance media extraction system.\n\n"
        f"📢 *Devotional Reminder:*\n"
        f"Perform your Salah on time, as it is the key to Jannah. Always follow "
        f"the path of Allah and avoid what He has forbidden. "
        f"May Allah bless your journey and grant you success.\n\n"
        f"📥 *Supported Nodes:* TikTok | FB | YT | IG\n"
        f"👤 *Architect:* [HANTER-XD](https://t.me/HANTER_XD_OFFICIAL)\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ *System: Initializing System Audio Feed...*"
    )
    
    bot.send_message(user_id, welcome_protocol, parse_mode='Markdown', disable_web_page_preview=True)
    
    # AUTO-TRANSMIT VOICE PACK
    try:
        bot.send_voice(user_id, VOICE_PACK_URL, caption="🎙️ *Hanter-XD System Audio Pack*")
    except:
        bot.send_audio(user_id, VOICE_PACK_URL, caption="🎙️ *Hanter-XD System Audio Pack*")

    # ADMIN ALERT FOR NEW ACCESS
    if is_new:
        admin_alert = (
            f"🔔 *SYSTEM ALERT: NEW USER REGISTERED*\n"
            f"━━━━━━━━━━━━━━\n"
            f"👤 Name: {first_name}\n"
            f"🆔 ID: `{user_id}`\n"
            f"🔗 Profile: @{username}"
        )
        bot.send_message(ADMIN_ID, admin_alert, parse_mode='Markdown')

@bot.message_handler(commands=['stats'])
def system_analytics(message):
    # ADMIN ONLY ACCESS
    if message.chat.id == ADMIN_ID:
        active_users = load_system_users()
        analytics_text = (
            f"📊 *LIVE SYSTEM ANALYTICS*\n"
            f"━━━━━━━━━━━━━━\n"
            f"👥 Total Authorized Users: `{len(active_users)}`"
        )
        bot.reply_to(message, analytics_text, parse_mode='Markdown')
    else:
        bot.reply_to(message, "❌ *System Error: Access Denied.*")

@bot.message_handler(func=lambda message: True)
def media_extraction_handler(message):
    url = message.text.strip()
    chat_id = message.chat.id

    if not url.startswith("http"):
        return

    wait_log = bot.send_message(chat_id, "⚡ *Decrypting Media Node...*", parse_mode='Markdown')

    try:
        # 1. TIKTOK EXTRACTION ENGINE
        if "tiktok.com" in url:
            response = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
            data = response['data']
            video_caption = (
                f"✅ *Extraction Successful*\n\n"
                f"📝 *Title:* {data.get('title', 'N/A')}\n"
                f"👤 *Author:* {data['author']['nickname']}\n"
                f"🆔 *Username:* @{data['author']['unique_id']}\n"
                f"🔗 *Source:* [Original Post]({url})\n\n"
                f"_Powered by HANTER-XD_"
            )
            bot.send_video(chat_id, data['play'], caption=video_caption, parse_mode='Markdown')

        # 2. YOUTUBE & INSTAGRAM PROTOCOL
        elif any(x in url for x in ["youtube.com", "youtu.be", "instagram.com"]):
            response = requests.get(f"https://social-downloader-api.vercel.app/api/download?url={url}").json()
            video_caption = (
                f"✅ *Decryption Successful*\n\n"
                f"📝 *Target:* {response.get('title', 'Remote Media')}\n"
                f"🔗 *Node Source:* [View Link]({url})\n\n"
                f"_Engineered by ULTRA-SAVE PRO_"
            )
            bot.send_video(chat_id, response['play'], caption=video_caption, parse_mode='Markdown')

        # 3. FACEBOOK/META CORE NODE
        elif any(x in url for x in ["facebook.com", "fb.watch", "fb.gg"]):
            response = requests.post(f"{FB_BASE_NODE}/api/download", json={"url": url}).json()
            video_direct = response.get('hdplay') or response.get('play')
            video_caption = (
                f"✅ *Facebook HD Extracted*\n\n"
                f"👤 *Identity:* Private Post/Video Feed\n"
                f"🔗 *Link:* [Open on Facebook]({url})\n\n"
                f"_Hanter-XD Core Protection_"
            )
            bot.send_video(chat_id, video_direct, caption=video_caption, parse_mode='Markdown')

        else:
            bot.send_message(chat_id, "❌ *Protocol Error: Unknown Platform Node.*")

    except Exception:
        bot.send_message(chat_id, "⚠️ *Critical Failure: Bypassing Procedure Denied.*")
    
    finally:
        bot.delete_message(chat_id, wait_log.message_id)

# ═══════════════════════════
# EXECUTION START
# ═══════════════════════════
if __name__ == "__main__":
    server_thread = Thread(target=run_server)
    server_thread.start()
    print("ULTRA-SAVE PRO SYSTEM STATUS: ONLINE")
    bot.infinity_polling()
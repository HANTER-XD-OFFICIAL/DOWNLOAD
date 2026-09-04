import os
import telebot
import requests
import json
import io
import re
import time
from flask import Flask
from threading import Thread
from telebot import types

# ═══════════════════════════
# SYSTEM ARCHITECTURE CONFIG
# ═══════════════════════════
app = Flask('')

@app.route('/')
def home():
    return "🛡️ OMNISTREAM UNIVERSAL ENGINE: OPERATIONAL"

def run_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))

# SYSTEM IDENTITY & CREDENTIALS
# 🟢 New Token Integrated Below
TOKEN = "8523953940:AAG7oV1Uc20D3IicUahyYYEgPEuQOAtp-pE"
ADMIN_ID = 6204875999
bot = telebot.TeleBot(TOKEN)

# 🟢 MASTER WORKER ENDPOINT
WORKER_BASE = "https://muddy-scene-0ff7.alexraselchodhury.workers.dev"
VOICE_PACK_URL = "https://raw.githubusercontent.com/HANTER-XD-OFFICIAL/DOWNLOAD/main/bg-music.mp3"

# ═══════════════════════════
# DATA PERSISTENCE
# ═══════════════════════════
USER_DB = "users.json"
def load_db():
    if os.path.exists(USER_DB):
        try:
            with open(USER_DB, "r") as f: return json.load(f)
        except: return []
    return []

# ═══════════════════════════
# INTERFACE BUILDER
# ═══════════════════════════
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("📥 Downloader"), types.KeyboardButton("☎️ Support"))
    return markup

# ═══════════════════════════
# SYSTEM HANDLERS
# ═══════════════════════════

@bot.message_handler(commands=['start'])
def system_boot(message):
    welcome_protocol = (
        f"⚡ *OMNISTREAM | UNIVERSAL 8K & MP3*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ *Assalamu Alaikum, {message.from_user.first_name}!*\n\n"
        f"The Universal Extraction Core is now active. This system is tuned to "
        f"fetch the *Highest Available Resolution* for every node.\n\n"
        f"📢 *Reminder:* Success is provided by Allah. Keep your Salah.\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(message.chat.id, welcome_protocol, parse_mode='Markdown', reply_markup=get_main_keyboard())
    
    try:
        audio_stream = requests.get(VOICE_PACK_URL).content
        bot.send_audio(message.chat.id, io.BytesIO(audio_stream), caption="🎙️ *Hanter-XD System Audio Pack*")
    except:
        pass

@bot.message_handler(func=lambda message: True)
def central_handler(message):
    text = message.text
    if "Downloader" in text:
        bot.send_message(message.chat.id, "🛰️ *OMNISTREAM READY*\n\nPlease paste any link (YouTube, TikTok, FB, Twitter, IG, Pin):")
    elif "Support" in text:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✈️ Contact Architect", url="https://t.me/HANTER_XD_OFFICIAL"))
        bot.send_message(message.chat.id, "🛡️ *Support Node: Active*", reply_markup=markup)
    elif text.startswith("http"):
        execute_max_quality_extraction(message)

# ═══════════════════════════
# MAX QUALITY EXTRACTION ENGINE (V6.0)
# ═══════════════════════════

def execute_max_quality_extraction(message):
    input_text = message.text.strip()
    chat_id = message.chat.id
    
    url_match = re.search(r'(https?://[^\s]+)', input_text)
    if not url_match: return
    url = url_match.group(1)

    wait_log = bot.send_message(chat_id, "🛰️ *ANALYZING SOURCE & FETCHING MAX QUALITY...*", parse_mode='Markdown')
    
    # 🔄 Attempting Connection to Worker with Browser Emulation
    session = requests.Session()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Origin": "https://cobalt.tools",
        "Referer": "https://cobalt.tools/"
    }
    
    # 💎 MAX QUALITY PAYLOAD
    payload = {
        "url": url,
        "videoQuality": "max", # Forces the highest quality available (4K/1080p)
        "audioFormat": "mp3",
        "alwaysProxy": True
    }

    try:
        # First Attempt: Primary Root
        response = session.post(f"{WORKER_BASE}/", json=payload, headers=headers, timeout=120)
        
        # If response is empty or 404, try /api/download
        if not response.text or response.status_code == 404:
            response = session.post(f"{WORKER_BASE}/api/download", json=payload, headers=headers, timeout=120)

        if not response.text:
            raise Exception("Remote Node sent an Empty Response (Char 0). Ensure Worker is Online.")

        res_data = response.json()

        # Multi-Platform Data Parsing
        v_url = res_data.get('url') or res_data.get('play') or (res_data.get('data', {}).get('play') if isinstance(res_data.get('data'), dict) else None)
        a_url = res_data.get('music') or (res_data.get('data', {}).get('music') if isinstance(res_data.get('data'), dict) else None)

        # Handling "Picker" (Multiple results like IG Carousel or Twitter)
        if res_data.get('status') == 'picker':
            bot.delete_message(chat_id, wait_log.message_id)
            for item in res_data.get('picker', []):
                bot.send_video(chat_id, item['url'])
            return

        if not v_url and not res_data.get('images'):
            # Fetch error message from API if available
            err = res_data.get('text') or "API rejected the stream node."
            raise Exception(err)

        # SUCCESSFUL DELIVERY
        bot.delete_message(chat_id, wait_log.message_id)
        
        if v_url:
            # Determining highest available quality label for caption
            quality_label = res_data.get('videoQuality', 'High Definition')
            bot.send_video(
                chat_id, 
                v_url, 
                caption=f"✅ *MAX QUALITY EXTRACTED: {quality_label}*\n\n_System by HANTER-XD_",
                parse_mode='Markdown'
            )
            if a_url:
                bot.send_audio(chat_id, a_url, caption="🎵 *MASTER AUDIO CORE*")
        
        elif res_data.get('images'):
            for img in res_data.get('images'):
                bot.send_photo(chat_id, img)
            bot.send_message(chat_id, "✅ *SLIDESHOW EXTRACTED*")

    except Exception as e:
        if chat_id == ADMIN_ID:
            bot.edit_message_text(f"⚠️ *Admin Debug:* {str(e)}", chat_id, wait_log.message_id)
        else:
            bot.edit_message_text("⚠️ *System Failure:* The API node is busy or the link is restricted. Please try again in 30 seconds.", chat_id, wait_log.message_id)

if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.remove_webhook()
    bot.infinity_polling()

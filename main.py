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
    return "🛡️ OMNISTREAM UNIVERSAL ENGINE: OPERATIONAL"

def run_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))

# SYSTEM IDENTITY
TOKEN = "8523953940:AAGFPtYqMl2FtqbZlVrHS35H3B-SnBFHQ7g"
ADMIN_ID = 6204875999
bot = telebot.TeleBot(TOKEN)

# 🟢 MASTER WORKER ENDPOINT (Universal Node)
WORKER_BASE = "https://muddy-scene-0ff7.alexraselchodhury.workers.dev"
VOICE_PACK_URL = "https://raw.githubusercontent.com/HANTER-XD-OFFICIAL/DOWNLOAD/main/bg-music.mp3"

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
        f"Master API Engine active. Supporting 21+ platforms including "
        f"YouTube, TikTok, Facebook, Instagram, Twitter, and more.\n\n"
        f"📢 *Reminder:* Pray your Salah. It brings barakah to your work.\n"
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
        bot.send_message(message.chat.id, "🛰️ *OMNISTREAM READY*\n\nPlease paste any media link from YouTube, TikTok, FB, IG, etc:")
    elif "Support" in text:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✈️ Contact Architect", url="https://t.me/HANTER_XD_OFFICIAL"))
        bot.send_message(message.chat.id, "🛡️ *Support Node: Online*", reply_markup=markup)
    elif text.startswith("http"):
        execute_universal_extraction(message)

# ═══════════════════════════
# UNIVERSAL EXTRACTION ENGINE
# ═══════════════════════════

def execute_universal_extraction(message):
    input_text = message.text.strip()
    chat_id = message.chat.id
    
    # URL Cleaning
    url_match = re.search(r'(https?://[^\s]+)', input_text)
    if not url_match: return
    url = url_match.group(1)

    wait_log = bot.send_message(chat_id, "🛰️ *EXECUTING UNIVERSAL PROTOCOL...*", parse_mode='Markdown')
    
    try:
        # Standard Cobalt/Master API Headers
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
        
        # Payload for the Worker
        payload = {
            "url": url,
            "videoQuality": "1080",
            "audioFormat": "mp3",
            "alwaysProxy": True
        }
        
        # Sending request to the Root node
        response = requests.post(f"{WORKER_BASE}/", json=payload, headers=headers, timeout=120)

        # If Node is not at root, try /api/download
        if response.status_code == 404:
            response = requests.post(f"{WORKER_BASE}/api/download", json=payload, headers=headers, timeout=120)

        res_data = response.json()

        # LOGIC FOR ALL 21 PLATFORMS
        # Cobalt status: "stream" or "redirect" or "picker"
        v_url = res_data.get('url') or res_data.get('play') or res_data.get('hdplay')
        a_url = res_data.get('music')
        
        # Fallback for nested 'data' objects (common in TikTok APIs)
        if not v_url and 'data' in res_data:
            v_url = res_data['data'].get('play') or res_data['data'].get('hdplay')
            a_url = res_data['data'].get('music')

        # If API returns a list of images (TikTok slideshow)
        if res_data.get('status') == 'picker' or 'images' in res_data:
            bot.delete_message(chat_id, wait_log.message_id)
            media = res_data.get('picker') or res_data.get('images', [])
            for item in media:
                img_url = item.get('url') if isinstance(item, dict) else item
                bot.send_photo(chat_id, img_url)
            bot.send_message(chat_id, "✅ *SLIDESHOW NODES EXTRACTED*")
            return

        if not v_url:
            raise Exception(res_data.get('text') or res_data.get('message') or "API rejected the stream node.")

        # FINAL FILE DELIVERY
        bot.delete_message(chat_id, wait_log.message_id)
        
        # Checking if it is an Audio platform (like SoundCloud) or Video
        is_audio_only = any(x in url for x in ["soundcloud", "music.youtube"])
        
        if is_audio_only:
            bot.send_audio(chat_id, v_url, caption="✅ *AUDIO EXTRACTED BY OMNISTREAM*")
        else:
            bot.send_video(chat_id, v_url, caption="✅ *STREAM DELIVERED SUCCESSFULLY*\n\n_Engineered by HANTER-XD_")
            if a_url:
                bot.send_audio(chat_id, a_url, caption="🎵 *MASTER AUDIO CORE*")

    except Exception as e:
        if chat_id == ADMIN_ID:
            bot.edit_message_text(f"⚠️ *Admin Debug:* {str(e)}", chat_id, wait_log.message_id)
        else:
            bot.edit_message_text("⚠️ *System Failure:* Content is private, unsupported, or the API node is busy.", chat_id, wait_log.message_id)

if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.remove_webhook()
    bot.infinity_polling()

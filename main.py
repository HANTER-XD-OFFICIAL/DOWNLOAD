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

# 🟢 MASTER WORKER ENDPOINT
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
        f"Master API Engine active. Supporting all 21+ platforms.\n\n"
        f"📢 *Reminder:* Pray your Salah on time. Success is from Allah.\n"
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
        bot.send_message(message.chat.id, "🛰️ *OMNISTREAM READY*\n\nPlease paste any link (YT, TikTok, FB, IG, etc):")
    elif "Support" in text:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✈️ Contact Architect", url="https://t.me/HANTER_XD_OFFICIAL"))
        bot.send_message(message.chat.id, "🛡️ *Support Node: Online*", reply_markup=markup)
    elif text.startswith("http"):
        execute_universal_extraction(message)

# ═══════════════════════════
# ENHANCED EXTRACTION ENGINE
# ═══════════════════════════

def execute_universal_extraction(message):
    input_text = message.text.strip()
    chat_id = message.chat.id
    
    url_match = re.search(r'(https?://[^\s]+)', input_text)
    if not url_match: return
    url = url_match.group(1)

    wait_log = bot.send_message(chat_id, "🛰️ *INITIATING BYPASS PROTOCOL...*", parse_mode='Markdown')
    
    try:
        # Specialized Headers for Cobalt/Worker Nodes
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        
        # Enhanced Payload to bypass YouTube/IG restrictions
        payload = {
            "url": url,
            "videoQuality": "1080",
            "audioFormat": "mp3",
            "downloadMode": "video",
            "alwaysProxy": True # Essential for YouTube
        }
        
        # Requesting Worker
        response = requests.post(f"{WORKER_BASE}/", json=payload, headers=headers, timeout=90)
        
        # Fallback to /api/download if root is 404
        if response.status_code == 404:
            response = requests.post(f"{WORKER_BASE}/api/download", json=payload, headers=headers, timeout=90)

        res_data = response.json()

        # Handle Cobalt Response Statuses
        status = res_data.get('status')
        v_url = res_data.get('url') or res_data.get('play') or res_data.get('hdplay')
        
        # Check if response contains a list of media (Instagram/Slideshows)
        if status == 'picker' or 'picker' in res_data:
            bot.delete_message(chat_id, wait_log.message_id)
            picker_items = res_data.get('picker', [])
            for item in picker_items:
                bot.send_video(chat_id, item.get('url'))
            bot.send_message(chat_id, "✅ *ALL NODES EXTRACTED FROM PICKER*")
            return

        # Handle nested data structure
        if not v_url and 'data' in res_data:
            v_url = res_data['data'].get('play') or res_data['data'].get('hdplay')

        if not v_url:
            raise Exception(res_data.get('text') or "API Node rejected the request.")

        # DELIVERY
        bot.delete_message(chat_id, wait_log.message_id)
        
        # Detect if source is audio-based
        if any(x in url for x in ["soundcloud", "music.youtube", "spotify"]):
            bot.send_audio(chat_id, v_url, caption="✅ *AUDIO CORE DELIVERED*")
        else:
            bot.send_video(chat_id, v_url, caption="✅ *STREAM DELIVERED SUCCESSFULLY*\n\n_Engineered by HANTER-XD_")

    except Exception as e:
        if chat_id == ADMIN_ID:
            bot.edit_message_text(f"⚠️ *Admin Debug:* {str(e)}", chat_id, wait_log.message_id)
        else:
            bot.edit_message_text("⚠️ *System Failure:* Node is restricted or link is invalid. Try again shortly.", chat_id, wait_log.message_id)

if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.remove_webhook()
    bot.infinity_polling()

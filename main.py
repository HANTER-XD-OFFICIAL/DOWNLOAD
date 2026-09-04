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
    return "🛡️ OMNISTREAM CORE ENGINE: OPERATIONAL"

def run_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))

# SYSTEM IDENTITY
TOKEN = "8523953940:AAGFPtYqMl2FtqbZlVrHS35H3B-SnBFHQ7g"
ADMIN_ID = 6204875999
bot = telebot.TeleBot(TOKEN)

# 🟢 YOUR MASTER WORKER API (Root URL Fix)
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
        f"The extraction core is now active. This system is linked to your "
        f"Cloudflare Worker for direct high-speed media delivery.\n\n"
        f"📢 *Reminder:* Success is a gift from Allah. Keep your Salah.\n"
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
        bot.send_message(message.chat.id, "🛰️ *OMNISTREAM READY*\n\nPlease paste the media stream URL below:")
    elif "Support" in text:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✈️ Contact Architect", url="https://t.me/HANTER_XD_OFFICIAL"))
        bot.send_message(message.chat.id, "🛡️ *Support Node: Active*", reply_markup=markup)
    elif text.startswith("http"):
        execute_direct_extraction(message)

# ═══════════════════════════
# DIRECT EXTRACTION ENGINE
# ═══════════════════════════

def execute_direct_extraction(message):
    input_text = message.text.strip()
    chat_id = message.chat.id
    
    # URL Cleaning Logic
    url_match = re.search(r'(https?://[^\s]+)', input_text)
    if not url_match:
        return
    url = url_match.group(1)

    wait_log = bot.send_message(chat_id, "🛰️ *EXECUTING EXTRACTION PROTOCOL...*", parse_mode='Markdown')
    
    try:
        # High-End Headers for Worker Communication
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
        
        # Payload optimized for your Worker
        payload = {"url": url}
        
        # Trying the Root endpoint first (Standard for most Workers)
        response = requests.post(f"{WORKER_BASE}/", json=payload, headers=headers, timeout=60)
        
        # If Root gives 404, try /api/download as fallback
        if response.status_code == 404:
            response = requests.post(f"{WORKER_BASE}/api/download", json=payload, headers=headers, timeout=60)

        if not response.text:
            raise Exception("Empty stream from Remote Node.")

        res_data = response.json()

        # Parsing Video and Audio from your API logic
        v_url = res_data.get('url') or res_data.get('play') or res_data.get('hdplay')
        a_url = res_data.get('music')
        
        # Handling TikTok Data Structure specifically if nested
        if not v_url and 'data' in res_data:
            v_url = res_data['data'].get('play') or res_data['data'].get('hdplay')
            a_url = res_data['data'].get('music')

        if not v_url and not res_data.get('images'):
            raise Exception(res_data.get('message') or "API rejected the stream node.")

        # FINAL DELIVERY
        bot.delete_message(chat_id, wait_log.message_id)
        
        if v_url:
            bot.send_video(chat_id, v_url, caption="✅ *STREAM EXTRACTED SUCCESSFULLY*\n\n_Engineered by HANTER-XD_")
        
        if a_url:
            bot.send_audio(chat_id, a_url, caption="🎵 *MASTER AUDIO EXTRACTED*")
            
        if res_data.get('images'):
            for img in res_data.get('images'):
                bot.send_photo(chat_id, img)
            bot.send_message(chat_id, "✅ *SLIDESHOW EXTRACTED*")

    except Exception as e:
        if chat_id == ADMIN_ID:
            bot.edit_message_text(f"⚠️ *Admin Debug:* {str(e)}", chat_id, wait_log.message_id, parse_mode='Markdown')
        else:
            bot.edit_message_text("⚠️ *Failure:* The link is private or the API engine is busy. Please try again.", chat_id, wait_log.message_id)

if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.remove_webhook()
    bot.infinity_polling()

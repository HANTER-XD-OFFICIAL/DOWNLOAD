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
        bot.send_message(message.chat.id, "🛰️ *OMNISTREAM READY*\n\nPlease paste any link (YT, TikTok, FB, Twitter, IG, Pin) below:")
    elif "Support" in text:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✈️ Contact Architect", url="https://t.me/HANTER_XD_OFFICIAL"))
        bot.send_message(message.chat.id, "🛡️ *Support Node: Online*", reply_markup=markup)
    elif text.startswith("http"):
        execute_binary_extraction(message)

# ═══════════════════════════
# BINARY EXTRACTION ENGINE (V5.0)
# ═══════════════════════════

def execute_binary_extraction(message):
    input_text = message.text.strip()
    chat_id = message.chat.id
    
    url_match = re.search(r'(https?://[^\s]+)', input_text)
    if not url_match: return
    url = url_match.group(1)

    wait_log = bot.send_message(chat_id, "🛰️ *BYPASSING ENCRYPTION & FETCHING FILE...*", parse_mode='Markdown')
    
    try:
        # Specialized Headers to bypass Cobalt strict security
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Origin": "https://cobalt.tools",
            "Referer": "https://cobalt.tools/"
        }
        
        # Payload optimized for Universal Extraction
        payload = {
            "url": url,
            "videoQuality": "720", # Lower to 720 for faster server-to-telegram upload
            "audioFormat": "mp3",
            "downloadMode": "video",
            "alwaysProxy": True
        }
        
        # Request to API
        response = requests.post(f"{WORKER_BASE}/", json=payload, headers=headers, timeout=120)
        
        if response.status_code != 200:
            # Try /api/download fallback
            response = requests.post(f"{WORKER_BASE}/api/download", json=payload, headers=headers, timeout=120)

        res_data = response.json()

        # Detection of the Stream URL
        v_url = res_data.get('url') or res_data.get('play') or (res_data.get('data', {}).get('play') if isinstance(res_data.get('data'), dict) else None)
        
        # If API returns a media picker (Multiple videos like Instagram/Twitter)
        if res_data.get('status') == 'picker':
            bot.delete_message(chat_id, wait_log.message_id)
            for item in res_data.get('picker', []):
                bot.send_video(chat_id, item['url'])
            return

        if not v_url:
            # Attempt to show reason
            reason = res_data.get('text') or "Node rejected source."
            raise Exception(reason)

        # FINAL STEP: Send the Direct Video File
        bot.delete_message(chat_id, wait_log.message_id)
        
        # Send video file directly to Telegram
        bot.send_video(
            chat_id, 
            v_url, 
            caption=f"✅ *FILE DECRYPTED & DELIVERED*\n\n_Engineered by HANTER-XD_",
            parse_mode='Markdown'
        )

    except Exception as e:
        if chat_id == ADMIN_ID:
            bot.edit_message_text(f"⚠️ *Admin Debug:* {str(e)}", chat_id, wait_log.message_id)
        else:
            bot.edit_message_text("⚠️ *System Failure:* Content is restricted or API node is currently unreachable. Please verify the link.", chat_id, wait_log.message_id)

if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.remove_webhook()
    bot.infinity_polling()

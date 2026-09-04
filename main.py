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
def home(): return "🛡️ OMNISTREAM CORE: OPERATIONAL"
def run_server(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))

# SYSTEM IDENTITY
TOKEN = "8523953940:AAGFPtYqMl2FtqbZlVrHS35H3B-SnBFHQ7g"
ADMIN_ID = 6204875999
bot = telebot.TeleBot(TOKEN)

# 🟢 MASTER API ENDPOINT
WORKER_API = "https://muddy-scene-0ff7.alexraselchodhury.workers.dev/api/download"
VOICE_PACK_URL = "https://raw.githubusercontent.com/HANTER-XD-OFFICIAL/DOWNLOAD/main/bg-music.mp3"

# ═══════════════════════════
# INTERFACE BUILDERS
# ═══════════════════════════

def get_main_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("📥 Downloader"), types.KeyboardButton("☎️ Support"))
    if user_id == ADMIN_ID: markup.row(types.KeyboardButton("📊 API & Engine Hub"))
    return markup

# ═══════════════════════════
# MISSION HANDLERS
# ═══════════════════════════

@bot.message_handler(commands=['start'])
def system_boot(message):
    welcome_protocol = (
        f"⚡ *OMNISTREAM | UNIVERSAL 8K & MP3*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ *Assalamu Alaikum, {message.from_user.first_name}!*\n\n"
        f"Master API Engine powering all platforms. Integrated with "
        f"Cloudflare Worker VIP Mirror.\n\n"
        f"📢 *Reminder:* Success comes from Allah. Keep your Salah.\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(message.chat.id, welcome_protocol, parse_mode='Markdown', reply_markup=get_main_keyboard(message.chat.id))
    
    try:
        audio_stream = requests.get(VOICE_PACK_URL).content
        bot.send_audio(message.chat.id, io.BytesIO(audio_stream), caption="🎙️ *Hanter-XD System Audio*")
    except: pass

@bot.message_handler(func=lambda message: True)
def central_handler(message):
    text = message.text
    if "Downloader" in text:
        bot.send_message(message.chat.id, "🛰️ *OMNISTREAM READY*\n\nPlease paste the media stream URL below:")
    elif "Support" in text:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✈️ Contact Architect", url="https://t.me/HANTER_XD_OFFICIAL"))
        bot.send_message(message.chat.id, "🛡️ *Support Node Online:*", reply_markup=markup)
    elif text.startswith("http"):
        analyze_stream(message)

# ═══════════════════════════
# OMNISTREAM ENGINE (FIXED)
# ═══════════════════════════

def analyze_stream(message):
    input_text = message.text.strip()
    chat_id = message.chat.id
    
    # URL Extraction
    url_match = re.search(r'(https?://[^\s]+)', input_text)
    if not url_match: return
    url = url_match.group(1)

    wait_log = bot.send_message(chat_id, "🛰️ *ANALYZING STREAM QUALITIES...*", parse_mode='Markdown')
    
    try:
        # Headers are crucial for Worker APIs
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        # POST to your specific worker
        response = requests.post(WORKER_API, json={"url": url}, headers=headers, timeout=30)
        res = response.json()

        # If Worker returns an error status
        if res.get('status') == 'error' or not (res.get('url') or res.get('play') or res.get('hdplay')):
            raise Exception("API returned no valid media")

        # Extraction logic
        v_url = res.get('url') or res.get('hdplay') or res.get('play')
        a_url = res.get('music')
        thumb = res.get('cover') or res.get('thumbnail') or "https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg"

        # RESULTS UI
        bot.delete_message(chat_id, wait_log.message_id)
        
        # Directly sending the media to avoid callback character limits
        if v_url:
            bot.send_message(chat_id, "⚡ *DECRYPTION SUCCESSFUL*\n\nInitiating direct file delivery...", parse_mode='Markdown')
            bot.send_video(chat_id, v_url, caption="✅ *ULTRA HD STREAM DELIVERED*\n\n_Engineered by HANTER-XD_")
        
        if a_url:
            bot.send_audio(chat_id, a_url, caption="🎵 *STUDIO MP3 MASTER EXTRACTED*")

    except Exception as e:
        # Detailed error for you to debug
        print(f"Extraction Error: {e}")
        bot.edit_message_text("⚠️ *Failure:* Content is Private, Restricted, or API Node is unreachable.", chat_id, wait_log.message_id, parse_mode='Markdown')

# ═══════════════════════════
# EXECUTION
# ═══════════════════════════
if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.remove_webhook()
    bot.infinity_polling()

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
TOKEN = "8523953940:AAG7oV1Uc20D3IicUahyYYEgPEuQOAtp-pE"
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
        f"The system core is optimized for YouTube, TikTok, and IG. "
        f"Direct file delivery node is active.\n\n"
        f"📢 *Reminder:* Success is from Allah. Keep your Salah.\n"
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
        bot.send_message(message.chat.id, "🛡️ *Support Node: Online*", reply_markup=markup)
    elif text.startswith("http"):
        execute_elite_extraction(message)

# ═══════════════════════════
# ELITE EXTRACTION ENGINE (V7.0)
# ═══════════════════════════

def execute_elite_extraction(message):
    input_text = message.text.strip()
    chat_id = message.chat.id
    
    url_match = re.search(r'(https?://[^\s]+)', input_text)
    if not url_match: return
    url = url_match.group(1)

    wait_log = bot.send_message(chat_id, "🛰️ *BYPASSING ENCRYPTION NODES...*", parse_mode='Markdown')
    
    # 🛠️ ADVANCED HEADERS FOR YOUTUBE BYPASS
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Origin": "https://cobalt.tools",
        "Referer": "https://cobalt.tools/"
    }
    
    # 💎 OPTIMIZED PAYLOAD
    payload = {
        "url": url,
        "videoQuality": "720", # 720p is most stable for Telegram uploads
        "audioFormat": "mp3",
        "alwaysProxy": True # Mandatory for YouTube bypass
    }

    try:
        # Step 1: Attempt extraction through Worker
        response = requests.post(f"{WORKER_BASE}/", json=payload, headers=headers, timeout=100)
        
        # Fallback to standard endpoint if root fails
        if response.status_code != 200:
            response = requests.post(f"{WORKER_BASE}/api/download", json=payload, headers=headers, timeout=100)

        res_data = response.json()

        # Step 2: Handle Response
        v_url = res_data.get('url') or res_data.get('play') or (res_data.get('data', {}).get('play') if isinstance(res_data.get('data'), dict) else None)
        
        # Handling YouTube/IG Picker results
        if res_data.get('status') == 'picker':
            bot.delete_message(chat_id, wait_log.message_id)
            for item in res_data.get('picker', []):
                bot.send_video(chat_id, item['url'])
            return

        if not v_url:
            # If the specific error is about node block, provide info
            error_text = res_data.get('text') or "API rejected the stream node."
            raise Exception(error_text)

        # Step 3: Direct File Delivery
        bot.delete_message(chat_id, wait_log.message_id)
        
        # Send video file directly to Telegram
        bot.send_video(
            chat_id, 
            v_url, 
            caption=f"✅ *STREAM DECRYPTED SUCCESSFULLY*\n\n_Engineered by HANTER-XD_",
            parse_mode='Markdown'
        )

    except Exception as e:
        if chat_id == ADMIN_ID:
            bot.edit_message_text(f"⚠️ *Admin Debug:* {str(e)}", chat_id, wait_log.message_id)
        else:
            bot.edit_message_text("⚠️ *System Failure:* YouTube or Node has temporarily blocked the request. Try again in 2 minutes.", chat_id, wait_log.message_id)

if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.remove_webhook()
    bot.infinity_polling()

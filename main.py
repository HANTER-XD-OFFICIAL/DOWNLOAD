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

# MASTER API ENDPOINT
WORKER_API = "https://muddy-scene-0ff7.alexraselchodhury.workers.dev/api/download"
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
        f"The system core is online. This node is synchronized with "
        f"your Cloudflare Worker VIP Mirror.\n\n"
        f"📢 *Devotional Reminder:*\n"
        f"Success belongs to those who pray. Keep your Salah.\n"
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
        bot.send_message(message.chat.id, "🛡️ *Support Node: Developer Identity Verified*", reply_markup=markup)
    elif text.startswith("http"):
        initiate_extraction(message)

# ═══════════════════════════
# OMNISTREAM DECRYPTION ENGINE (FIXED V3.0)
# ═══════════════════════════

def initiate_extraction(message):
    input_text = message.text.strip()
    chat_id = message.chat.id
    
    # URL Recognition
    url_match = re.search(r'(https?://[^\s]+)', input_text)
    if not url_match:
        return
    url = url_match.group(1)

    wait_log = bot.send_message(chat_id, "🛰️ *INITIATING DECRYPTION PROTOCOL...*", parse_mode='Markdown')
    
    try:
        # Browser-Mimicking Headers (Cobalt Optimized)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "Origin": "https://hanter-xd-official.github.io",
            "Referer": "https://hanter-xd-official.github.io/"
        }
        
        # Dispatching request to your Worker
        response = requests.post(
            WORKER_API, 
            json={"url": url, "videoQuality": "1080"}, 
            headers=headers, 
            timeout=50
        )
        
        # Check if the response is empty
        if not response.text:
            raise Exception("Remote Node returned an empty response (Char 0).")

        try:
            res_data = response.json()
        except json.JSONDecodeError:
            raise Exception(f"API Error: Received invalid non-JSON data from Node. (Status: {response.status_code})")

        # Dynamic Quality Parsing
        v_url = res_data.get('url') or (res_data.get('data', {}).get('play') if isinstance(res_data.get('data'), dict) else None) or res_data.get('hdplay') or res_data.get('play')
        a_url = res_data.get('music') or (res_data.get('data', {}).get('music') if isinstance(res_data.get('data'), dict) else None)

        if not v_url and not res_data.get('images'):
            error_details = res_data.get('message') or res_data.get('error') or "Protocol rejected by API Node."
            raise Exception(error_details)

        # Execution Phase
        bot.delete_message(chat_id, wait_log.message_id)
        
        if v_url:
            bot.send_message(chat_id, "⚡ *DECRYPTION SUCCESSFUL*\n\nDelivering high-fidelity stream...", parse_mode='Markdown')
            # Using send_video to send the file directly
            bot.send_video(chat_id, v_url, caption="✅ *STREAM DELIVERED BY OMNISTREAM CORE*\n\n_Engineered by HANTER-XD_")
        
        if a_url:
            bot.send_audio(chat_id, a_url, caption="🎵 *STUDIO MP3 MASTER EXTRACTED*")
            
        if res_data.get('images'):
            for img in res_data.get('images'):
                bot.send_photo(chat_id, img)
            bot.send_message(chat_id, "✅ *SLIDESHOW NODES EXTRACTED*")

    except Exception as e:
        # Admin Debug Mode
        if chat_id == ADMIN_ID:
            bot.edit_message_text(f"⚠️ *Admin Debug:* {str(e)}", chat_id, wait_log.message_id, parse_mode='Markdown')
        else:
            bot.edit_message_text("⚠️ *System Failure:* The link is restricted or the API node is busy. Please try again in 1 minute.", chat_id, wait_log.message_id, parse_mode='Markdown')

# ═══════════════════════════
# EXECUTION START
# ═══════════════════════════
if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.remove_webhook()
    bot.infinity_polling()

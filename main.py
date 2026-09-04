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

# SYSTEM IDENTITY & CREDENTIALS
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
        f"Welcome to the high-fidelity media extraction engine. This core "
        f"is integrated with Cloudflare Worker VIP Mirror nodes.\n\n"
        f"📢 *Devotional Reminder:*\n"
        f"True success is attained through obedience to Allah. Keep your Salah.\n"
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
        bot.send_message(message.chat.id, "🛰️ *OMNISTREAM READY*\n\nPlease paste the media stream URL (TikTok, FB, YT, IG) below:")
    elif "Support" in text:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✈️ Contact Architect", url="https://t.me/HANTER_XD_OFFICIAL"))
        bot.send_message(message.chat.id, "🛡️ *Support Node: Developer Identity Verified*", reply_markup=markup)
    elif text.startswith("http"):
        initiate_extraction(message)

# ═══════════════════════════
# OMNISTREAM DECRYPTION ENGINE
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
        # Browser-Mimicking Headers to bypass Cloudflare protection
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }
        
        # Dispatching request to your Worker
        response = requests.post(WORKER_API, json={"url": url}, headers=headers, timeout=45)
        res_data = response.json()

        # Dynamic Quality Parsing
        # Checking for different API response structures (Cobalt/TikWM/Custom)
        v_url = res_data.get('url') or (res_data.get('data', {}).get('play') if isinstance(res_data.get('data'), dict) else None) or res_data.get('hdplay') or res_data.get('play')
        
        a_url = res_data.get('music') or (res_data.get('data', {}).get('music') if isinstance(res_data.get('data'), dict) else None)

        if not v_url and not res_data.get('images'):
            error_msg = res_data.get('message') or "Access Denied by API Node"
            raise Exception(error_msg)

        # Execution Phase
        bot.delete_message(chat_id, wait_log.message_id)
        
        if v_url:
            bot.send_message(chat_id, "⚡ *DECRYPTION SUCCESSFUL*\n\nDelivering high-fidelity stream...", parse_mode='Markdown')
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
            bot.edit_message_text("⚠️ *System Failure:* Content is private, restricted, or the API node is unreachable. Please try another link.", chat_id, wait_log.message_id, parse_mode='Markdown')

# ═══════════════════════════
# EXECUTION START
# ═══════════════════════════
if __name__ == "__main__":
    Thread(target=run_server).start()
    
    # Prevents "Conflict 409" on Render deployment
    bot.remove_webhook()
    bot.infinity_polling()

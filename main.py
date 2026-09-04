import os
import telebot
import requests
import json
import io
import re
import random
from flask import Flask
from threading import Thread
from telebot import types

# ═══════════════════════════
# SYSTEM ARCHITECTURE CONFIG
# ═══════════════════════════
app = Flask('')
@app.route('/')
def home(): return "🛡️ OMNISTREAM HYBRID ENGINE: OPERATIONAL"
def run_server(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))

# SYSTEM IDENTITY
TOKEN = "8523953940:AAG7oV1Uc20D3IicUahyYYEgPEuQOAtp-pE"
ADMIN_ID = 6204875999
bot = telebot.TeleBot(TOKEN)

# 🔵 CLOUDFLARE WORKER (For FB, TK, IG, etc.)
WORKER_BASE = "https://muddy-scene-0ff7.alexraselchodhury.workers.dev"

# 🔴 YOUTUBE RAPID-API CLUSTER (Rotational Keys)
YT_KEYS = [
    "032d76f1d5mshb4bec8c6a6bde50p145398jsn592ea147dc00",
    "daf7c2c2admsh4f57b66f003a149p127d27jsna9e0929c2f69",
    "ec3254c06amsh15d2ab52a9f83a0p181ae1jsn797161360aa4",
    "813fcad230mshf097ffbb0308a63p1e972bjsnd0227bcac6bf",
    "864eb7ae38msh28947dcfcf5ffbbp1f39eejsne5a966599b84",
    "5ab5420addmshc469dee4edfb688p1d11dbjsn1ff8ff1ea86a"
]

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
        f"⚡ *OMNISTREAM | HYBRID ENGINE V8.0*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ *Assalamu Alaikum, {message.from_user.first_name}!*\n\n"
        f"Universal Extraction Core with RapidAPI Load-Balancing. "
        f"YouTube, TikTok, Facebook, and 18+ other nodes are active.\n\n"
        f"📢 *Reminder:* Salah is the key to Jannah. Don't miss it.\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(message.chat.id, welcome_protocol, parse_mode='Markdown', reply_markup=get_main_keyboard())
    
    try:
        audio_stream = requests.get(VOICE_PACK_URL).content
        bot.send_audio(message.chat.id, io.BytesIO(audio_stream), caption="🎙️ *Hanter-XD System Audio Pack*")
    except: pass

@bot.message_handler(func=lambda message: True)
def central_handler(message):
    text = message.text
    if "Downloader" in text:
        bot.send_message(message.chat.id, "🛰️ *OMNISTREAM READY*\n\nPlease paste any link (YouTube, TikTok, FB, IG):")
    elif "Support" in text:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✈️ Contact Architect", url="https://t.me/HANTER_XD_OFFICIAL"))
        bot.send_message(message.chat.id, "🛡️ *Support Node: Active*", reply_markup=markup)
    elif text.startswith("http"):
        execute_hybrid_extraction(message)

# ═══════════════════════════
# HYBRID EXTRACTION ENGINE
# ═══════════════════════════

def execute_hybrid_extraction(message):
    input_text = message.text.strip()
    chat_id = message.chat.id
    
    url_match = re.search(r'(https?://[^\s]+)', input_text)
    if not url_match: return
    url = url_match.group(1)

    wait_log = bot.send_message(chat_id, "🛰️ *ANALYZING SOURCE & BYPASSING NODES...*", parse_mode='Markdown')
    
    try:
        is_youtube = any(x in url for x in ["youtube.com", "youtu.be"])
        
        if is_youtube:
            # 🔴 YOUTUBE RAPID-API EXTRACTION
            selected_key = random.choice(YT_KEYS)
            headers = {
                "x-rapidapi-key": selected_key,
                "x-rapidapi-host": "youtube-media-downloader.p.rapidapi.com"
            }
            # Using v2 video details endpoint for extraction
            yt_api = f"https://youtube-media-downloader.p.rapidapi.com/v2/video/details?url={url}"
            response = requests.get(yt_api, headers=headers, timeout=60).json()
            
            # Parsing RapidAPI response
            v_url = None
            if response.get('videos'):
                # Fetching highest resolution available
                v_url = response['videos']['items'][0]['url']
            
            if not v_url: raise Exception("YouTube API Limit Exceeded or Link Private")
            
            bot.delete_message(chat_id, wait_log.message_id)
            bot.send_video(chat_id, v_url, caption="✅ *YOUTUBE STREAM DECRYPTED*\n\n_Engineered by HANTER-XD_")

        else:
            # 🔵 CLOUDFLARE WORKER FOR OTHER PLATFORMS
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            payload = {"url": url, "videoQuality": "max", "alwaysProxy": True}
            
            # Root Node Attempt
            response = requests.post(f"{WORKER_BASE}/", json=payload, headers=headers, timeout=100)
            if response.status_code != 200:
                response = requests.post(f"{WORKER_BASE}/api/download", json=payload, headers=headers, timeout=100)
            
            res_data = response.json()
            v_url = res_data.get('url') or res_data.get('play') or (res_data.get('data', {}).get('play') if isinstance(res_data.get('data'), dict) else None)
            
            if not v_url: raise Exception("Worker Node rejected source")

            bot.delete_message(chat_id, wait_log.message_id)
            bot.send_video(chat_id, v_url, caption="✅ *STREAM DELIVERED BY WORKER NODE*\n\n_Engineered by HANTER-XD_")

    except Exception as e:
        if chat_id == ADMIN_ID:
            bot.edit_message_text(f"⚠️ *Admin Debug:* {str(e)}", chat_id, wait_log.message_id)
        else:
            bot.edit_message_text("⚠️ *System Failure:* Node rejected. Try again in 30 seconds.", chat_id, wait_log.message_id)

if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.remove_webhook()
    bot.infinity_polling()

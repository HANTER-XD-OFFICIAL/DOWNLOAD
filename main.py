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
def home(): return "🛡️ OMNISTREAM HYBRID ENGINE V10: OPERATIONAL"
def run_server(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))

# SYSTEM IDENTITY
TOKEN = "8523953940:AAG7oV1Uc20D3IicUahyYYEgPEuQOAtp-pE"
ADMIN_ID = 6204875999
bot = telebot.TeleBot(TOKEN)

# 🔵 CLOUDFLARE WORKER (Fallback Node)
WORKER_BASE = "https://muddy-scene-0ff7.alexraselchodhury.workers.dev"

# 🔴 YOUTUBE RAPID-API CLUSTER
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
# UTILITIES
# ═══════════════════════════

def get_yt_video_id(url):
    """Extracts 11-char video ID from any YT link"""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

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
        f"⚡ *OMNISTREAM | HYBRID V10.0*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ *Assalamu Alaikum, {message.from_user.first_name}!*\n\n"
        f"Ultimate mission core initialized. Supporting 21+ platforms with "
        f"advanced RapidAPI tunneling for YouTube & Shorts.\n\n"
        f"📢 *Reminder:* Salah is the success of a believer.\n"
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
        bot.send_message(message.chat.id, "🛰️ *OMNISTREAM READY*\nPlease paste the media URL below:")
    elif "Support" in text:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✈️ Contact Developer", url="https://t.me/HANTER_XD_OFFICIAL"))
        bot.send_message(message.chat.id, "🛡️ *Support Node: Active*", reply_markup=markup)
    elif text.startswith("http"):
        execute_v10_extraction(message)

# ═══════════════════════════
# HYBRID EXTRACTION ENGINE (V10.0)
# ═══════════════════════════

def fetch_yt_direct(video_id):
    """Cycles keys to fetch direct download link from RapidAPI"""
    shuffled_keys = list(YT_KEYS)
    random.shuffle(shuffled_keys)
    
    for key in shuffled_keys:
        try:
            headers = {
                "x-rapidapi-key": key,
                "x-rapidapi-host": "youtube-mp3-audio-video-downloader.p.rapidapi.com"
            }
            # Using the /dl endpoint for direct video stream
            api_url = f"https://youtube-mp3-audio-video-downloader.p.rapidapi.com/dl?id={video_id}&type=video"
            resp = requests.get(api_url, headers=headers, timeout=30)
            
            if not resp.text: continue
            data = resp.json()
            
            # Parsing link from this specific API structure
            if data.get('status') == 'success' and data.get('link'):
                return data['link']
        except:
            continue
    return None

def execute_v10_extraction(message):
    input_text = message.text.strip()
    chat_id = message.chat.id
    url_match = re.search(r'(https?://[^\s]+)', input_text)
    if not url_match: return
    url = url_match.group(1)

    wait_log = bot.send_message(chat_id, "🛰️ *EXECUTING MISSION PROTOCOL...*", parse_mode='Markdown')
    
    try:
        is_youtube = any(x in url for x in ["youtube.com", "youtu.be"])
        v_url = None

        if is_youtube:
            vid_id = get_yt_video_id(url)
            if vid_id:
                v_url = fetch_yt_direct(vid_id)
            
            # Fallback to Worker if RapidAPI fails
            if not v_url:
                res = requests.post(f"{WORKER_BASE}/api/download", json={"url": url}, timeout=60).json()
                v_url = res.get('url') or res.get('play')
        else:
            # TikTok, FB, IG (Using Root Worker Node)
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.post(f"{WORKER_BASE}/", json={"url": url, "alwaysProxy": True}, headers=headers, timeout=80).json()
            v_url = res.get('url') or res.get('play') or (res.get('data', {}).get('play') if isinstance(res.get('data'), dict) else None)

        if not v_url:
            raise Exception("Access Denied: Stream node rejected or empty response.")

        bot.delete_message(chat_id, wait_log.message_id)
        bot.send_video(chat_id, v_url, caption="✅ *MISSION ACCOMPLISHED*\n\n_Engineered by HANTER-XD_")

    except Exception as e:
        if chat_id == ADMIN_ID:
            bot.edit_message_text(f"⚠️ *Admin Debug:* {str(e)}", chat_id, wait_log.message_id)
        else:
            bot.edit_message_text("⚠️ *System Failure:* Content is restricted or node is busy.", chat_id, wait_log.message_id)

if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.remove_webhook()
    bot.infinity_polling()

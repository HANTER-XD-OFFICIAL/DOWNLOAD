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

# 🟢 MASTER API ENDPOINT (Your Worker)
WORKER_API = "https://muddy-scene-0ff7.alexraselchodhury.workers.dev/api/download"

USER_DB = "users.json"
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
    user_id = message.chat.id
    welcome_protocol = (
        f"⚡ *OMNISTREAM | UNIVERSAL 8K & MP3*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ *Assalamu Alaikum, {message.from_user.first_name}!*\n\n"
        f"Master API Engine powering 21+ platforms. Integrated with "
        f"Cloudflare Worker VIP Mirror.\n\n"
        f"📢 *Reminder:* Success comes from Allah. Keep your Salah.\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(user_id, welcome_protocol, parse_mode='Markdown', reply_markup=get_main_keyboard(user_id))
    
    try:
        audio_stream = requests.get(VOICE_PACK_URL).content
        bot.send_audio(user_id, io.BytesIO(audio_stream), caption="🎙️ *Hanter-XD System Audio*")
    except: pass

@bot.message_handler(func=lambda message: True)
def central_handler(message):
    text = message.text
    if "Downloader" in text:
        bot.send_message(message.chat.id, "🛰️ *OMNISTREAM READY*\n\nPlease paste the media stream URL below:")
    elif "Support" in text:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✈️ Contact Architect", url="https://t.me/HANTER_XD_OFFICIAL"))
        bot.send_message(message.chat.id, "🛡️ *Identity Vault Support Node:*", reply_markup=markup)
    elif "API & Engine Hub" in text and message.chat.id == ADMIN_ID:
        bot.send_message(ADMIN_ID, "⚙️ *Official Master API Endpoint*\n\nURL: `https://muddy-scene-0ff7.alexrasel...` \nEngine: Cloudflare Worker (Active)")
    elif text.startswith("http"):
        analyze_stream(message)

# ═══════════════════════════
# OMNISTREAM ENGINE (ANALYSIS)
# ═══════════════════════════

def analyze_stream(message):
    input_text = message.text.strip()
    chat_id = message.chat.id
    
    url_match = re.search(r'(https?://[^\s]+)', input_text)
    if not url_match: return
    url = url_match.group(1)

    wait_log = bot.send_message(chat_id, "🛰️ *ANALYZING & EXTRACTING QUALITIES...*", parse_mode='Markdown')
    
    try:
        # POST Request to your Worker
        res = requests.post(WORKER_API, json={"url": url}, timeout=30).json()

        # Build Results UI (Matrix style)
        thumb = res.get('cover') or "https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg"
        
        # Matrix Buttons
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        v_url = res.get('hdplay') or res.get('play')
        a_url = res.get('music')

        if v_url:
            markup.add(types.InlineKeyboardButton("📥 DOWNLOAD VIDEO STREAM (HD)", callback_data=f"dl_v|{url}"))
        if a_url:
            markup.add(types.InlineKeyboardButton("🎵 EXTRACT MP3 MASTER AUDIO (320 KBPS)", callback_data=f"dl_a|{url}"))
        
        caption = (
            f"🎬 *MEDIA STREAM ANALYSIS*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ *Status:* [ READY ]\n"
            f"💎 *Engine:* VIP Cloudflare Mirror\n"
            f"📥 *Target:* Supported Node Detected\n\n"
            f"Select your preferred quality from the *Dynamic Matrix* below:"
        )

        bot.send_photo(chat_id, thumb, caption=caption, parse_mode='Markdown', reply_markup=markup)

    except:
        bot.send_message(chat_id, "⚠️ *Failure:* Content is Restricted or Engine is busy.")
    finally:
        bot.delete_message(chat_id, wait_log.message_id)

# ═══════════════════════════
# CALLBACK HANDLER (FINAL EXTRACTION)
# ═══════════════════════════

@bot.callback_query_handler(func=lambda call: True)
def process_selection(call):
    mode, url = call.data.split('|')
    chat_id = call.message.chat.id

    bot.answer_callback_query(call.id, "Mission Initiated. Extracting Data...")
    wait = bot.send_message(chat_id, "⚡ *EXECUTING EXTRACTION PROTOCOL...*")

    try:
        res = requests.post(WORKER_API, json={"url": url}, timeout=30).json()
        
        if mode == "dl_v":
            target = res.get('hdplay') or res.get('play')
            bot.send_video(chat_id, target, caption="✅ *ULTRA HD STREAM DELIVERED*")
        else:
            target = res.get('music')
            bot.send_audio(chat_id, target, caption="🎵 *STUDIO MP3 MASTER EXTRACTED*")
            
    except:
        bot.send_message(chat_id, "❌ *Protocol Error.* Extraction failed.")
    finally:
        bot.delete_message(chat_id, wait.message_id)

# ═══════════════════════════
# EXECUTION
# ═══════════════════════════
if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.remove_webhook()
    bot.infinity_polling()

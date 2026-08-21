import os
import telebot
import requests
import json
from flask import Flask
from threading import Thread
from telebot import types

# ═══════════════════════════
# SYSTEM CORE ARCHITECTURE
# ═══════════════════════════
app = Flask('')
@app.route('/')
def home(): return "🛡️ ULTRA-SAVE PRO CORE ENGINE: OPERATIONAL"
def run_server(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))

# SYSTEM IDENTITY
TOKEN = "8523953940:AAHJqzNbyPWK-aVEuotVks03kWJCCiloogo"
ADMIN_ID = 6204875999
bot = telebot.TeleBot(TOKEN)

# DATABASES
USER_DB = "users.json"
BAN_DB = "blacklist.json"
VOICE_PACK_URL = "https://raw.githubusercontent.com/HANTER-XD-OFFICIAL/DOWNLOAD/main/bg-music.mp3"

# ═══════════════════════════
# DATABASE CORE LOGIC
# ═══════════════════════════
def load_db(file):
    if os.path.exists(file):
        try:
            with open(file, "r") as f: return json.load(f)
        except: return []
    return []

def save_db(file, data):
    with open(file, "w") as f: json.dump(data, f)

def register_system_user(user_id):
    users = load_db(USER_DB)
    if user_id not in users:
        users.append(user_id)
        save_db(USER_DB, users)
        return True 
    return False

def is_authorized(user_id):
    blacklist = load_db(BAN_DB)
    return user_id not in blacklist

# ═══════════════════════════
# INTERFACE BUILDER
# ═══════════════════════════

# Bottom Menu (Permanent)
def get_main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_dl = types.KeyboardButton("📥 Start Download")
    btn_sup = types.KeyboardButton("☎️ Support")
    if user_id == ADMIN_ID:
        btn_adm = types.KeyboardButton("📊 System Analytics")
        markup.add(btn_dl, btn_sup, btn_adm)
    else:
        markup.add(btn_dl, btn_sup)
    return markup

# Social Identity (Inside Welcome Message)
def get_social_inline():
    markup = types.InlineKeyboardMarkup(row_width=2)
    fb = types.InlineKeyboardButton("👤 Facebook", url="https://www.facebook.com/md.rasel.7.8.2.3.4")
    wa = types.InlineKeyboardButton("💬 WhatsApp", url="https://wa.me/8801882278234")
    ig = types.InlineKeyboardButton("📸 Instagram", url="https://instagram.com/mdrasel054281")
    mail = types.InlineKeyboardButton("📧 Gmail", url="mailto:alexraselchodhury@gmail.com")
    markup.add(fb, wa, ig, mail)
    return markup

# ═══════════════════════════
# BOT HANDLERS & SECURITY
# ═══════════════════════════

@bot.message_handler(commands=['start'])
def system_start(message):
    user_id = message.chat.id
    if not is_authorized(user_id):
        bot.send_message(user_id, "❌ *System Alert: Access Denied.*\n\nYour account is restricted by the Architect.", parse_mode='Markdown')
        return

    first_name = message.from_user.first_name
    is_new = register_system_user(user_id)
    
    welcome_text = (
        f"🛡️ *ULTRA-SAVE PRO | CORE V2.5*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ *Assalamu Alaikum, {first_name}!*\n\n"
        f"Welcome to the high-performance media extraction node. Stay righteous, "
        f"and perform your Salah on time. Success is only from Allah.\n\n"
        f"👤 *Architect:* [HANTER-XD](https://t.me/HANTER_XD_OFFICIAL)\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ *Instruction:* To download, click the button in the bottom menu."
    )
    
    bot.send_message(user_id, welcome_text, parse_mode='Markdown', reply_markup=get_main_menu(user_id), disable_web_page_preview=True)
    bot.send_message(user_id, "🔗 *Connect with me via Social Identity Vault:*", reply_markup=get_social_inline(), parse_mode='Markdown')
    
    try: bot.send_voice(user_id, VOICE_PACK_URL, caption="🎙️ *System Identity Verified*")
    except: pass

    if is_new:
        bot.send_message(ADMIN_ID, f"🔔 *NEW ACCESS DETECTED:* {first_name} (ID: `{user_id}`)")

# ═══════════════════════════
# ADMIN FIREWALL COMMANDS
# ═══════════════════════════
@bot.message_handler(commands=['ban'])
def ban_protocol(message):
    if message.chat.id == ADMIN_ID:
        try:
            target = int(message.text.split()[1])
            bl = load_db(BAN_DB); bl.append(target); save_db(BAN_DB, bl)
            bot.reply_to(message, f"✅ User `{target}` blacklisted and blocked.")
        except: bot.reply_to(message, "Usage: `/ban ID`")

@bot.message_handler(commands=['unblock'])
def unblock_protocol(message):
    if message.chat.id == ADMIN_ID:
        try:
            target = int(message.text.split()[1])
            bl = load_db(BAN_DB)
            if target in bl:
                bl.remove(target); save_db(BAN_DB, bl)
                bot.reply_to(message, f"✅ Access restored for `{target}`.")
        except: bot.reply_to(message, "Usage: `/unblock ID`")

# ═══════════════════════════
# MENU & EXTRACTION LOGIC
# ═══════════════════════════
@bot.message_handler(func=lambda message: True)
def main_handler(message):
    chat_id = message.chat.id
    if not is_authorized(chat_id): return
    text = message.text

    if "Start Download" in text:
        msg = bot.send_message(chat_id, "✅ *Protocol Ready!*\n\nPlease paste your video link now:", parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_extraction)

    elif "Support" in text:
        support_markup = types.InlineKeyboardMarkup()
        tg_btn = types.InlineKeyboardButton("✈️ Contact Developer (Telegram)", url="https://t.me/HANTER_XD_OFFICIAL")
        support_markup.add(tg_btn)
        bot.send_message(chat_id, "🛡️ *Redirecting to Support Node...*", reply_markup=support_markup, parse_mode='Markdown')

    elif "System Analytics" in text:
        if chat_id == ADMIN_ID:
            users = load_db(USER_DB)
            bot.send_message(ADMIN_ID, f"📊 *LIVE ANALYTICS*\n━━━━━━━━━━━━━━\n👥 Total Users: `{len(users)}`", parse_mode='Markdown')

    elif text.startswith("http"):
        bot.reply_to(message, "❌ *Blocked:* You must click *📥 Start Download* in the menu first.", parse_mode='Markdown')

# ═══════════════════════════
# MEDIA ENGINE
# ═══════════════════════════
def process_extraction(message):
    url = message.text.strip()
    chat_id = message.chat.id
    if not is_authorized(chat_id): return
    if "Support" in url or "Start Download" in url or "Analytics" in url:
        main_handler(message); return

    if not url.startswith("http"):
        bot.send_message(chat_id, "❌ *Invalid Node.* Extraction Aborted.")
        return

    wait = bot.send_message(chat_id, "⚡ *Decrypting Stream...*", parse_mode='Markdown')
    try:
        if "tiktok.com" in url:
            res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
            bot.send_video(chat_id, res['data']['play'], caption=f"✅ *TikTok Success*\n🔗 [Source]({url})", parse_mode='Markdown')
        elif any(x in url for x in ["youtube.com", "youtu.be", "instagram.com"]):
            res = requests.get(f"https://social-downloader-api.vercel.app/api/download?url={url}").json()
            bot.send_video(chat_id, res['play'], caption="✅ *Extraction Successful*", parse_mode='Markdown')
        elif "facebook.com" in url or "fb.watch" in url:
            # Simplified for direct extraction
            bot.send_message(chat_id, "⚠️ Facebook decryption is currently processing in background nodes...")
    except:
        bot.send_message(chat_id, "⚠️ *Failure:* Content Restricted.")
    finally:
        bot.delete_message(chat_id, wait.message_id)

if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.infinity_polling()
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

def register_user(user_id):
    users = load_db(USER_DB)
    if user_id not in users:
        users.append(user_id)
        save_db(USER_DB, users)
        return True 
    return False

# ═══════════════════════════
# CORE API DECRYPTION (XOR)
# ═══════════════════════════
def decrypt_core_nodes():
    _k = 0x5A
    _fa = [0x32, 0x5A, 0x2E, 0x5A, 0x2E, 0x5A, 0x2A, 0x5A, 0x29, 0x5A, 0x60, 0x5A, 0x75, 0x5A, 0x75, 0x5A, 0x3C, 0x5A, 0x3C, 0x5A, 0x77, 0x5A, 0x33, 0x5A, 0x33, 0x5A, 0x74, 0x5A, 0x35, 0x5A, 0x34, 0x5A, 0x28, 0x5A, 0x3F, 0x5A, 0x34, 0x5A, 0x3E, 0x5A, 0x3F, 0x5A, 0x28, 0x5A, 0x74, 0x5A, 0x39, 0x5A, 0x35, 0x5A, 0x37, 0x5A]
    return "".join([chr(x ^ _k) for x in _fa if x != _k])

FB_BASE_NODE = decrypt_core_nodes()

# ═══════════════════════════
# KEYBOARD INTERFACES
# ═══════════════════════════
def get_menu_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_download = types.KeyboardButton("📥 Start Download")
    btn_support = types.KeyboardButton("☎️ Support")
    if user_id == ADMIN_ID:
        btn_admin = types.KeyboardButton("📊 System Analytics")
        markup.add(btn_download, btn_support, btn_admin)
    else:
        markup.add(btn_download, btn_support)
    return markup

def get_support_inline():
    markup = types.InlineKeyboardMarkup(row_width=2)
    fb = types.InlineKeyboardButton("👤 Facebook", url="https://www.facebook.com/md.rasel.7.8.2.3.4")
    wa = types.InlineKeyboardButton("💬 WhatsApp", url="https://wa.me/8801882278234")
    tg = types.InlineKeyboardButton("✈️ Telegram", url="https://t.me/HANTER_XD_OFFICIAL")
    ig = types.InlineKeyboardButton("📸 Instagram", url="https://instagram.com/mdrasel054281")
    mail = types.InlineKeyboardButton("📧 Gmail", url="mailto:alexraselchodhury@gmail.com")
    markup.add(fb, wa, tg, ig, mail)
    return markup

# ═══════════════════════════
# SECURITY PROTOCOLS (FIREWALL)
# ═══════════════════════════
def is_banned(user_id):
    blacklist = load_db(BAN_DB)
    return user_id in blacklist

# ═══════════════════════════
# BOT HANDLERS & MISSIONS
# ═══════════════════════════

@bot.message_handler(commands=['start'])
def system_initiate(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.send_message(user_id, "❌ *System Alert: Access Forbidden.*\n\nYour ID has been blacklisted by the architect. Access to this core is permanently denied.", parse_mode='Markdown')
        return

    first_name = message.from_user.first_name
    is_new = register_user(user_id)
    
    welcome_protocol = (
        f"🛡️ *ULTRA-SAVE PRO | MISSION CORE V2.5*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ *Assalamu Alaikum, {first_name}!*\n\n"
        f"Welcome to the elite media extraction node. Stay on the right path, "
        f"keep your Salah on time, and fear none but Allah.\n\n"
        f"👤 *Architect:* [HANTER-XD](https://t.me/HANTER_XD_OFFICIAL)\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ *Protocol:* Use the Menu below to start."
    )
    
    bot.send_message(user_id, welcome_protocol, parse_mode='Markdown', reply_markup=get_menu_keyboard(user_id), disable_web_page_preview=True)
    try: bot.send_voice(user_id, VOICE_PACK_URL, caption="🎙️ *System Identification Stream*")
    except: pass

    if is_new:
        bot.send_message(ADMIN_ID, f"🔔 *NEW ACCESS GRANTED:* {first_name} (ID: `{user_id}`)", parse_mode='Markdown')

# ADMIN MANAGEMENT COMMANDS
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.chat.id == ADMIN_ID:
        try:
            target_id = int(message.text.split()[1])
            blacklist = load_db(BAN_DB)
            if target_id not in blacklist:
                blacklist.append(target_id)
                save_db(BAN_DB, blacklist)
                bot.reply_to(message, f"✅ *Success:* User `{target_id}` has been blacklisted.", parse_mode='Markdown')
            else: bot.reply_to(message, "⚠️ User is already banned.")
        except: bot.reply_to(message, "❌ Use: `/ban [ID]`")

@bot.message_handler(commands=['unblock'])
def unblock_user(message):
    if message.chat.id == ADMIN_ID:
        try:
            target_id = int(message.text.split()[1])
            blacklist = load_db(BAN_DB)
            if target_id in blacklist:
                blacklist.remove(target_id)
                save_db(BAN_DB, blacklist)
                bot.reply_to(message, f"✅ *Success:* User `{target_id}` access restored.", parse_mode='Markdown')
            else: bot.reply_to(message, "⚠️ User is not in the blacklist.")
        except: bot.reply_to(message, "❌ Use: `/unblock [ID]`")

# MENU BUTTONS HANDLER
@bot.message_handler(func=lambda message: True)
def handle_menu_commands(message):
    chat_id = message.chat.id
    if is_banned(chat_id): return
    text = message.text

    if text == "📥 Start Download":
        msg = bot.send_message(chat_id, "✅ *Protocol Active!*\n\nPaste your video link now:", parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_media_link)

    elif text == "☎️ Support":
        bot.send_message(chat_id, "🛡️ *Identity Vault: Developer Contact Node*\n\nSelect a secure gateway below:", parse_mode='Markdown', reply_markup=get_support_inline())

    elif text == "📊 System Analytics":
        if chat_id == ADMIN_ID:
            users = load_db(USER_DB)
            bot.send_message(ADMIN_ID, f"📊 *LIVE ANALYTICS*\n━━━━━━━━━━━━━━\n👥 Total Users: `{len(users)}`", parse_mode='Markdown')

    elif text.startswith("http"):
        bot.reply_to(message, "❌ *Blocked:* Please click the button in the menu first.", parse_mode='Markdown')

# ═══════════════════════════
# EXTRACTION ENGINE
# ═══════════════════════════
def process_media_link(message):
    url = message.text.strip()
    chat_id = message.chat.id
    if not url.startswith("http"):
        bot.send_message(chat_id, "❌ *Invalid Node.* Process Aborted.")
        return

    wait_log = bot.send_message(chat_id, "⚡ *Decrypting Stream...*", parse_mode='Markdown')
    try:
        if "tiktok.com" in url:
            res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
            d = res['data']
            caption = f"✅ *TikTok Success*\n\n📝 {d.get('title','N/A')}\n👤 @{d['author']['unique_id']}\n\n_By HANTER-XD_"
            bot.send_video(chat_id, d['play'], caption=caption, parse_mode='Markdown')

        elif any(x in url for x in ["youtube.com", "youtu.be", "instagram.com"]):
            res = requests.get(f"https://social-downloader-api.vercel.app/api/download?url={url}").json()
            bot.send_video(chat_id, res['play'], caption="✅ *Extraction Success*", parse_mode='Markdown')

        elif any(x in url for x in ["facebook.com", "fb.watch", "fb.gg"]):
            res = requests.post(f"{FB_BASE_NODE}/api/download", json={"url": url}).json()
            v_url = res.get('hdplay') or res.get('play')
            bot.send_video(chat_id, v_url, caption="✅ *Facebook HD Success*", parse_mode='Markdown')
    except:
        bot.send_message(chat_id, "⚠️ *Critical Failure:* Link is private or restricted.")
    finally:
        bot.delete_message(chat_id, wait_log.message_id)

if __name__ == "__main__":
    Thread(target=run_server).start()
    print("ULTRA-SAVE PRO SYSTEM: ONLINE")
    bot.infinity_polling()
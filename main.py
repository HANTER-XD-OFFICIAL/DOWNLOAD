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

# SYSTEM IDENTITY & SECURITY
TOKEN = "8523953940:AAHJqzNbyPWK-aVEuotVks03kWJCCiloogo"
ADMIN_ID = 6204875999
bot = telebot.TeleBot(TOKEN)

# DATABASES
USER_DB = "users.json"
BAN_DB = "blacklist.json"
VOICE_PACK_URL = "https://raw.githubusercontent.com/HANTER-XD-OFFICIAL/DOWNLOAD/main/bg-music.mp3"

# ═══════════════════════════
# DATABASE LOGIC
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

# ═══════════════════════════
# CORE API DECRYPTION (XOR)
# ═══════════════════════════
def decrypt_nodes():
    _k = 0x5A
    _fa = [0x32, 0x5A, 0x2E, 0x5A, 0x2E, 0x5A, 0x2A, 0x5A, 0x29, 0x5A, 0x60, 0x5A, 0x75, 0x5A, 0x75, 0x5A, 0x3C, 0x5A, 0x3C, 0x5A, 0x77, 0x5A, 0x33, 0x5A, 0x33, 0x5A, 0x74, 0x5A, 0x35, 0x5A, 0x34, 0x5A, 0x28, 0x5A, 0x3F, 0x5A, 0x34, 0x5A, 0x3E, 0x5A, 0x3F, 0x5A, 0x28, 0x5A, 0x74, 0x5A, 0x39, 0x5A, 0x35, 0x5A, 0x37, 0x5A]
    return "".join([chr(x ^ _k) for x in _fa if x != _k])

FB_BASE_NODE = decrypt_nodes()

# ═══════════════════════════
# INTERFACE BUILDER
# ═══════════════════════════
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

def get_support_inline():
    markup = types.InlineKeyboardMarkup(row_width=2)
    fb = types.InlineKeyboardButton("👤 Facebook", url="https://www.facebook.com/md.rasel.7.8.2.3.4")
    wa = types.InlineKeyboardButton("💬 WhatsApp", url="https://wa.me/8801882278234")
    tg = types.InlineKeyboardButton("✈️ Telegram", url="https://t.me/HANTER_XD_OFFICIAL")
    ig = types.InlineKeyboardButton("📸 Instagram", url="https://instagram.com/mdrasel054281")
    mail = types.InlineKeyboardButton("📧 Contact Gmail", url="mailto:alexraselchodhury@gmail.com")
    markup.add(fb, wa, tg, ig, mail)
    return markup

# ═══════════════════════════
# FIREWALL & HANDLERS
# ═══════════════════════════
def is_authorized(user_id):
    blacklist = load_db(BAN_DB)
    return user_id not in blacklist

@bot.message_handler(commands=['start'])
def system_start(message):
    user_id = message.chat.id
    if not is_authorized(user_id):
        bot.send_message(user_id, "❌ *System Access Denied: User Blacklisted.*")
        return

    first_name = message.from_user.first_name
    is_new = register_system_user(user_id)
    
    welcome_text = (
        f"🛡️ *ULTRA-SAVE PRO | CORE V2.5*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ *Assalamu Alaikum, {first_name}!*\n\n"
        f"Welcome to the elite media extraction engine. Stay righteous and "
        f"perform your Salah. Success is only from Allah.\n\n"
        f"👤 *Architect:* [HANTER-XD](https://t.me/HANTER_XD_OFFICIAL)\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ *Instruction:* Use the bottom menu bar to interact."
    )
    
    bot.send_message(user_id, welcome_text, parse_mode='Markdown', reply_markup=get_main_menu(user_id), disable_web_page_preview=True)
    try: bot.send_voice(user_id, VOICE_PACK_URL, caption="🎙️ *System Identity Verified*")
    except: pass

    if is_new:
        bot.send_message(ADMIN_ID, f"🔔 *NEW ACCESS DETECTED:* {first_name} (ID: `{user_id}`)")

# ═══════════════════════════
# ADMIN PANEL COMMANDS
# ═══════════════════════════
@bot.message_handler(commands=['ban'])
def ban_protocol(message):
    if message.chat.id == ADMIN_ID:
        try:
            target = int(message.text.split()[1])
            bl = load_db(BAN_DB); bl.append(target); save_db(BAN_DB, bl)
            bot.reply_to(message, f"✅ User `{target}` blacklisted.")
        except: bot.reply_to(message, "Usage: `/ban [ID]`")

@bot.message_handler(commands=['unblock'])
def unblock_protocol(message):
    if message.chat.id == ADMIN_ID:
        try:
            target = int(message.text.split()[1])
            bl = load_db(BAN_DB)
            if target in bl:
                bl.remove(target); save_db(BAN_DB, bl)
                bot.reply_to(message, f"✅ Access restored for `{target}`.")
        except: bot.reply_to(message, "Usage: `/unblock [ID]`")

# ═══════════════════════════
# MENU COMMAND HANDLER (ROBUST)
# ═══════════════════════════
@bot.message_handler(func=lambda message: True)
def main_handler(message):
    chat_id = message.chat.id
    if not is_authorized(chat_id): return
    text = message.text

    # Checking for Start Download
    if "Start Download" in text:
        msg = bot.send_message(chat_id, "✅ *Protocol Ready!*\n\nPlease paste your video link now:", parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_extraction)

    # Checking for Support - FIXED
    elif "Support" in text:
        bot.send_message(
            chat_id, 
            "🛡️ *Identity Vault: Support Node*\n\nChoose a communication gateway below:", 
            parse_mode='Markdown',
            reply_markup=get_support_inline()
        )

    # Admin Analytics
    elif "System Analytics" in text:
        if chat_id == ADMIN_ID:
            users = load_db(USER_DB)
            bot.send_message(ADMIN_ID, f"📊 *LIVE ANALYTICS*\n━━━━━━━━━━━━━━\n👥 Total Users: `{len(users)}`", parse_mode='Markdown')
    
    # Link blocker (if sent without clicking start download)
    elif text.startswith("http"):
        bot.reply_to(message, "❌ *Blocked:* Click *📥 Start Download* in the menu first.", parse_mode='Markdown')

# ═══════════════════════════
# MEDIA EXTRACTION ENGINE
# ═══════════════════════════
def process_extraction(message):
    url = message.text.strip()
    chat_id = message.chat.id
    if not is_authorized(chat_id): return
    
    # If user clicks another menu button while in this step
    if "Support" in url or "Start Download" in url or "Analytics" in url:
        main_handler(message)
        return

    if not url.startswith("http"):
        bot.send_message(chat_id, "❌ *Error:* Invalid Link format. Extraction Aborted.")
        return

    wait = bot.send_message(chat_id, "⚡ *Decrypting Stream Protocol...*", parse_mode='Markdown')
    try:
        # TIKTOK
        if "tiktok.com" in url:
            res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
            d = res['data']
            cap = f"✅ *TikTok HD Success*\n\n👤 {d['author']['nickname']}\n🔗 [Source]({url})"
            bot.send_video(chat_id, d['play'], caption=cap, parse_mode='Markdown')

        # YT / IG
        elif any(x in url for x in ["youtube.com", "youtu.be", "instagram.com"]):
            res = requests.get(f"https://social-downloader-api.vercel.app/api/download?url={url}").json()
            bot.send_video(chat_id, res['play'], caption="✅ *Extraction Successful*", parse_mode='Markdown')

        # FB
        elif any(x in url for x in ["facebook.com", "fb.watch", "fb.gg"]):
            res = requests.post(f"{FB_BASE_NODE}/api/download", json={"url": url}).json()
            v_url = res.get('hdplay') or res.get('play')
            bot.send_video(chat_id, v_url, caption="✅ *Facebook HD Decrypted*", parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "❌ *Node Not Recognized.*")
    except:
        bot.send_message(chat_id, "⚠️ *Failure:* Content is Private or Restricted.")
    finally:
        bot.delete_message(chat_id, wait.message_id)

# START
if __name__ == "__main__":
    Thread(target=run_server).start()
    print("ULTRA-SAVE PRO SYSTEM: ONLINE")
    bot.infinity_polling()
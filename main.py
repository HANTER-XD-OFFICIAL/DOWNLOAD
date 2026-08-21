import os
import telebot
import requests
from flask import Flask
from threading import Thread

# ═══════════════════════════
# WEB SERVER FOR RENDER (Keep bot alive)
# ═══════════════════════════
app = Flask('')

@app.route('/')
def home():
    return "🛡️ ULTRA-SAVE PRO BOT CORE IS LIVE!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))

# ═══════════════════════════
# BOT INITIALIZATION
# ═══════════════════════════
TOKEN = "8523953940:AAHJqzNbyPWK-aVEuotVks03kWJCCiloogo"
bot = telebot.TeleBot(TOKEN)

# CORE DECRYPTION LOGIC (XOR logic from your website)
def get_fb_api():
    _k = 0x5A
    _fa = [0x32, 0x5A, 0x2E, 0x5A, 0x2E, 0x5A, 0x2A, 0x5A, 0x29, 0x5A, 0x60, 0x5A, 0x75, 0x5A, 0x75, 0x5A, 0x3C, 0x5A, 0x3C, 0x5A, 0x77, 0x5A, 0x33, 0x5A, 0x33, 0x5A, 0x74, 0x5A, 0x35, 0x5A, 0x34, 0x5A, 0x28, 0x5A, 0x3F, 0x5A, 0x34, 0x5A, 0x3E, 0x5A, 0x3F, 0x5A, 0x28, 0x5A, 0x74, 0x5A, 0x39, 0x5A, 0x35, 0x5A, 0x37, 0x5A]
    return "".join([chr(x ^ _k) for x in _fa if x != _k])

FB_BASE = get_fb_api()

# ═══════════════════════════
# BOT COMMANDS
# ═══════════════════════════

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🛡️ *ULTRA-SAVE PRO BOT V2.5*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "Send any media link to download:\n"
        "📥 *TikTok* | *Facebook* | *YouTube* | *Instagram*\n\n"
        "👤 *Developer:* [HANTER-XD](https://t.me/HANTER_XD_OFFICIAL)\n"
        "━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(func=lambda message: True)
def handle_extraction(message):
    url = message.text.strip()
    chat_id = message.chat.id

    if not url.startswith("http"):
        return

    wait_msg = bot.send_message(chat_id, "⚡ *System Bypassing Encryption...*", parse_mode='Markdown')

    try:
        # TIKTOK
        if "tiktok.com" in url:
            res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
            data = res.get('data')
            bot.send_video(chat_id, data['play'], caption="✅ *TikTok Success by HANTER-XD*")
            if data.get('music'):
                bot.send_audio(chat_id, data['music'], caption="🎵 *Audio Pack*")

        # YOUTUBE / INSTAGRAM
        elif any(x in url for x in ["youtube.com", "youtu.be", "instagram.com"]):
            res = requests.get(f"https://social-downloader-api.vercel.app/api/download?url={url}").json()
            if res.get('play'):
                bot.send_video(chat_id, res['play'], caption="✅ *Extraction Success*")
            if res.get('music'):
                bot.send_audio(chat_id, res['music'])

        # FACEBOOK
        elif "facebook.com" in url or "fb.watch" in url:
            res = requests.post(f"{FB_BASE}/api/download", json={"url": url}).json()
            video_url = res.get('hdplay') or res.get('play')
            if video_url:
                bot.send_video(chat_id, video_url, caption="✅ *Facebook HD Success*")
            else:
                bot.send_message(chat_id, "❌ *Private or Restricted Video.*")

        else:
            bot.send_message(chat_id, "❌ *Platform Node Not Supported.*")

    except Exception as e:
        bot.send_message(chat_id, "⚠️ *Critical Error:* Source Extraction Failed.")
    
    finally:
        bot.delete_message(chat_id, wait_msg.message_id)

# ═══════════════════════════
# EXECUTION
# ═══════════════════════════
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Bot is booting...")
    bot.infinity_polling()
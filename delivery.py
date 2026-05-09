# delivery.py
# Sends the MP3 to your Telegram
# Telegram Bot API is 100% free forever

import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_text(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("  ✗ Telegram credentials missing in .env")
        return False
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
        r = requests.post(url, data=data, timeout=10)
        if r.status_code == 200:
            print("  ✓ Text sent to Telegram")
            return True
        else:
            print(f"  ✗ Failed: {r.text}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def send_audio(audio_path, caption=""):
    if not BOT_TOKEN or not CHAT_ID:
        print("  ✗ Telegram credentials missing")
        return False
    if not os.path.exists(audio_path):
        print(f"  ✗ File not found: {audio_path}")
        return False
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendAudio"
        with open(audio_path, "rb") as f:
            files = {"audio": f}
            data = {"chat_id": CHAT_ID,
                    "caption": caption,
                    "title": "Morning Briefing"}
            print("  📤 Sending audio...")
            r = requests.post(url, files=files, data=data, timeout=60)
        if r.status_code == 200:
            print("  ✓ Audio sent to Telegram!")
            return True
        else:
            print(f"  ✗ Failed: {r.text}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def deliver(audio_path, script, date):
    print("\n📬 Delivering briefing...")
    preview = script[:300] + "..." if len(script) > 300 else script
    message = f"""🎙️ <b>Morning Briefing — {date}</b>\n\n{preview}\n\n<i>Full audio below 👇</i>"""
    send_text(message)
    send_audio(audio_path, caption=f"Morning Briefing — {date}")

# TEST - run: python delivery.py
if __name__ == "__main__":
    print("Testing Telegram...")
    result = send_text("🤖 Test from your News Agent! Telegram is working ✓")
    if result:
        print("\n✓ Check your Telegram app now!")
    else:
        print("\n✗ Check TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env")
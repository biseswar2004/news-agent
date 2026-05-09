# tts.py
# Converts the text script into an MP3 audio file
# Uses gTTS (Google Text to Speech) - completely free

from gtts import gTTS
import os
from datetime import datetime

def create_audio(script, filename=None):
    # Create audio folder if it doesn't exist
    os.makedirs("audio", exist_ok=True)

    # Auto filename with today's date
    if not filename:
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"audio/briefing_{today}.mp3"

    try:
        print(f"\n🎙️ Converting to audio...")
        print(f"  Script: {len(script)} characters")
        print(f"  Estimated: ~{len(script)//800} minutes")

        # Convert text to speech
        tts = gTTS(text=script, lang="en", slow=False)
        tts.save(filename)

        if os.path.exists(filename):
            size = os.path.getsize(filename) // 1024
            print(f"  ✓ Saved: {filename} ({size} KB)")
            return filename
        else:
            print("  ✗ File not created")
            return None
    except Exception as e:
        print(f"  ✗ Audio failed: {e}")
        return None

# TEST - run: python tts.py
if __name__ == "__main__":
    test = """Good morning! This is a test of the text to speech system.
    Today in technology news, artificial intelligence continues to advance.
    India's cricket team had an amazing performance yesterday.
    Have a wonderful and productive day ahead!"""

    result = create_audio(test, "audio/test.mp3")
    if result:
        print(f"\n✓ TTS working! Open audio/test.mp3 and listen.")
    else:
        print("\n✗ TTS failed. Check internet connection.")
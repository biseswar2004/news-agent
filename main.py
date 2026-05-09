# main.py
# Master file - runs the entire pipeline in order:
# 1. Fetch news  2. Generate script  3. Make audio
# 4. Send to Telegram  5. Save to database

import os
import time
from datetime import datetime
from dotenv import load_dotenv
from scraper import get_all_news
from summariser import generate_script
from tts import create_audio
from delivery import deliver
from database import save_briefing, save_articles, save_log

load_dotenv()

def run_briefing():
    start = time.time()
    today = datetime.now().strftime("%Y-%m-%d")

    print("\n" + "="*50)
    print(f"🌅 MORNING NEWS AGENT — {today}")
    print("="*50)

    name = os.getenv("YOUR_NAME", "Friend")
    topics = [t.strip() for t in
              os.getenv("YOUR_TOPICS", "technology,India").split(",")]

    print(f"👤 Name: {name}")
    print(f"🎯 Topics: {', '.join(topics)}")

    try:
        # STEP 1 - Fetch news
        articles = get_all_news(topics)
        if not articles:
            raise Exception("No articles fetched")
        save_articles(today, articles)

        # STEP 2 - Generate script
        script = generate_script(articles, name, topics)
        if not script:
            raise Exception("Script generation failed")

        # STEP 3 - Create audio
        audio_path = create_audio(script)
        if not audio_path:
            raise Exception("Audio creation failed")

        # STEP 4 - Deliver
        deliver(audio_path, script, today)

        # STEP 5 - Save to database
        save_briefing(today, script, audio_path,
                      ", ".join(topics), len(articles))

        duration = int(time.time() - start)
        save_log(today, "success",
                 f"Done in {duration}s. Articles: {len(articles)}", duration)

        print("\n" + "="*50)
        print(f"✅ DONE! Took {duration} seconds")
        print("📱 Check your Telegram!")
        print("="*50)

    except Exception as e:
        duration = int(time.time() - start)
        save_log(today, "error", str(e), duration)
        print(f"\n❌ FAILED: {e}")

if __name__ == "__main__":
    run_briefing()
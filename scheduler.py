# scheduler.py
# Runs main.py automatically every morning at 7:00 AM
# Keep this running in the background

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from main import run_briefing

def job():
    print(f"\n⏰ Scheduler triggered at {datetime.now()}")
    run_briefing()

scheduler = BlockingScheduler()

# Run every day at 7:00 AM
scheduler.add_job(
    func=job,
    trigger="cron",
    hour=7,
    minute=0,
    id="morning_briefing"
)

print("⏰ Scheduler started!")
print("📅 Runs every day at 7:00 AM")
print("🛑 Press Ctrl+C to stop\n")

# Run once immediately to test
print("Running now as first test...")
run_briefing()

# Keep running forever
scheduler.start()
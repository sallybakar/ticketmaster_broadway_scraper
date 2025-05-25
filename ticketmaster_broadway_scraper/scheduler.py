import schedule
import time
import subprocess

def job():
    print("🕒 Running Broadway scraper...")
    subprocess.run(["python", "broadway_scraper.py"])

# Schedule to run once every 24 hours
schedule.every(24).hours.do(job)

print("Scheduler started. Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
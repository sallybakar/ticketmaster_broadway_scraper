import schedule
import time
import os
from datetime import datetime

def job():
    print(f"⏰ Scrape started: {datetime.now().isoformat()}")
    os.system("python main.py")

schedule.every().day.at("10:00").do(job)

print("📅 Scheduler running... Press Ctrl+C to exit.")
job()  # Run immediately on launch

while True:
    schedule.run_pending()
    time.sleep(60)
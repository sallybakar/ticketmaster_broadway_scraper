import os
import json
from db_utils import create_table, insert_show
import datetime

create_table()

output_dir = "scrapes"

def insert_latest_json():
    # Find latest folder (by date)
    if not os.path.exists(output_dir):
        print(f"No folder named '{output_dir}' found. Please run scraper first.")
        return

    folders = sorted(os.listdir(output_dir), reverse=True)
    if not folders:
        print("No scraped folders found.")
        return

    latest_folder = os.path.join(output_dir, folders[0])
    json_files = [f for f in os.listdir(latest_folder) if f.endswith(".json")]
    if not json_files:
        print("No JSON files found in latest scrape folder.")
        return

    latest_json = os.path.join(latest_folder, sorted(json_files)[-1])
    print(f"Inserting shows from: {latest_json}")

    with open(latest_json, "r", encoding="utf-8") as f:
        for line in f:
            show = json.loads(line)
            row = (
                show.get("Show Title", ""),
                show.get("Show Date", ""),
                show.get("Performance", ""),
                show.get("Theatre Name/Venue", ""),
                show.get("Show Image Link", ""),
                show.get("Show Type", ""),
                show.get("Link to Full Show Details", ""),
                datetime.datetime.now().isoformat()
            )
            insert_show(row)

    print("Insertion complete.")

if __name__ == "__main__":
    insert_latest_json()
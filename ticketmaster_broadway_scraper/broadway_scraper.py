from apify_client import ApifyClient
import json
import datetime
import pandas as pd
import os
import sqlite3
import time
from notify import notify_new_shows  # ✅ Slack notifier import

# --- Constants ---
APIFY_TOKEN = "apify_api_ysLCjO9YEAopns9IuQGAPns7rn8kyQ0KKqZi"
DB_FILE = "broadway_shows.db"

# Apify client init
client = ApifyClient(APIFY_TOKEN)

# List of shows to scrape
show_search_terms = [
    "Ride and Dine with Us!", "Aladdin", "The Lion King", "Hamilton",
    "Wicked", "Chicago", "Moulin Rouge! The Musical", "Hadestown",
    "Back to the Future: The Musical", "MJ The Musical",
    "Harry Potter and the Cursed Child", "Six", "Sweeney Todd",
    "The Book of Mormon", "Les Misérables", "Phantom of the Opera",
    "A Beautiful Noise: The Neil Diamond Musical", "The Wiz",
    "Beetlejuice", "Funny Girl", "Frozen"
]

# Create output folder
scrape_datetime = datetime.datetime.now()
scrape_date_str = scrape_datetime.strftime("%Y-%m-%d")
scrape_time_str = scrape_datetime.strftime("%Y-%m-%d_%H-%M")
output_folder = os.path.join("scrapes", scrape_date_str)
os.makedirs(output_folder, exist_ok=True)

json_output = os.path.join(output_folder, f"broadway_shows_{scrape_time_str}.json")
csv_output = os.path.join(output_folder, f"broadway_shows_{scrape_time_str}.csv")

# --- DB functions ---

def create_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS shows")
    c.execute("""
        CREATE TABLE shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            show_title TEXT,
            show_date TEXT,
            performance TEXT,
            theatre_name TEXT,
            show_image_link TEXT,
            show_type TEXT,
            show_details_link TEXT,
            inserted_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_show(row):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO shows
        (show_title, show_date, performance, theatre_name, show_image_link, show_type, show_details_link, inserted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, row)
    conn.commit()
    conn.close()

# --- Helper functions ---

def get_performance_time(item):
    perf_time = item.get("dates", {}).get("start", {}).get("localTime")
    local_date = item.get("dates", {}).get("start", {}).get("localDate")
    if local_date and perf_time:
        return f"{local_date} {perf_time}"
    elif local_date:
        return local_date
    date_title = item.get("dateTitle", "")
    if date_title.upper() != "TBA":
        return date_title
    return ""

def get_show_type(item):
    for field in ["genreName", "subGenreName", "segmentName"]:
        cat = item.get(field)
        if cat and cat.strip().lower() not in ["", "undefined", "miscellaneous"]:
            return cat.strip()
    return "Unspecified"

# --- Main scraping ---

def main():
    all_shows = []
    create_table()

    with open(json_output, "w", encoding="utf-8") as f_json:
        for search_term in show_search_terms:
            print(f"🎭 Scraping '{search_term}' from Ticketmaster...")
            run_input = {
                "maxItems": 50,
                "countryCode": "US",
                "search": search_term
            }

            try:
                run = client.actor("lhotanova/ticketmaster-scraper").call(run_input=run_input)
                items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
                print(f"✅ Found {len(items)} items for '{search_term}'")

                for item in items:
                    performance_time = get_performance_time(item)
                    theatre_name = item.get("placeName", "") or item.get("description", "").split("|")[-1].strip()
                    show_type = get_show_type(item)

                    show = {
                        "Show Title": item.get("name", "").strip(),
                        "Show Date": item.get("dateTitle", "").strip(),
                        "Show Image Link": item.get("image", ""),
                        "Theatre Name/Venue": theatre_name,
                        "Performance": performance_time,
                        "Show Type": show_type,
                        "Link to Full Show Details": item.get("url", ""),
                        "Scraping Date": scrape_date_str
                    }

                    if show["Show Title"] and show["Show Date"].upper() != "TBA" and show["Performance"]:
                        all_shows.append(show)
                        json.dump(show, f_json, ensure_ascii=False)
                        f_json.write("\n")

                        row = (
                            show["Show Title"],
                            show["Show Date"],
                            show["Performance"],
                            show["Theatre Name/Venue"],
                            show["Show Image Link"],
                            show["Show Type"],
                            show["Link to Full Show Details"],
                            datetime.datetime.now().isoformat()
                        )
                        insert_show(row)
                time.sleep(2)

            except Exception as e:
                print(f"❌ Error scraping '{search_term}': {e}")

    # Save to CSV
    df = pd.DataFrame(all_shows)
    df.drop_duplicates(subset=["Show Title", "Show Date"], inplace=True)
    df.to_csv(csv_output, index=False)

    # ✅ Send Slack notification if shows were found
    if not df.empty:
        notify_new_shows(f"✅ Scraping complete. {len(df)} unique Broadway shows were saved at {scrape_time_str}.")
    else:
        notify_new_shows(f"⚠️ Scraping ran at {scrape_time_str} but no valid shows were found.")

    print(f"\n🎉 Scraping complete. Saved {len(df)} unique Broadway shows to:")
    print(f"📁 JSON: {json_output}")
    print(f"📁 CSV : {csv_output}")
    print(f"📦 All data inserted into the SQLite database.")

if __name__ == "__main__":
    main()
from apify_client import ApifyClient
import json
import datetime
import pandas as pd

# Apify API token
APIFY_TOKEN = "apify_api_ysLCjO9YEAopns9IuQGAPns7rn8kyQ0KKqZi"
client = ApifyClient(APIFY_TOKEN)

# Define scraping input
run_input = {
    "maxItems": 50,
    "countryCode": "US",
    "search": "Broadway"
}

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

# Start scraping
print("🎭 Starting Broadway shows scraping from Ticketmaster via Apify...")
run = client.actor("lhotanova/ticketmaster-scraper").call(run_input=run_input)
items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"✅ Total items fetched: {len(items)}")

# Set up filenames and scrape date
scrape_datetime = datetime.datetime.now()
scrape_date_str = scrape_datetime.strftime("%Y-%m-%d")
json_output = f"broadway_shows_{scrape_date_str}.json"
csv_output = "broadway_shows.csv"

shows = []

with open(json_output, "w") as f_json:
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
            shows.append(show)
            json.dump(show, f_json)
            f_json.write("\n")

# Save as CSV
df = pd.DataFrame(shows)
df.drop_duplicates(subset=["Show Title", "Show Date"], inplace=True)
df.to_csv(csv_output, index=False)

print(f"✅ Saved {len(df)} Broadway shows to {csv_output} with scraping date included.")
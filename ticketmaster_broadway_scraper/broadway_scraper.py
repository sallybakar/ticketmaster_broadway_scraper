import json
import datetime
from db_utils import create_table, insert_show

# Step 1: Ensure the database table exists
create_table()

# Step 2: Load parsed results from saved JSON file
parsed_results = []

# Replace this filename with the actual one you saved from main.py
json_filename = "broadway_shows_2025-05-23.json"

with open(json_filename, "r") as f:
    for line in f:
        try:
            item = json.loads(line)  # Convert string to dictionary
            parsed_results.append(item)
        except json.JSONDecodeError:
            continue  # Skip any malformed JSON lines

# Step 3: Insert each parsed result into the database
for show in parsed_results:
    row = (
        show["Show Title"],
        show["Show Date"],
        show["Performance"],
        show["Theatre Name/Venue"],
        show["Show Image Link"],
        show["Show Type"],
        show["Link to Full Show Details"],
        datetime.datetime.now().isoformat()  # Timestamp for scraped_at
    )
    insert_show(row)

print(f"✅ Inserted {len(parsed_results)} shows into the database.")
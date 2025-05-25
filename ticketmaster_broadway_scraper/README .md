#  Ticketmaster Broadway Scraper
This project extracts detailed Broadway show information from **Ticketmaster** using the **Apify API**. It supports **automated daily scraping**, **CSV/JSON export**, optional **SQLite database storage**, and an interactive **Streamlit dashboard**.

---

##  Project Overview

- Scrapes daily Broadway show data using Apify.
- Stores data as **CSV**, **JSON**, and optionally in a **SQLite database**.
- Offers a **Streamlit dashboard** for exploring and analyzing scraped shows.
- Built with ethical scraping principles and scalable design.
- Supports Slack notifications, deduplication

---

##  Features

-  Extracts key show details:
  - Show Title
  - Show Date
  - Show Image Link
  - Theatre Name / Venue
  - Performance Time
  - Show Type (e.g., Musical, Play)
  - Link to Full Show Details

-  Saves data to CSV, JSON, and SQLite database
-  Deduplicates and logs each scraping session with a timestamp
-  Scheduled to run every 24 hours with `schedule.py`
-  Slack notifications when new shows are detected
-  Visualized using a Streamlit dashboard (`main.py`)
-  Anti-scraping measures: request throttling, retry logic, and ethical scraping practices

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sallybakar/ticketmaster_broadway_scraper.git
cd ticketmaster_broadway_scraper

2. Install Required Packages

pip install -r requirements.txt

 -  Contents of requirements.txt:
requests,
schedule,
streamlit,
pandas,
sqlite3,
beautifulsoup4,

3. Configure Apify API Token:

Open main.py or broadway_scraper.py and update:

APIFY_TOKEN = "your_apify_api_token_here"

4. Run the Scraper Manually:

python broadway_scraper.py

This will generate the latest broadway_shows.csv and broadway_shows.json in the output/YYYY-MM-DD folder.

5. Automate Daily Scraping:

To run the scraper automatically every 24 hours:

python scheduler.py

    Uses the schedule library.

    Automatically stores scraped data into CSV/JSON and optionally into SQLite.

    Logs execution time in the console.

6. (Optional) Launch the Streamlit Dashboard:

streamlit run main.py

Explore the data visually via filters, tables, and show previews.

 Automation Details

     Runs once every 24 hours using the schedule library.

     Deduplication logic to avoid re-saving shows already scraped.

     Console logs include scrape timestamps for traceability.

 Ethical Scraping Practices

     Uses Apify’s public API, avoiding direct HTML scraping.

     Respects source website with polite user-agent and throttling.

     Limits each request to 50 shows per run.

     Runs once daily to reduce server load.

     Provides transparent data logging and deduplication.

 Project Structure

ticketmaster_broadway_scraper/
├── main.py               # Creates a Streamlit dashboard that displays Broadway show data from a SQLite database.
├── scheduler.py          # Scheduler for daily scraping
├── broadway_scraper.py   # Main scraper using Apify API (CSV + JSON output + SQLite DB storage + Slack notification)
├── load_to_db.py         # Load JSON data into SQLite
├── db_utils.py           # Database setup & insertion logic
├── requirements.txt      # Required Python packages
├── README.md             # Documentation (this file)
├── output/
│   └── YYYY-MM-DD/
│       └── broadway_shows_TIMESTAMP.csv/json
├── shows.db              # SQLite database (optional)

 Sample Output Format (CSV)
Show Title,Show Date,Show Image Link,Theatre Name/Venue,Performance,Show Type,Link to Full Show Details,Scraping Date
Ride and Dine with Us!,Apr 30,https://s1.ticketm.net/dam/c/03e/e15ef00f-2c87-4421-ae61-d740851a703e_105891_RECOMENDATION_16_9.jpg,"Hard Rock Cafe Miami, Miami, FL",Apr 30,Unspecified,https://www.ticketweb.com/event/ride-and-dine-with-us-hard-rock-cafe-tickets/13384408?REFERRAL_ID=tmfeed,2025-05-25

 Deliverables Summary
File	Description
main.py -:	Creates a Streamlit dashboard that displays Broadway show data from a SQLite database
scheduler.py -:	Automates the scraper daily
broadway_scraper.py-:	Main scraper using Apify API, saves CSV/JSON
load_to_db.py -:	Inserts shows into SQLite database
db_utils.py -:	Helper functions for DB table setup
streamlit (main.py) -:	Optional dashboard for data visualization
shows.db -:	SQLite database of scraped entries
broadway_shows.csv/json -:	Cleaned and exported Broadway show data
README.md -:	Full documentation and setup guide

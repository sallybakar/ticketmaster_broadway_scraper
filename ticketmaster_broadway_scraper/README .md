🎭 Ticketmaster Broadway Scraper
📄 Project Overview
This project extracts key Broadway show information from Ticketmaster using the Apify API. The data is collected daily and saved as a CSV file for easy analysis. Additionally, a Streamlit dashboard is provided as an optional bonus to visualize the scraped show data interactively.

📊 Scope of Scraping
The scraper gathers the following details for each Broadway show:

Show Title

Show Date

Show Image URL

Theatre Name / Venue

Performance Time

Show Type (e.g., Musical, Play)

Link to Full Show Details

⚙️ Setup Instructions
1. Clone the Repository
git clone https://github.com/sallybakar/ticketmaster_broadway_scraper.git
cd ticketmaster_broadway_scraper
2. Install Required Packages
pip install -r requirements.txt
3. Configure Apify API Token
Open main.py and update the following line with Apify API token:

APIFY_TOKEN = "apify_api_ysLCjO9YEAopns9IuQGAPns7rn8kyQ0KKqZi"

4. Run the Scraper Manually -:
python main.py -
This will generate broadway_shows.csv containing the latest Broadway show data.

5. Automate Daily Scraping -:
python scheduler.py -
This script schedules the scraper to run automatically once every 24 hours.

6. (Optional) Launch the Streamlit Dashboard
To explore the data interactively via a web dashboard -:
streamlit run streamlit_app.py


📅 Automation Details
Scheduling implemented with the Python schedule library

Runs the scraper once daily

Logs each scraping timestamp in the console for monitoring

⚖️ Ethical Scraping Practices
Utilizes Apify’s official public API, avoiding direct raw HTML scraping

Limits data to 50 items per run to minimize load on the source

Sets a polite User-Agent through Apify API requests

Runs only once per day to avoid overloading Ticketmaster servers

📁 Project Deliverables
main.py –: Main scraper script using Apify API and saves to CSV and JSON

db_utils.py –: SQLite helper functions for table creation and data insertion

broadway_scraper.py –: Loads scraped data from JSON and inserts it into the database

load_to_db.py –: Reads parsed JSON and loads valid entries into a SQLite database

scheduler.py –: Automates the scraper to run daily

streamlit_app.py –: Optional Streamlit dashboard to visualize Broadway shows

requirements.txt –: All Python dependencies

README.md – Setup instructions, documentation, and usage guide

broadway_shows.csv –: Latest scraped and cleaned data

shows.db –: SQLite database storing scraped show data

📈 Sample Output Format (CSV)
Title	Date	Time	Venue	Image URL	Type	Details Link	Scraped At
Hamilton	2025-05-22	19:00	Richard Rodgers Theatre	https://image.url/hamilton	Musical	https://ticket.link/hamilton	2025-05-22 10:00:00
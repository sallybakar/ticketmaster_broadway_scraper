import streamlit as st
import sqlite3
import pandas as pd
import os

DB_NAME = "broadway_shows.db"

def load_data():
    if not os.path.exists(DB_NAME):
        st.warning("Database not found.")
        return pd.DataFrame()
    
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM shows ORDER BY inserted_at DESC", conn)
    conn.close()
    return df

st.set_page_config(page_title="🎭 Broadway Shows Dashboard", layout="wide")

st.title("🎭 Broadway Shows Scraper Dashboard")

df = load_data()

if df.empty:
    st.info("No show data available yet. Please run the scraper script first.")
else:
    st.success(f"Loaded {len(df)} shows from the database.")
    
    # Optional Filters
    with st.expander("🔍 Filter options"):
        title_filter = st.multiselect("Filter by Show Title:", sorted(df["show_title"].unique()))
        venue_filter = st.multiselect("Filter by Venue:", sorted(df["theatre_name"].unique()))
        
        if title_filter:
            df = df[df["show_title"].isin(title_filter)]
        if venue_filter:
            df = df[df["theatre_name"].isin(venue_filter)]

    st.dataframe(df, use_container_width=True)
import streamlit as st
import pandas as pd

def load_data(csv_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Remove rows where Show Date is 'TBA' (case insensitive)
    df = df[df["Show Date"].str.upper() != "TBA"]
    
    # Optional: Reset index for neatness
    df = df.reset_index(drop=True)
    
    return df

def main():
    st.title("Broadway Shows Listing")

    csv_file = "broadway_shows.csv"  # Change to your actual filename if different
    
    try:
        df = load_data(csv_file)
        
        st.write(f"Total shows displayed: {len(df)}")
        
        # Show the dataframe as a table
        st.dataframe(df)
        
        # Optional: Show images and links in a nicer format
        for idx, row in df.iterrows():
            st.markdown(f"### {row['Show Title']}")
            st.markdown(f"**Date:** {row['Show Date']}")
            st.markdown(f"**Theatre/Venue:** {row['Theatre Name/Venue']}")
            st.markdown(f"**Performance Time:** {row['Performance']}")
            st.markdown(f"**Show Type:** {row['Show Type']}")
            st.image(row['Show Image Link'], width=300)
            st.markdown(f"[More Details]({row['Link to Full Show Details']})")
            st.markdown("---")
        
    except FileNotFoundError:
        st.error(f"File {csv_file} not found. Please make sure the file exists in this directory.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
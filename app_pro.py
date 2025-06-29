import streamlit as st
import pandas as pd
import feedparser
import os

# Function to fetch latest papers from ArXiv
def get_latest_papers(topic="remote sensing"):
    base_url = "http://export.arxiv.org/api/query?"
    query = f"search_query=all:{topic}&start=0&max_results=5&sortBy=lastUpdatedDate&sortOrder=descending"
    feed = feedparser.parse(base_url + query)
    papers = [{"title": entry.title, "link": entry.link} for entry in feed.entries]
    return papers

# Streamlit App
st.title("🛰️ Remote Sensing App (Pro Edition)")

st.header("🔍 Real-Time Research Papers (via arXiv API)")
topic = st.text_input("Enter a research topic (e.g., hyperspectral, LiDAR, SAR)", "remote sensing")
if topic:
    results = get_latest_papers(topic)
    for i, paper in enumerate(results, 1):
        st.markdown(f"**{i}. {paper['title']}**  \n🔗 [View Paper]({paper['link']})")

st.header("📥 Hyperspectral Metadata")
meta_path = "hyperspectral_metadata/aviris_metadata.csv"
if os.path.exists(meta_path):
    df = pd.read_csv(meta_path)
    st.dataframe(df.head())
else:
    st.warning("Metadata file not found.")

import streamlit as st
import pandas as pd
import feedparser
import urllib.parse
import requests

# ========== Functions ==========

def get_latest_papers(topic="remote sensing"):
    base_url = "http://export.arxiv.org/api/query?"
    safe_topic = urllib.parse.quote(topic.strip())
    query = f"search_query=all:{safe_topic}&start=0&max_results=5&sortBy=lastUpdatedDate&sortOrder=descending"
    feed = feedparser.parse(base_url + query)
    papers = [{"title": entry.title, "link": entry.link} for entry in feed.entries]
    return papers

def fetch_nasa_datasets(keyword="hyperspectral"):
    url = "https://cmr.earthdata.nasa.gov/search/collections.json"
    params = {"keyword": keyword, "page_size": 5}
    r = requests.get(url, params=params)
    results = r.json().get("feed", {}).get("entry", [])
    return [
        {
            "title": item["short_name"],
            "summary": item.get("summary", "No description."),
            "url": item.get("links", [{}])[0].get("href", "")
        }
        for item in results
    ]

def fetch_opentopo_datasets():
    url = "https://portal.opentopography.org/API/globaldem?demtype=SRTMGL1&south=36&north=36.5&west=-122.5&east=-122&outputFormat=GTiff"
    return url

# ========== Streamlit UI ==========

st.title("🛰️ Remote Sensing App v1.0")

data_source = st.sidebar.selectbox("Choose data source", ["arXiv", "NASA CMR", "OpenTopography"])

if data_source == "arXiv":
    st.header("🔍 Real-Time Research Papers (via arXiv API)")
    topic = st.text_input("Enter a research topic (e.g., hyperspectral, LiDAR, SAR)", "remote sensing")
    if topic:
        results = get_latest_papers(topic)
        for i, paper in enumerate(results, 1):
            st.markdown(f"**{i}. {paper['title']}**  
🔗 [View Paper]({paper['link']})")

elif data_source == "NASA CMR":
    st.header("🌐 NASA Earthdata Search")
    keyword = st.text_input("Enter NASA dataset keyword", "AVIRIS")
    if st.button("Search NASA Datasets"):
        nasa_data = fetch_nasa_datasets(keyword)
        for d in nasa_data:
            st.write(f"### {d['title']}")
            st.write(d["summary"])
            st.markdown(f"[Dataset Link]({d['url']})")

elif data_source == "OpenTopography":
    st.header("🏔️ OpenTopography Global DEM (SRTMGL1)")
    download_url = fetch_opentopo_datasets()
    st.markdown(f"[Download GeoTIFF DEM (Sample)]({download_url})")

# Metadata Viewer
st.sidebar.markdown("---")
st.sidebar.markdown("📂 View Local Metadata")
if st.sidebar.checkbox("Show AVIRIS Metadata"):
    try:
        df = pd.read_csv("hyperspectral_metadata/aviris_metadata.csv")
        st.subheader("📋 AVIRIS Metadata")
        st.dataframe(df.head())
    except Exception as e:
        st.warning(f"Metadata could not be loaded: {e}")

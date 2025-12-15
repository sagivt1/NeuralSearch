# src/ui.py
import streamlit as st
import requests
import os

# The URL of your backend API (Docker service name 'web' or localhost)
# If running outside docker, use localhost. If inside docker, use the service name.
API_URL = os.getenv("API_URL", "http://localhost:8000")


st.set_page_config(page_title="NeuralSearch", layout="wide")

st.title("NeuralSearch Engine")
st.caption("Powered by FastAPI, pgvector, and Docker")

# --- Sidebar: Upload Section ---
with st.sidebar:
    st.header("1. Ingest Documents")
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])
    
    if uploaded_file and st.button("Ingest File"):
        with st.spinner("Processing and embedding..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            try:
                # Adjust the endpoint '/ingest' to match your actual API route
                response = requests.post(f"{API_URL}/ingest", files=files)
                if response.status_code == 200:
                    st.success("File ingested successfully!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")

# --- Main Area: Search Section ---
st.header("2. Search Your Knowledge Base")
query = st.text_input("Enter your search query...", placeholder="e.g., How does the transformer architecture work?")

if query:
    with st.spinner("Searching vector database..."):
        try:
            # Adjust endpoint '/search' to match your actual API route
            payload = {"query": query, "k": 3} # k = number of results
            response = requests.post(f"{API_URL}/search", json=payload)
            
            if response.status_code == 200:
                results = response.json()
                
                if not results:
                    st.warning("No results found. Try ingesting some documents first!")
                
                for idx, result in enumerate(results):
                    with st.expander(f"Result {idx + 1} (Score: {result.get('score', 0):.4f})", expanded=True):
                        st.markdown(result.get('content', 'No content'))
                        st.caption(f"Source: {result.get('metadata', {}).get('filename', 'Unknown')}")
            else:
                st.error(f"Search failed: {response.text}")
                
        except Exception as e:
            st.error(f"Connection error: {e}")
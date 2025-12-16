# A simple Streamlit web interface for the NeuralSearch API.
# Allows users to upload documents and perform semantic search.
import streamlit as st
import requests
import os

# The URL of the backend API.
# Defaults to localhost for local development.
# In a Docker environment, this would be the service name (e.g., http://web:8000).
API_URL = os.getenv("API_URL", "http://localhost:8000")


st.set_page_config(page_title="NeuralSearch", layout="wide")

st.title("NeuralSearch Engine")
st.caption("Powered by FastAPI, pgvector, and Streamlit")

# --- Sidebar: Document Upload ---
with st.sidebar:
    st.header("1. Upload Documents")
    # The backend currently only supports UTF-8 encoded text files.
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
    
    if uploaded_file and st.button("Ingest File"):
        with st.spinner("Processing and embedding..."):
            # Prepare the file for multipart/form-data upload.
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            try:
                # The backend endpoint for file ingestion.
                response = requests.post(f"{API_URL}/upload", files=files)
                if response.status_code == 200:
                    st.success("File ingested successfully!")
                else:
                    st.error(f"Error: {response.text}")
            except requests.exceptions.ConnectionError as e:
                st.error(f"Connection to API failed: {e}. Is the backend running?")

# --- Main Area: Search ---
st.header("2. Search Documents")
query = st.text_input("Enter your search query...", placeholder="e.g., How does the transformer architecture work?")

if query:
    with st.spinner("Searching vector database..."):
        try:
            # The backend search endpoint expects the query as a URL parameter.
            # The number of results is hardcoded to 5 in the backend.
            response = requests.post(f"{API_URL}/search?query={query}")
            
            if response.status_code == 200:
                results = response.json()
                
                if not results:
                    st.warning("No results found. Try uploading some documents first!")
                
                # The API does not yet return a similarity score.
                for idx, result in enumerate(results):
                    with st.expander(f"Result {idx + 1}", expanded=True):
                        st.markdown(result.get('content', 'No content available.'))
                        st.caption(f"Source: {result.get('filename', 'Unknown')}")
            else:
                st.error(f"Search failed: {response.text}")
                
        except requests.exceptions.ConnectionError as e:
            st.error(f"Connection to API failed: {e}. Is the backend running?")
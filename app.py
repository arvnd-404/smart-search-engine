import streamlit as st  # builds the visual interface
import requests  # to call our FastAPI backend

API_URL = "http://localhost:8000"  # address of our FastAPI server

# ─── Page config ───
st.set_page_config(
    page_title="Smart Search Engine",  # browser tab title
    page_icon="🔍",                    # browser tab icon
    layout="centered"                  # center the content
)

# ─── Header ───
st.title("🔍 Smart Search Engine")  # big title at the top
st.write("Search Wikipedia semantically — finds meaning, not just keywords.")  # subtitle

# ─── Search bar ───
query = st.text_input("Enter your search query")  # text box for user to type

# ─── Results ───
if query:  # only search if user has typed something
    response = requests.get(f"{API_URL}/search", params={"query": query})  # call FastAPI
    data = response.json()  # parse the JSON response

    st.write(f"### Results for: *{query}*")  # show the query back to user

    for result in data["results"]:  # loop through each result
        with st.expander(f"📄 {result['title']} — Score: {result['score']:.4f}"):  # collapsible card
            st.write(result["text"])  # show page text inside the card
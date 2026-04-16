from fastapi import FastAPI
from search.database import search_db, load_embeddings_to_db
from embedder.embed import embed_pages, save_embeddings
from crawler.fetch import fetch_page, get_wikipedia_titles
import os
import json

app = FastAPI()

def setup():  # runs once when server starts
    if not os.path.exists("data/embeddings.json"):  # only crawl if no data exists
        print("No data found. Starting crawl...")
        
        titles = get_wikipedia_titles("Artificial_intelligence", limit=20)  # fetch 20 pages
        os.makedirs("data/pages", exist_ok=True)

        for title in titles:
            filepath = f"data/pages/{title.replace(' ', '_').replace('/', '_')}.json"
            if not os.path.exists(filepath):
                page = fetch_page(title)
                if page["text"]:
                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(page, f, ensure_ascii=False, indent=2)

        embeddings = embed_pages("data/pages")
        save_embeddings(embeddings, "data/embeddings.json")
        load_embeddings_to_db("data/embeddings.json")
        print("Setup complete!")

setup()  # run setup when API starts

@app.get("/")
def root():
    return {"message": "Smart Search Engine is running!"}

@app.get("/search")
def search(query: str):
    results = search_db(query)
    return {"query": query, "results": results}
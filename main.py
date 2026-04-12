import json  # to save results
import os  # to work with folders
from crawler.fetch import fetch_page, get_wikipedia_titles  # our crawler functions
from embedder.embed import embed_pages, save_embeddings  # our embedder functions
from search.database import load_embeddings_to_db, search_db  # our ChromaDB functions

# ─── Step 1: Get 100 Wikipedia page titles ───
print("Fetching list of Wikipedia pages...")
titles = get_wikipedia_titles("Artificial_intelligence", limit=100)  # get 100 AI related pages
print(f"Found {len(titles)} pages to crawl\n")

# ─── Step 2: Crawl each page ───
os.makedirs("data/pages", exist_ok=True)  # create folder if it doesn't exist

for title in titles:
    filepath = f"data/pages/{title.replace(' ', '_').replace('/', '_')}.json"  # safe filename

    if os.path.exists(filepath):  # skip if already crawled
        print(f"Skipping (already saved): {title}")
        continue

    print(f"Fetching: {title}")
    page = fetch_page(title)  # fetch the page from Wikipedia

    if not page["text"]:  # skip empty pages
        print(f"Skipping (empty): {title}")
        continue

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(page, f, ensure_ascii=False, indent=2)  # save page as JSON

    print(f"Saved: {title}")

# ─── Step 3: Embed all pages ───
print("\nStarting embedding...\n")
embeddings = embed_pages("data/pages")  # read all JSON files and convert to vectors
save_embeddings(embeddings, "data/embeddings.json")  # save all vectors to disk
print(f"Done! Created {len(embeddings)} embeddings")

# ─── Step 4: Load into ChromaDB ───
print("\nLoading into ChromaDB...\n")

# Clear old data first
from search.database import collection  # import the collection
collection.delete(where={"title": {"$ne": ""}})  # delete all old entries

load_embeddings_to_db("data/embeddings.json")  # load fresh data into ChromaDB

# ─── Step 5: Test Search ───
print("\n--- Search Test ---\n")
query = "how do computers learn?"  # test query
results = search_db(query)  # search ChromaDB

for result in results:
    print(f"Title: {result['title']}")
    print(f"Score: {result['score']:.4f}")
    print("---")
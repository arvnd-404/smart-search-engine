
```markdown
# Smart Search Engine — Full Project Documentation

## What is this project?

A private semantic search engine built in Python. Unlike standard search engines that look for exact words, this engine understands the **meaning** behind a query. For example, searching "how do computers learn?" will return pages about "Machine learning" even though none of those words appear in the query.

---

## How it works — The Big Picture

```
Step 1: Crawler fetches 100 Wikipedia pages and saves them as JSON files
Step 2: Embedder reads each page and converts the text into 384 numbers (a vector)
Step 3: Vectors are stored in ChromaDB (a vector database)
Step 4: User types a query → query is converted to a vector → ChromaDB finds the closest matching vectors → results are returned
Step 5: FastAPI serves the search as a REST API
Step 6: Streamlit displays the results visually
```

---

## Project Structure

```
smart-search/
├── crawler/
│   ├── __init__.py
│   └── fetch.py              # fetches Wikipedia pages using the official API
├── embedder/
│   ├── __init__.py
│   └── embed.py              # converts text into vectors using sentence-transformers
├── search/
│   ├── __init__.py
│   ├── query.py              # original search logic using cosine similarity
│   └── database.py           # ChromaDB vector database integration
├── data/
│   ├── pages/                # saved Wikipedia JSON files
│   ├── embeddings.json       # saved vectors for all pages
│   └── chromadb/             # ChromaDB database files
├── api.py                    # FastAPI REST API backend
├── app.py                    # Streamlit visual search UI
├── main.py                   # ties everything together
└── requirements.txt          # list of all dependencies
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Main programming language |
| requests | Fetches Wikipedia pages from the API |
| BeautifulSoup | Cleans and parses HTML |
| sentence-transformers | Converts text into 384-dimensional vectors |
| ChromaDB | Stores and searches vectors instantly |
| FastAPI | REST API backend |
| uvicorn | Server that runs FastAPI |
| Streamlit | Visual search interface |

---

## Layer 1 — The Crawler (`crawler/fetch.py`)

### What it does
Fetches Wikipedia pages using the official Wikipedia API and saves them as JSON files on disk.

### Key functions

**`fetch_page(title)`**
- Takes a Wikipedia page title as input
- Sends a request to `https://en.wikipedia.org/w/api.php`
- Returns the page title and full plain text content
- Saves the result as a JSON file in `data/pages/`

**`get_wikipedia_titles(category, limit)`**
- Takes a Wikipedia category name and a limit
- Returns a list of page titles from that category
- Used to automatically generate the list of 100 pages to crawl

### Why we used the Wikipedia API instead of scraping
Scraping HTML directly gets blocked by Wikipedia. The official API always returns clean plain text without any HTML tags, ads, or navigation elements.

### Output
Each page is saved as a JSON file like this:
```json
{
  "title": "Machine learning",
  "text": "Machine learning is a field of study..."
}
```

---

## Layer 2 — The Embedder (`embedder/embed.py`)

### What it does
Reads all saved JSON files and converts the text of each page into a vector — a list of 384 numbers that mathematically represent the meaning of the text.

### What is a vector?
A vector is just a list of numbers. The AI model reads the text and produces 384 numbers that capture its meaning. Pages about similar topics will have similar numbers. This is what makes semantic search possible.

### Key functions

**`embed_pages(pages_folder)`**
- Loops through all JSON files in `data/pages/`
- For each page, takes the first 1000 characters of text
- Passes the text through the AI model `all-MiniLM-L6-v2`
- Returns a list of dictionaries containing title, text and vector

**`save_embeddings(embeddings, output_path)`**
- Saves all embeddings to a single JSON file at `data/embeddings.json`

### The AI model
We use `all-MiniLM-L6-v2` from the `sentence-transformers` library. It is a small but powerful pre-trained model that converts any text into a 384-dimensional vector. It was trained on millions of sentences so it already understands language deeply.

### Output
```json
{
  "title": "Machine learning",
  "text": "Machine learning is a field of study...",
  "vector": [0.231, -0.512, 0.814, ...]
}
```

---

## Layer 3 — The Search Engine

### Part 1 — Basic Search (`search/query.py`)

The first version of search. Loads all vectors from `embeddings.json`, converts the query to a vector, loops through every page and measures cosine similarity, then sorts and returns the top results.

**Cosine similarity** measures the angle between two vectors. A score of 1.0 means identical meaning, 0.0 means completely unrelated.

This approach works but gets slow with many pages because it checks every single page one by one.

### Part 2 — ChromaDB (`search/database.py`)

Replaces the slow loop with a proper vector database. ChromaDB stores all vectors and finds the closest match instantly without looping.

**Key functions**

**`load_embeddings_to_db(embeddings_path)`**
- Reads `embeddings.json`
- Loads all vectors into ChromaDB with their title and text
- Each page is stored with a unique ID, its vector, its text and its title

**`search_db(query, top_k)`**
- Converts the query to a vector
- Asks ChromaDB to find the top k closest vectors
- Returns results with title, text and distance score

**Note on scores:** ChromaDB returns distance instead of similarity. Lower score = better match. This is the opposite of cosine similarity.

### Part 3 — FastAPI (`api.py`)

Turns the search engine into a REST API that any app can call.

**Endpoints**

| Method | URL | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/search?query=...` | Returns top 3 matching pages |

**Example request:**
```
GET http://localhost:8000/search?query=machine+learning
```

**Example response:**
```json
{
  "query": "machine learning",
  "results": [
    {
      "title": "Machine learning",
      "text": "Machine learning is a field of study...",
      "score": 0.8932
    }
  ]
}
```

### Part 4 — Streamlit UI (`app.py`)

A visual search interface built entirely in Python. Calls the FastAPI backend and displays results as collapsible cards showing the title, score and page text.

---

## How to run the project

### Step 1 — Activate virtual environment
```bash
.\.venv\Scripts\activate
cd smart-search
```

### Step 2 — Crawl, embed and load data
```bash
python main.py
```

### Step 3 — Start FastAPI server (Terminal 1)
```bash
uvicorn api:app --reload
```

### Step 4 — Start Streamlit UI (Terminal 2)
```bash
streamlit run app.py
```

### Step 5 — Open in browser
- Search UI: `http://localhost:8501`
- API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

---

## What makes this different from normal search

| Normal search | This search engine |
|---|---|
| Looks for exact words | Understands meaning |
| "felines" won't find "cats" | "felines" will find "cats" |
| Simple string matching | Vector mathematics |
| No understanding of context | Understands context |

---

## Possible improvements

- Scale to 1000+ pages
- Add a React frontend instead of Streamlit
- Deploy to a cloud server so others can use it
- Add support for searching PDFs and documents
- Add a re-ranking step to improve result quality
```


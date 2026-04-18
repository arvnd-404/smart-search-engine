
```markdown
# 🔍 Smart Search Engine

A semantic search engine built in Python that understands the **meaning** of your query — not just exact words.

> Searching "how do computers learn?" returns "Machine learning" even though those words never appear in the query.

---

## Tech Stack
- **sentence-transformers** — converts text to vectors
- **ChromaDB** — vector database
- **FastAPI** — REST API backend
- **Streamlit** — search UI

---

## Setup

**1. Clone the repo and activate virtual environment**
```bash
.\.venv\Scripts\activate
cd smart-search
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Crawl, embed and load data**
```bash
python main.py
```

---

## Run

**Terminal 1 — API**
```bash
uvicorn api:app --reload
```

**Terminal 2 — UI**
```bash
streamlit run app.py
```

---

## Usage
- Open `http://localhost:8501` in your browser
- Type any query in the search box
- Get semantically matched Wikipedia pages instantly

---

## API
| Endpoint | Description |
|---|---|
| `GET /` | Check if API is running |
| `GET /search?query=...` | Search and get results |

---

## Project Structure
```
smart-search/
├── crawler/              → fetches Wikipedia pages
├── embedder/             → converts text to vectors
├── search/               → ChromaDB search logic
├── data/                 → embeddings and crawled pages
├── api.py                → FastAPI backend
├── app.py                → Streamlit UI
├── main.py               → runs everything
├── Dockerfile            → cloud deployment config
├── requirements.txt      → all dependencies
├── README.md             → project overview
└── DOCUMENTATION.md      → detailed documentation
```
```


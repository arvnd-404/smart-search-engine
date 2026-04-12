from fastapi import FastAPI  # the framework that builds our API
from search.database import search_db  # our ChromaDB search function

app = FastAPI()  # create the API app

# ─── Root endpoint ───
@app.get("/")  # when someone visits http://localhost:8000/
def root():
    return {"message": "Smart Search Engine is running!"}  # just a welcome message

# ─── Search endpoint ───
@app.get("/search")  # when someone visits http://localhost:8000/search?query=...
def search(query: str):  # query comes from the URL automatically
    results = search_db(query)  # search ChromaDB with the query
    return {"query": query, "results": results}  # return results as JSON
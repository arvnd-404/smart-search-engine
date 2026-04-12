from sentence_transformers import SentenceTransformer  # same AI model we used for embedding
from sklearn.metrics.pairwise import cosine_similarity  # measures how close two vectors are
import json  # to read our saved embeddings
import numpy as np  # to work with numbers and vectors

model = SentenceTransformer("all-MiniLM-L6-v2")  # load the same AI model (must be same as embedder)

def search(query, embeddings_path, top_k=3):  # takes a search query and returns top matching pages
    with open(embeddings_path, "r", encoding="utf-8") as f:
        embeddings = json.load(f)  # load all our saved vectors from disk

    query_vector = model.encode(query)  # convert the search query into 384 numbers

    results = []  # empty list to store results

    for page in embeddings:  # loop through every saved page
        page_vector = np.array(page["vector"])  # convert the saved list back to a numpy array
        score = cosine_similarity([query_vector], [page_vector])[0][0]  # measure closeness (0 to 1)
        results.append({
            "title": page["title"],  # store the page title
            "text": page["text"],    # store the page text
            "score": float(score)    # store the similarity score
        })

    results.sort(key=lambda x: x["score"], reverse=True)  # sort by score, highest first
    return results[:top_k]  # return only the top matches
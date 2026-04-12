import chromadb  # the vector database
import json  # to read our saved embeddings
from sentence_transformers import SentenceTransformer  # to convert query to vector

model = SentenceTransformer("all-MiniLM-L6-v2")  # same AI model as before

# Create a local ChromaDB client — saves data in a folder called "data/chromadb"
client = chromadb.PersistentClient(path="data/chromadb")

# Create a collection — think of this like a table in a normal database
collection = client.get_or_create_collection(name="wikipedia_pages")

def load_embeddings_to_db(embeddings_path):  # loads our saved embeddings into ChromaDB
    with open(embeddings_path, "r", encoding="utf-8") as f:
        embeddings = json.load(f)  # read the saved embeddings file

    for i, page in enumerate(embeddings):  # loop through each page
        collection.add(
            ids=[str(i)],                  # unique ID for each page
            embeddings=[page["vector"]],   # the 384 numbers
            documents=[page["text"]],      # the actual text
            metadatas=[{"title": page["title"]}]  # extra info like title
        )
    print(f"Loaded {len(embeddings)} pages into ChromaDB")

def search_db(query, top_k=3):  # searches ChromaDB with a query
    query_vector = model.encode(query).tolist()  # convert query to vector

    results = collection.query(
        query_embeddings=[query_vector],  # search using the query vector
        n_results=top_k                   # return top k results
    )

    matches = []  # empty list to store results
    for i in range(len(results["ids"][0])):  # loop through each result
        matches.append({
            "title": results["metadatas"][0][i]["title"],  # get the title
            "text": results["documents"][0][i],            # get the text
            "score": results["distances"][0][i]            # get the similarity score
        })

    return matches  # return all matches
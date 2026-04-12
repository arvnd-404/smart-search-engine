from sentence_transformers import SentenceTransformer  # the AI model that converts text to vectors
import json  # to read our saved JSON files
import os  # to work with files and folders

# Load the AI model (this runs once and stays in memory)
# "all-MiniLM-L6-v2" is a small but powerful model — turns text into 384 numbers
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_pages(pages_folder):  # takes the folder path where our JSON files are saved
    embeddings = []  # empty list to store our results

    for filename in os.listdir(pages_folder):  # loop through every file in the folder
        if filename.endswith(".json"):  # only process JSON files
            filepath = os.path.join(pages_folder, filename)  # build the full file path

            with open(filepath, "r", encoding="utf-8") as f:  # open the file for reading
                page = json.load(f)  # load the JSON content into a Python dictionary

            title = page["title"]  # get the page title
            text = page["text"][:1000]  # take first 1000 characters (enough for a good vector)

            print(f"Embedding: {title}")  # show progress
            vector = model.encode(text)  # convert text into a list of 384 numbers

            embeddings.append({
                "title": title,       # store the title
                "text": text,         # store the text
                "vector": vector.tolist()  # store the vector (convert from numpy to normal list)
            })

    return embeddings  # return all the embeddings
def save_embeddings(embeddings, output_path):  # saves all vectors to a single JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(embeddings, f, ensure_ascii=False, indent=2)  # write everything to file
    print(f"Saved {len(embeddings)} embeddings to {output_path}")  # confirm how many were saved
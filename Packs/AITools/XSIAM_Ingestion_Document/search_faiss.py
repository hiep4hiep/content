from sentence_transformers import SentenceTransformer
import faiss
import torch
import json


def search_sentence_in_faiss(sentence, faiss_index_path="readme_faiss.index", metadata_path="readme_corpus.json"):
    """
    Searches for the most similar sentence in a FAISS index given an input sentence.
    Args:
        sentence (str): The input sentence to search for in the FAISS index.
        faiss_index_path (str, optional): Path to the FAISS index file. Defaults to "readme_faiss.index".
    Returns:
        str: The most similar sentence (or data) retrieved from the corpus.
    Raises:
        FileNotFoundError: If the FAISS index file or the corpus file does not exist.
        Exception: For errors during model loading, encoding, or FAISS search.
    """

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
    index = faiss.read_index(faiss_index_path)
    embedding = model.encode(sentence, convert_to_tensor=True, device=device)
    embedding_np = embedding.cpu().unsqueeze(0).numpy()
    D, I = index.search(embedding_np, k=1)

    with open(metadata_path, 'r', encoding='utf-8') as infile:
        target_idx = I[0][0]
        corpus_data = json.load(infile)
        return corpus_data[target_idx].get('data', 'No data found for this index')

if __name__ == "__main__":
    
    print(search_sentence_in_faiss("Okta cloud identity management platform"))
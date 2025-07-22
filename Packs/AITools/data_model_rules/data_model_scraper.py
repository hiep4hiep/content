import os
from sentence_transformers import SentenceTransformer
import faiss
import torch
import json
import pandas as pd
import numpy as np
import pickle


def embed_and_store_in_faiss(sample_path):
    df = pd.read_csv(sample_path)
    # Load embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')  # or use OpenAI embeddings for production
    # Generate embeddings
    embeddings = model.encode(df['raw_log'].tolist(), convert_to_numpy=True)
    # Build FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save index and mapping
    faiss.write_index(index, "rawlog_faiss.index")
    with open("rawlog_data_mapping.pkl", "wb") as f:
        pickle.dump(df['data_model'].tolist(), f)
    with open("rawlog_data_mapping_raw_log.pkl", "wb") as f:
        pickle.dump(df['raw_log'].tolist(), f)


if __name__ == "__main__":
    embed_and_store_in_faiss("sample_raw_log_to_dm.csv")
    
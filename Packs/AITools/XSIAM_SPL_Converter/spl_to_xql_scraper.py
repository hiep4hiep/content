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
    #invalid_rows = df[~df['SPL_Query'].apply(lambda x: isinstance(x, str))]
    #return invalid_rows
    # Load embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')  # or use OpenAI embeddings for production
    # Generate embeddings
    embeddings = model.encode(df['SPL_Query'].dropna().astype(str).tolist(), convert_to_numpy=True)
    # Build FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save index and mapping
    faiss.write_index(index, "spl_faiss.index")
    with open("spl_data_mapping.pkl", "wb") as f:
        pickle.dump(df['SPL_Query'].tolist(), f)
    with open("xql_data_mapping.pkl", "wb") as f:
        pickle.dump(df['XQL_Query'].tolist(), f)
    with open("search_name_data_mapping.pkl", "wb") as f:
        pickle.dump(df['Search_Name'].tolist(), f)
    


if __name__ == "__main__":
    embed_and_store_in_faiss("SPL_to_XQL.csv")
    
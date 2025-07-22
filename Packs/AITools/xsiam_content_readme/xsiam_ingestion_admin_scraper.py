import os
from sentence_transformers import SentenceTransformer
import faiss
import torch
import json
import re


def write_readmes_to_file(readme_paths, output_file="ingestion_method_corpus.json"):
    """
    Reads the content of a PDF file named 'ingestion_method.pdf', splits it into chunks based on a specific pattern,
    and writes the resulting chunks with their indices to a JSON file.
    Args:
        readme_paths (list of str): Unused parameter, included for compatibility.
        output_file (str, optional): Path to the output JSON file. Defaults to "readmes_corpus.json".
    Returns:
        None
    Side Effects:
        Creates or overwrites the specified output JSON file with extracted PDF content.
    Example:
        write_readmes_to_file([], output_file='output.json')
    """
    with open(readme_paths, "r") as infile:
        text = infile.read()

    split_pattern = r"### Ingest .+"
    chunks = re.split(split_pattern, text)
    metadata = []
    for idx, chunk in enumerate(chunks):
        if chunk.strip():
            metadata.append({"index": idx, "data": chunk.strip()})

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(metadata, outfile, indent=2)
    print(f"Readme files written to {output_file}")
    return(chunks)


def embed_and_store_in_faiss(readme_paths):
    """
    Embeds the contents of README files using a pre-trained SentenceTransformer model and stores the resulting embeddings in a FAISS index.
    Args:
        readme_paths (list of str): List of file paths to README files to be embedded.
    Returns:
        faiss.IndexFlatL2: The FAISS index containing the embeddings of the README files.
    Side Effects:
        Writes the FAISS index to disk as "readme_faiss.index".
    Notes:
        - Uses GPU if available, otherwise falls back to CPU.
        - Each README file is read in UTF-8 encoding.
        - Requires the 'torch', 'faiss', and 'sentence_transformers' libraries.
    """

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
    embeddings = []
    print(f"Writing file {readme_paths}\n to faiss index")
    data = write_readmes_to_file(readme_paths)
    for item in data:
        embedding = model.encode(item, convert_to_tensor=True, device=device)
        embeddings.append(embedding)

    embeddings = torch.stack(embeddings).to(device)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings.cpu().numpy())
    faiss.write_index(index, "ingestion_admin_guide_faiss.index")
    return index


if __name__ == "__main__":
    embed_and_store_in_faiss("ingestion_doc.md")
    
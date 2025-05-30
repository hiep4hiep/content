import anthropic
from sentence_transformers import SentenceTransformer
import faiss
import torch
import json


def search_sentence_in_faiss(sentence, faiss_index_path="readme_faiss.index", metadata_path="readmes_corpus.json"):
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
    
    ### Get item from corpus
    with open(metadata_path, 'r', encoding='utf-8') as infile:
        corpus = json.load(infile)
        data = corpus[I[0][0]]['data']
    return data


def prompt_claude_with_rag(question):
    """
    Prompts Claude API with RAG (Retrieval-Augmented Generation).
    Claude acts as a solution architect for designing data ingestion into SIEM.

    Args:
        question (str): The user's question.
        context_docs (list of str): List of relevant context documents.

    Returns:
        str: Claude's response.
    """
    # Build the context for RAG
    context = (
        """
        You are an experienced Solution Architect with deep knowledge in security information and event management (SIEM), log pipelines, cloud architecture, and threat detection.

        Your task is to design a robust and scalable SIEM data ingestion solution for a security product. You don't need to provide Broker VM configuration, just provide the ingestion method design and data source configuration.

        The solution should address the following:

        1. **Data Sources**:
        - What telemetry or event types are available from Microsoft Defender?
        - How should they be collected?
        - How to configure the data source for the log ingestion?

        2. **Ingestion Pipeline**:
        - What are the recommended ingestion methods (e.g., API, connector, syslog (via Cortex Broker VM), Event Hub)?
        - How would you ensure reliability, scalability, and security?

        """
       
    )
    context += search_sentence_in_faiss(question, faiss_index_path="readme_faiss.index", metadata_path="readmes_corpus.json")

    content = f"Context:\n{context}\n\n"
    content += f"User question: {question}\n"

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        messages=[
            {"role": "user", "content": content.replace("\n", "<br>")},
        ]
    )
    return message.content[0].text

if __name__ == "__main__":
    print(prompt_claude_with_rag("Ingest Imperva WAF logs into XSIAM"))
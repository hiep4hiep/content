import anthropic
from sentence_transformers import SentenceTransformer
from search_faiss import search_sentence_in_faiss
from dotenv import load_dotenv

load_dotenv()  # Load from .env if exists


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
    with open("data_model_schema.txt", "r") as f:
        dm_schema = f.read()
    sample_rule, raw_log_samples = search_sentence_in_faiss(question)
    context = f"""
        You are a skilled SIEM engineer specializing in log onboarding and data modeling for XSIAM.

        Your task is to analyze the provided data model schema and raw log messages, then generate precise XSIAM data model mapping rules.

        Follow these steps:
        1. Review the data model schema and understand the required fields and their types.
        2. Examine the raw log messages and identify how each field maps to the XSIAM schema. Refer to the provided data model rule examples for guidance.
        3. Output the mapping rules in a clear, structured format suitable for implementation.

        Data model schema:
        {dm_schema}

        Sample raw log messages:
        {raw_log_samples}

        Sample data model rule:
        {sample_rule}
        """

    content = f"Context:\n{context}\n\n"
    content += f"Raw log: {question}\n"

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {"role": "user", "content": content},
        ]
    )
    return message.content[0].text

if __name__ == "__main__":
    # For testing purposes, can run this script directly
    print(prompt_claude_with_rag('CEF:0|Palo Alto Networks|PAN-OS|10.2|TRAFFIC|traffic-log|5|src=10.10.10.5 dst=192.168.1.25 spt=60415 dpt=443 proto=tcp act=allow app=web-browsing cs1Label=src_zone cs1=Trust cs2Label=dst_zone cs2=Untrust cn1Label=session_id cn1=304478'))
import anthropic
from search_faiss import search_sentence_in_faiss


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
    xsiam_guidance = search_sentence_in_faiss(question)
    # Build the context for RAG
    context = f"""
        You are an experienced Solution Architect with deep knowledge in security information and event management (SIEM), log pipelines, cloud architecture, and threat detection.

        Your task is to design a robust and scalable SIEM data ingestion solution for a security product. You don't need to provide Broker VM configuration, just provide the ingestion method design and data source configuration.
        Refer to the XSIAM guidance below for the design and configuration of the data ingestion method. If Broker VM is not mentioned, assume it is not required and the collection method might be API-based or S3, Event Hub or HTTP Event Collector and so on

        XSIAM Guidance:
        {xsiam_guidance}

        The solution should provide enough information for the data ingestion implementation, can have the following items:

        1. **Data Sources**:
        - What data sources are relevant for the security product?
        - What telemetry or event types are available?
        - How to configure the data source for the log ingestion?

        2. **Ingestion Pipeline**:
        - What are the recommended ingestion methods (e.g., API connector, syslog (via Cortex Broker VM), Event Hub)?
        - How would you ensure reliability, scalability, and security?
        - Network requirements for the ingestion method?
        - Credetials or authentication methods required for the data source?
        
        """
    

    content = f"Context:\n{context}\n\n"
    content += f"User question: {question}\n"

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": content},
        ]
    )
    return message.content[0].text

if __name__ == "__main__":
    # For testing purposes, can run this script directly
    print(prompt_claude_with_rag("Okta cloud identity management platform"))
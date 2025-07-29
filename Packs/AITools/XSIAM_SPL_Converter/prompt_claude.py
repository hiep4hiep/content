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
    with open("xql_stages.txt", "r") as f:
        xql_stages = f.read()
    with open("xql_functions.txt", "r") as f:
        xql_functions = f.read()

    faiss_results = search_sentence_in_faiss(question)
    example_text = ""
    for i, (spl, xql) in enumerate(faiss_results):
        example_text += f"""
        Example {i+1}:
        - SPL Query: {spl}
        - Equivalent XQL Query: {xql}

"""

    context = f"""
You are a skilled SIEM engineer specializing in writing searches in XQL in Cortex XSIAM.
Your task is to analyze the provided search query in Splunk SPL and convert it to Cortex XSIAM XQL.

Given the following example search queries in Splunk SPL and the corresponding converted XQL query, your task is to to the same for the required search query.
{example_text}

Refer to the list of XQL stages and functions and the field schema below to help you with the conversion:
- XQL Stages:
{xql_stages}

- XQL Functions:
{xql_functions}

- XQL Field Schema:
{dm_schema}

        """

    content = f"Context:\n{context}\n\n"
    content += f"Convert this query: {question}\n"
    
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
    print(prompt_claude_with_rag("""
'| tstats `security_content_summariesonly` count min(_time) as firstTime max(_time)
  as lastTime FROM datamodel=Endpoint.Registry WHERE (Registry.registry_path= "*SOFTWARE\\Microsoft\\Windows
  NT\\CurrentVersion\\Winlogon*" AND Registry.registry_value_name=AutoAdminLogon AND
  Registry.registry_value_data=1) by Registry.action Registry.dest Registry.process_guid
  Registry.process_id Registry.registry_hive Registry.registry_path Registry.registry_key_name
  Registry.registry_value_data Registry.registry_value_name Registry.registry_value_type
  Registry.status Registry.user Registry.vendor_product | `drop_dm_object_name(Registry)`
  | where isnotnull(registry_value_data) | `security_content_ctime(firstTime)` | `security_content_ctime(lastTime)`
  | `auto_admin_logon_registry_entry_filter`'
                                 """))
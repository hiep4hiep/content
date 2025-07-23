import os
from sentence_transformers import SentenceTransformer
import faiss
import torch
import json
import re



def write_ingestion_guide_to_file(readme_paths, output_file="readme_corpus.json", start_index=0, metadata=[]):
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
    for idx, chunk in enumerate(chunks):
        if chunk.strip():
            metadata.append({"index": start_index + idx + 1, "data": chunk.strip()})

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(metadata, outfile, indent=2)
    print(f"Readme files written to {output_file}")
    print(f"Total chunks written: {len(metadata)}")
    return(chunks)


def find_readme_files(main_folder):
    """
    Searches for README.md files within "Integrations" directories of content packs that contain a "ModelingRules" directory.
    Args:
        main_folder (str): The root directory to start searching for content packs.
    Returns:
        list: A list of file paths to README.md files found within "Integrations" directories of qualifying content packs.
    """

    xsiam_content_pack = []
    readme_paths= []
    for root, dirs, files in os.walk(main_folder):
        if "ModelingRules" in dirs:
            xsiam_content_pack.append(root)
    for path in xsiam_content_pack:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower() == "readme.md" and "Integrations" in root:
                    readme_paths.append(os.path.join(root, file))
    return readme_paths


def indexing_readme_files(readme_paths, output_file="readmes_corpus.json"):
    """
    Reads multiple README files, extracts content up to the "## Commands" section from each,
    and writes the extracted data along with their indices to a JSON file.
    Args:
        readme_paths (list of str): List of file paths to the README files to be processed.
        output_file (str, optional): Path to the output JSON file. Defaults to "readmes_corpus.json".
    Returns:
        None
    Side Effects:
        Creates or overwrites the specified output JSON file with the extracted README contents.
    Example:
        write_readmes_to_file(['README1.md', 'README2.md'], output_file='output.json')
    """

    metadata = []
    for idx, path in enumerate(readme_paths):
        print(f"Writing file {path} to metadata dictionary\n")
        with open(path, 'r', encoding='utf-8') as infile:
            content = infile.read()
            metadata.append({"index": idx, "data": content.split("## Commands")[0]})
    return metadata,idx


def embed_and_store_in_faiss(readme_paths,ingestion_guide_paths):
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
    print(f"Running on device: {device}")
    model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
    embeddings = []
    # Embed data from README.md files from marketplace content packs
    for path in readme_paths:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            embedding = model.encode(content, convert_to_tensor=True, device=device)
            embeddings.append(embedding)

    first_metadata, first_index = indexing_readme_files(readme_files)
     # Embed data from Ingestion method admin guide (exported version from website)
    ingestion_data = write_ingestion_guide_to_file(readme_paths=ingestion_guide_paths,output_file="readme_corpus.json", start_index=first_index, metadata=first_metadata) # Continue from previous index and metadata
    for item in ingestion_data:
        embedding = model.encode(item, convert_to_tensor=True, device=device)
        embeddings.append(embedding)

    embeddings = torch.stack(embeddings).to(device)
    index = faiss.IndexFlatL2(embeddings.shape[1])

    index.add(embeddings.cpu().numpy())
    faiss.write_index(index, "readme_faiss.index")
    return index



if __name__ == "__main__":
    main_folder = "/home/hiepn/content/Packs"
    readme_files = find_readme_files(main_folder)
    ingestion_guide_paths = "ingestion_doc.md"
    

    embed_and_store_in_faiss(readme_files,ingestion_guide_paths)
    
import os
from typing import List, Dict

import ollama
from loguru import logger
from dotenv import load_dotenv
from hashlib import sha256


def init_tokenizer():
    import nltk
    from nltk.tokenize import sent_tokenize
    try:
        sent_tokenize("Hello do I have punkt tokenizer?")
    except LookupError:
        nltk.download('punkt')


def init_ollama_backend(model_name: str = "nomic-embed-text"):
    # docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
    try:
        ollama.embeddings(model_name, prompt="Mic check")
        logger.info(f"Model {model_name} exists locally.")
    except ollama.ResponseError as e:
        if "not found" in e.error:
            logger.info("Model not found, pulling it now...")
            ollama.pull(model_name)
        else:
            raise e


def ollama_pull_model(ollama_host: str = "http://localhost:11434", model_name: str = 'llama3'):
    import requests
    url = f"{ollama_host}/api/pull"
    data = {"name": model_name}
    response = requests.post(url, json=data)
    logger.info(response.json())


def batch_write_chunk_to_db(collection, chunks: List[Dict[str, str]], embed_model="nomic-embed-text"):
    # Replace with a pydantic or dataclass later
    if not isinstance(chunks, dict):
        raise TypeError(f"Expect the input chunk to be of dictionary type, got {type(chunks)}.")
    for chunk in chunks:
        text = chunk['text']
        metadata = chunk['metadata']
        # If empty use sha256 on the text
        try:
            chunk_id = chunk['id']
        except KeyError:
            chunk_id = sha256(text.encode('utf-8')).hexdigest()
        embedding = ollama.embeddings(model=embed_model, prompt=text)['embedding']
        collection.add(embeddings=[embedding], documents=[text], metadatas=[metadata], ids=[chunk_id])


if __name__ == "__main__":
    from parsers import pdf
    from start import get_collection, start_chroma_db_server

    # Load environment variables from .env file
    load_dotenv()
    init_tokenizer()
    init_ollama_backend()
    _host = os.getenv("CHROMA_HOST", "localhost")
    _port = int(os.getenv("CHROMA_PORT", 8000))
    _collection_name = os.getenv("COLLECTION_NAME", "default_collection")
    # Initialize the ChromaDB collection
    try:
        _collection = get_collection(_collection_name, _host, _port)
    except ConnectionError as e:
        logger.error(f"Error connecting the DB server, trying to start now... Original Error message: {e}")
        _db_path = os.getenv("CHROMA_DB_PATH", "../vectordb-stores/chromadb")
        start_chroma_db_server(_host, _port, _db_path)
        _collection = get_collection(_collection_name, _host, _port)
    # Convert PDF to text, split into chunks, embed with "nomic-embed-text" model and write to chroma DB.
    _embed_model = os.getenv("EMBED_MODEL", "nomic-embed-text")
    _file_path = "../data/ev_outlook_2023.pdf"
    _chunks = pdf.pdf_to_text_chunk(_file_path)
    batch_write_chunk_to_db(_collection, _chunks)

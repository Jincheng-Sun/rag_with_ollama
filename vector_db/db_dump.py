import os
import time
import logging

import ollama
import chromadb
from dotenv import load_dotenv
from mattsollamatools import chunk_text_by_sentences

from utilities import readtext, getconfig
from db_init import get_collection

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_tokenizer():
    import nltk
    from nltk.tokenize import sent_tokenize
    try:
        sent_tokenize("Hello do I have punkt tokenizer?")
    except LookupError:
        nltk.download('punkt')


def init_ollama_backend(model_name: str = "nomic-embed-text"):
    # docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
    ollama.pull(model_name)


def ollama_pull_model(ollama_host: str = "http://localhost:11434", model_name: str = 'llama3'):
    import requests
    url = f"{ollama_host}/api/pull"
    data = {"name": model_name}
    response = requests.post(url, json=data)
    logger.info(response.json())


def process_chunks(collection, embed_model="nomic-embed-text", source_path: str = "./source_links.txt"):
    start_time = time.time()
    with open(source_path) as f:
        lines = f.readlines()
        for link in lines:
            text = readtext(link)
            chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=0)
            logger.info(f"Processing {link} with {len(chunks)} chunks")
            for index, chunk in enumerate(chunks):
                embed = ollama.embeddings(model=embed_model, prompt=chunk)['embedding']
                logger.info(f"Adding chunk {index} from {link}")
                collection.add([link + str(index)], [embed], documents=[chunk], metadatas={"source": link})
    logger.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    init_tokenizer()
    init_ollama_backend()
    _host = os.getenv("CHROMA_HOST", "localhost")
    _port = int(os.getenv("CHROMA_PORT", 8000))
    _collection_name = os.getenv("COLLECTION_NAME", "default_collection")
    # Initialize the ChromaDB collection
    _collection = get_collection(_collection_name, _host, _port)
    _embed_model = "nomic-embed-text"
    process_chunks(_collection, _embed_model)

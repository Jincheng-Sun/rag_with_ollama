import os
import time
import subprocess

import chromadb
from chromadb.api import ClientAPI
from chromadb.api.models import Collection
from dotenv import load_dotenv
from loguru import logger


def start_chroma_db_server(host: str, port: int, db_path: str) -> subprocess.Popen:
    cmd = f"chroma run --host {host} --port {port} --path {db_path}"
    process = subprocess.Popen(cmd, shell=True)
    return process


def get_client(host: str, port: int) -> ClientAPI:
    return chromadb.HttpClient(host=host, port=port)


def get_collection(collection_name: str, host: str = 'localhost', port: int = 8000, init: bool = False) -> Collection:
    client = get_client(host, port)
    if init:
        # Check if the collection exists, delete if it does
        if any(coll.name == collection_name for coll in client.list_collections()):
            logger.info(f'Deleting collection: {collection_name}')
            client.delete_collection(collection_name)
    # See other distance functions here: https://docs.trychroma.com/guides#changing-the-distance-function
    coll = client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
    return coll


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    _host = os.getenv("CHROMA_HOST", "localhost")
    _port = int(os.getenv("CHROMA_PORT", 8000))
    _collection_name = os.getenv("COLLECTION_NAME", "default_collection")
    _db_path = os.getenv("CHROMA_DB_PATH", "../vectordb-stores/chromadb")
    # Start the ChromaDB server
    chroma_process = start_chroma_db_server(_host, _port, _db_path)
    # Wait for a while for the server to start
    time.sleep(10)
    try:
        # Initialize the ChromaDB collection
        _ = get_collection(_collection_name, _host, _port)
        logger.info("Chroma DB started")
    finally:
        # Ensure the ChromaDB server is stopped after initialization
        chroma_process.terminate()
        chroma_process.wait()
        logger.info("Chroma DB terminated")


import os
import logging

import chromadb
from chromadb.api import ClientAPI
from chromadb.api.models import Collection
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    # command line: chroma run --host localhost --port 8000 --path ../vectordb-stores/chromadb
    # Load environment variables from .env file
    load_dotenv()
    _host = os.getenv("CHROMA_HOST", "localhost")
    _port = int(os.getenv("CHROMA_PORT", 8000))
    _collection_name = os.getenv("COLLECTION_NAME", "default_collection")
    # Initialize the ChromaDB collection
    _ = get_collection(_collection_name, _host, _port)

#!/bin/bash

# run_docker.sh

# Start all services in detached mode
docker-compose up -d

# Wait for the ollama service to be ready
echo "Waiting for ollama service to be ready..."
sleep 5

# Pull the models
echo "Pulling embedding model..."
docker-compose exec ollama ollama pull "${EMBED_MODEL:-nomic-embed-text}"

echo "Pulling language model..."
docker-compose exec ollama ollama pull "${LANGUAGE_MODEL:-phi3}"

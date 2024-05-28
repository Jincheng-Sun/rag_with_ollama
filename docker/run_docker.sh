#!/bin/bash

# run_docker.sh

# Generate a self-signed certificate
echo "Generating a self-signed certificate..."
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out my-ca.pem -days 3650 -nodes -subj "/CN=ollama.local"

# Copy the certificate to the ollama_with_ca folder
echo "Copying certificate to ollama_with_ca folder..."
cp my-ca.pem ./ollama_with_ca/

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

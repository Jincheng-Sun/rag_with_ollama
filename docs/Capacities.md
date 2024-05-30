
# Capacities

## Current Capacity

- **UI**:
  - Attach document(s) in chat
  - Upload document(s) in workspace
  - Reference a single document in chat
  - Reference all the documents, use the top 5 (by default) similar text chunks as the enhanced context
  - Set multiple models for comparison
  - Preserve chat history
  - Prompt Engineering & Management
  - Document management
  - RAG parameters configuration
  - Administration management



- **Vector Store**:
  - Chroma DB as backend
  - Free to choose embedding models (Local Ollama or OpenAI models)
  - Similarity search for similar content
  - (Optional) Advanced hybrid searching with re-ranking model

- **Models and Backend**:
  - Able to parse various format of documents (pdf, xlsx, docs...) 
  - Able to pull an Ollama model from Ollama Registry

## What is Missing

- **UI**:
  - Lacking a visual tool of the vector store (view collections, vector, original text, search for similar text...)
  - Lacking transparency of the RAG process (e.g. the user are not able to see which content has been chosen from the vector store)
  - Currently only provide OpenAI or Ollama model option, we can add support for Hugging Face and other polular registry platform

- **Models and Backend**:
  - Not able to parse image, we can enrich it's document parcing ability
  - Lacking a PII removal feature
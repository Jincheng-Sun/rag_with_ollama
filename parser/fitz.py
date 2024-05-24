from pathlib import Path
from typing import List, Union

import pymupdf
from langchain.text_splitter import CharacterTextSplitter
from loguru import logger

max_size = 1024
chunk_size = 1024
chunk_overlap = 128

all_chunks = []
splitter = CharacterTextSplitter(
    separator="\n",
    keep_separator=True,
    chunk_size=1024,
    chunk_overlap=128,
)

file_path = "../data/ev_outlook_2023.pdf"
doc = pymupdf.open(file_path)
current_text = ""
for page in doc:
    text = page.get_text("block")

    if len(text) > max_size:
        all_chunks.append(
            {"text": current_text, "metadata": {"page": page.number}}
        )
        chunks = splitter.split_text(text)
        for chunk in chunks:
            logger.info(
                f"Flushing chunk. Length: {len(chunk)}, page: {page.number}"
            )
            all_chunks.append(
                {"text": chunk, "metadata": {"page": page.number}}
            )
        current_text = ""

    elif len(current_text + text) >= max_size:
        if current_text != "":
            all_chunks.append(
                {"text": current_text, "metadata": {"page": page.number}}
            )
        logger.info(
            f"Flushing chunk. Length: {len(current_text)}, page: {page.number}"
        )
        current_text = text

    # Otherwise, add element's text to current chunk, without re-assigning the page number
    else:
        current_text += text

# Filter out empty docs
all_chunks = [
    chunk for chunk in all_chunks if chunk["text"].strip().replace(" ", "")
]

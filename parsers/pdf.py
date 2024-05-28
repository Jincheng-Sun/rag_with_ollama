import pymupdf
from langchain.text_splitter import CharacterTextSplitter
from loguru import logger


def pdf_to_text_chunk(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    res = []
    splitter = CharacterTextSplitter(
        separator="\n",
        keep_separator=False,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    doc = pymupdf.open(file_path)
    for page in doc:
        logger.info(f"Parsing page {page.number}...")
        text = page.get_text("block")
        chunks = splitter.split_text(text)
        logger.info(f"Splitting page into {len(chunks)} chunks")
        for chunk in chunks:
            res.append({"text": chunk, "metadata": {"page": page.number}})
    return res


if __name__ == "__main__":
    _file_path = "../data/ev_outlook_2023.pdf"
    _chunks = pdf_to_text_chunk(_file_path)

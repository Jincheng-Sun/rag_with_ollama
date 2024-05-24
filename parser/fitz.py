import pymupdf
from langchain.text_splitter import CharacterTextSplitter


def pdf_to_text_chunk(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    chunks = []
    splitter = CharacterTextSplitter(
        separator="\n",
        keep_separator=False,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    doc = pymupdf.open(file_path)
    for page in doc:
        text = page.get_text("block")
        chunks = splitter.split_text(text)
        for chunk in chunks:
            chunks.append({"text": chunk, "metadata": {"page": page.number}})
    return chunks


if __name__ == "__main__":
    _file_path = "../data/ev_outlook_2023.pdf"
    _chunks = pdf_to_text_chunk(_file_path)

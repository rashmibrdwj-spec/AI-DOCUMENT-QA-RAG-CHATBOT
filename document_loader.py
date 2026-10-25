from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import (RecursiveCharacterTextSplitter)


def extract_text_from_pdfs(uploaded_files):
    documents = []

    for file in uploaded_files:
        reader = PdfReader(file)

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            if text and text.strip():
                document = Document(
                    page_content=text,
                    metadata={
                        "source": file.name,
                        "page": page_number
                    }
                )

                documents.append(document)

    return documents
def split_documents_into_chunks(documents):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120
    ) 
    chunks=splitter.split_documents(documents)
    return chunks
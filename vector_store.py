from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
def create_vector_store(chunks):

    if not chunks:
        raise ValueError("No text chunks available to process.")

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    return vector_store
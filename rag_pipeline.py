import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from prompt import SYSTEM_PROMPT

load_dotenv()
def retrieve_relevant_chunks(vector_store, question):

    if vector_store is None:
        return []

    if not question or not question.strip():
        return []

    results = vector_store.similarity_search(
        question,
        k=4
    )

    return results


def generate_answer(question, retrieved_chunks):

    if not retrieved_chunks:
        return (
            "I could not find this information "
            "in the uploaded documents."
        )

    context_parts = []

    for chunk in retrieved_chunks:

        source = chunk.metadata.get("source", "Unknown")
        page = chunk.metadata.get("page", "Unknown")

        context_parts.append(
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content: {chunk.page_content}"
        )

    context = "\n\n".join(context_parts)

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Check your .env file."
        )

    llm = ChatOllama(
        model="llama3.1:8b",
        temperature=0,
        api_key=api_key
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=(
                f"Question: {question}\n\n"
                f"Retrieved context:\n{context}"
            )
        )
    ]

    response = llm.invoke(messages)

    return response.content
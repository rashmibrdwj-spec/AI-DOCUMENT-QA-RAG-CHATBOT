import streamlit as st

from document_loader import (
    extract_text_from_pdfs,
    split_documents_into_chunks
)

from vector_store import create_vector_store

from rag_pipeline import (
    retrieve_relevant_chunks,
    generate_answer
)

st.set_page_config(
    page_title="Domain-Specific RAG Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Domain-Specific RAG Chatbot")

st.write(
    "Upload PDF documents and ask questions "
    "to receive AI-generated answers."
)

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "documents" not in st.session_state:
    st.session_state.documents = []

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "retrieved_chunks" not in st.session_state:
    st.session_state.retrieved_chunks = []

if "answer" not in st.session_state:
    st.session_state.answer = ""

def clear_files():
    st.session_state.uploader_key += 1
    st.session_state.documents = []
    st.session_state.chunks = []
    st.session_state.vector_store = None
    st.session_state.retrieved_chunks = []
    st.session_state.answer = ""

uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True,
    key=f"pdf_uploader_{st.session_state.uploader_key}"
)

if uploaded_files:

    st.success(
        f"{len(uploaded_files)} PDF file(s) uploaded."
    )

    for file in uploaded_files:
        st.write(f"📄 {file.name}")

    st.button(
        "Clear Uploaded Files",
        on_click=clear_files
    )

    if st.button("Process PDF Documents"):

        try:
            with st.spinner("Extracting PDF text..."):
                documents = extract_text_from_pdfs(
                    uploaded_files
                )

            if not documents:
                st.warning(
                    "No extractable text found in the PDFs."
                )

                st.session_state.documents = []
                st.session_state.chunks = []
                st.session_state.vector_store = None
                st.session_state.retrieved_chunks = []
                st.session_state.answer = ""

            else:
                with st.spinner("Creating text chunks..."):
                    chunks = split_documents_into_chunks(
                        documents
                    )

                if not chunks:
                    st.warning(
                        "No text chunks were created."
                    )

                    st.session_state.documents = []
                    st.session_state.chunks = []
                    st.session_state.vector_store = None

                else:
                    with st.spinner(
                        "Creating embeddings and vector store..."
                    ):
                        vector_store = create_vector_store(
                            chunks
                        )

                    st.session_state.documents = documents
                    st.session_state.chunks = chunks
                    st.session_state.vector_store = vector_store
                    st.session_state.retrieved_chunks = []
                    st.session_state.answer = ""

                    st.success(
                        f"Processing complete! "
                        f"{len(documents)} page(s) extracted, "
                        f"{len(chunks)} chunks created, "
                        f"and vector store ready."
                    )

        except Exception as error:
            st.error(f"Document processing failed: {error}")

    if st.session_state.documents:

        with st.expander("📄 View Extracted Text"):

            for document in st.session_state.documents:
                st.markdown(
                    f"**{document.metadata.get('source', 'Unknown')} "
                    f"— Page {document.metadata.get('page', 'Unknown')}**"
                )

                st.write(document.page_content)
    if st.session_state.chunks:

        with st.expander("✂️ View Text Chunks"):

            for index, chunk in enumerate(
                st.session_state.chunks,
                start=1
            ):
                st.markdown(f"**Chunk {index}**")
                st.write(chunk.page_content)

    st.header("🤖 Ask Questions About Your PDFs")

    if st.session_state.vector_store is None:

        st.info(
            "Upload your PDFs and click "
            "'Process PDF Documents' first."
        )

    else:

        question = st.text_input(
            "Enter your question",
            key="question_input",
            placeholder="Example: What skills are mentioned?"
        )

        if st.button("Generate AI Answer"):

            if not question.strip():

                st.warning("Please enter a question.")

            else:

                try:
                    
                    with st.spinner(
                        "Retrieving relevant information..."
                    ):
                        retrieved_chunks = retrieve_relevant_chunks(
                            st.session_state.vector_store,
                            question
                        )

                    st.session_state.retrieved_chunks = (
                        retrieved_chunks
                    )

                    if not retrieved_chunks:

                        st.session_state.answer = (
                            "I could not find relevant information "
                            "in the uploaded documents."
                        )

                    else:
                        

                        with st.spinner(
                            "Generating AI answer..."
                        ):
                            answer = generate_answer(
                                question,
                                retrieved_chunks
                            )

                        st.session_state.answer = str(answer)

                except Exception as error:

                    st.session_state.answer = ""

                    st.error(
                        f"Question processing failed: {error}"
                    )

    if st.session_state.answer:

        st.subheader("💡 AI-Generated Answer")

        st.markdown(st.session_state.answer)

    if st.session_state.retrieved_chunks:

        st.subheader("📚 Retrieved Sources")

        for index, chunk in enumerate(
            st.session_state.retrieved_chunks,
            start=1
        ):
            source = chunk.metadata.get(
                "source", "Unknown"
            )

            page = chunk.metadata.get(
                "page", "Unknown"
            )

            with st.expander(f"Source {index}: {source}"):

                st.write(chunk.page_content)

                st.caption(f"Page: {page}")

else:

    st.info("Please upload at least one PDF to begin.")


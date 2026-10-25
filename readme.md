# Domain-Specific RAG Chatbot for PDF Question Answering

## 1. Project Overview

The Domain-Specific RAG Chatbot is an AI-powered application that allows users to upload PDF documents and ask questions about their contents.

It extracts text from uploaded PDFs, divides the text into smaller chunks, creates embeddings, and stores them in a FAISS vector store. When a user asks a question, the system retrieves relevant chunks to help generate an answer using a Large Language Model (LLM).

## 2. Objectives

- Upload one or multiple PDF documents.
- Extract text from PDF files.
- Divide extracted text into smaller chunks.
- Generate embeddings for text chunks.
- Store embeddings using FAISS.
- Retrieve relevant information based on user questions.
- Generate answers using an AI language model.
- Display relevant information from uploaded documents.

## 3. Technologies Used

- Python
- Streamlit
- PyPDF
- LangChain
- Sentence Transformers
- FAISS
- Groq API
- Large Language Models (LLMs)

## 4. Project Modules

### Module 1: Document Upload
Allows users to upload one or multiple PDF documents and displays their filenames.

### Module 2: Text Extraction
Extracts text from PDF pages and stores the source filename and page number.

### Module 3: Text Chunking
Divides extracted text into smaller chunks with overlapping content.

### Module 4: Embeddings and Vector Store
Converts text chunks into numerical embeddings using Sentence Transformers and stores them in FAISS.

### Module 5: Retrieval
Searches the vector store and retrieves the most relevant text chunks for a user's question.

### Module 6: AI Answer Generation
Uses a Large Language Model through the Groq API to generate answers based on retrieved document content.

### Module 7: User Interface
Provides an interactive Streamlit interface for uploading PDFs and asking questions.

## 5. Project Structure

```text
domain_rag_chatbot/
│
├── app.py
├── document_loader.py
├── vector_store.py
├── rag_pipeline.py
├── prompt.py
├── requirements.txt
├── README.md
└── .env
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config import docs, RAG_CHUNK_SIZE, RAG_CHUNK_OVERLAP, EMBED_MODEL, RAG_TOP_K

# Use a local HuggingFace model
#EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

class RAGPipeline:
    def __init__(self):
        # Local embeddings, no API token required
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        self.vectorstore = self._build_db()

    def _build_db(self):
        # Convert strings to Document objects
        documents = [Document(page_content=str(doc), metadata={"source": "sample"}) for doc in docs]

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=RAG_CHUNK_SIZE,
            chunk_overlap=RAG_CHUNK_OVERLAP
        )
        chunks = text_splitter.split_documents(documents)

        # Build Chroma vector store
        return Chroma.from_documents(chunks, self.embeddings, persist_directory=None)

    def retrieve(self, query):
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": RAG_TOP_K}
        )
        docs = retriever.invoke(query)
        return [str(d.page_content) for d in docs]

    def format_context(self, docs):
        return "\n\n".join([f".{doc}" for doc in docs])

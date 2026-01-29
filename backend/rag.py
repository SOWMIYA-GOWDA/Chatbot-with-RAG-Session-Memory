from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import TextLoader

DB_PATH = "vector_db"

_embedding = None

def get_embedding():
    global _embedding
    if _embedding is None:
        _embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return _embedding

def build_vector_db():
    loader = TextLoader("data/leave_policy.md")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embedding = get_embedding()
    db = Chroma.from_documents(chunks, embedding, persist_directory=DB_PATH)
    db.persist()
    return db

def load_vector_db():
    embedding = get_embedding()
    return Chroma(persist_directory=DB_PATH, embedding_function=embedding)
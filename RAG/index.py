import os
import time
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

load_dotenv()

pdf_path = Path(__file__).parent / "BNS.pdf"
# Load the PDF
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()
print(f"Loaded {len(docs)} pages")

# Split the document into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)
print(f"Split into {len(chunks)} chunks")

# Vector embeddings
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001")

# Create Qdrant collection first
qdrant_client = QdrantClient(url="http://localhost:6333")

# Get embedding dimension with a test embed
test_embedding = embedding_model.embed_query("test")
embedding_dim = len(test_embedding)
print(f"Embedding dimension: {embedding_dim}")

# Recreate collection
collection_name = "bns_pdf"
if qdrant_client.collection_exists(collection_name):
    qdrant_client.delete_collection(collection_name)

qdrant_client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE)
)

# Create vector store
vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name=collection_name,
    embedding=embedding_model,
)

# Add documents in small batches with delay to avoid rate limits
batch_size = 5
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i + batch_size]
    try:
        vector_store.add_documents(batch)
        print(f"Indexed batch {i // batch_size + 1}/{(len(chunks) + batch_size - 1) // batch_size}")
    except Exception as e:
        print(f"Rate limited on batch {i // batch_size + 1}, waiting 10s... ({e})")
        time.sleep(10)
        vector_store.add_documents(batch)
        print(f"Indexed batch {i // batch_size + 1} (retry success)")
    time.sleep(2)  # Small delay between batches

print("Indexing of docs done")
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
import os

load_dotenv()

# Vector embeddings
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001")

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="bns_pdf",
    embedding=embedding_model,
)

# Take user input
user_query = input("Ask something: ")

# Relevant chunks from the vector db
search_results = vector_db.similarity_search(query=user_query)

context = "\n\n\n".join([
    f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}"
    for result in search_results
])

SYSTEM_PROMPT = f"""
You are a helpfull AI Assistant who answeres user query based on the available context retrieved from a PDF file along with page_contents and page number.

Context:
{context}
"""

# Generate response using Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_client = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    system_instruction=SYSTEM_PROMPT
)

response = gemini_client.generate_content(
    contents=[
        { "role": "user", "parts": [user_query] }
    ]
)

print(f"🤖: {response.text}")
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

# --------------Ingestion Process---------------
# Step 1. Loading PDF Document
loader = PyPDFLoader("./Documents/HR-Policy.pdf")
document = loader.load()

# Step 2. Split the document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = text_splitter.split_documents(document)

# Step 3. Create an instance of embedding model
embedding = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

# Step 4. Store embeddings in vector database
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="./chromadb"
)

import os
import pytesseract
from PIL import Image
from pdfminer.high_level import extract_text
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# --- CONFIGURATION ---
# 1. Update this path if you installed Tesseract somewhere else!
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up two levels to reach 'data'
DATA_PATH = os.path.join(BASE_DIR, "../../data/knowledge_base")
FRAUD_PATH = os.path.join(BASE_DIR, "../../data/fraud_test")
DB_FAISS_PATH = os.path.join(BASE_DIR, "../../data/vector_store")

def get_text_from_file(file_path):
    """
    Smart Router: 
    - If PDF: Use pdfminer (Fast)
    - If Image (JPG/PNG): Use Tesseract (OCR)
    """
    filename = os.path.basename(file_path)
    
    try:
        if filename.lower().endswith('.pdf'):
            # It is a Digital PDF
            text = extract_text(file_path)
            if text and len(text) > 10:
                return text
            else:
                return "" # Empty PDF
                
        elif filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # It is an Image -> Use OCR
            print(f"👁️  Running OCR on: {filename}")
            text = pytesseract.image_to_string(Image.open(file_path))
            return text
            
    except Exception as e:
        print(f"❌ Error reading {filename}: {e}")
        return ""

def create_vector_db():
    print("🚀 Starting Ingestion Pipeline...")
    
    documents = []
    
    # 1. Gather all files from both folders
    all_files = []
    
    if os.path.exists(DATA_PATH):
        for f in os.listdir(DATA_PATH):
            all_files.append(os.path.join(DATA_PATH, f))
            
    if os.path.exists(FRAUD_PATH):
        for f in os.listdir(FRAUD_PATH):
            all_files.append(os.path.join(FRAUD_PATH, f))

    print(f"📂 Found {len(all_files)} files to process.")

    # 2. Process Files
    for file_path in all_files:
        raw_text = get_text_from_file(file_path)
        
        if raw_text:
            # Create a Document Object
            doc = Document(
                page_content=raw_text, 
                metadata={"source": os.path.basename(file_path)}
            )
            documents.append(doc)

    print(f"✅ Extracted text from {len(documents)} documents.")

    if not documents:
        print("⚠️ No documents found! Check your data folder.")
        return

    # 3. Chunking (Splitting text)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    print(f"✂️  Split into {len(texts)} chunks.")

    # 4. Embeddings (Loading the AI Model)
    print("🧠 Loading AI Model (MiniLM)...")
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'}
    )

    # 5. Create & Save Vector DB
    print("💾 Creating FAISS Index...")
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)
    print(f"🎉 Success! Database saved to {DB_FAISS_PATH}")

if __name__ == "__main__":
    create_vector_db()
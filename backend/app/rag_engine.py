import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# --- CONFIGURATION ---
# 1. PASTE YOUR GROQ KEY HERE!
#USER: Replace these with your own keys in production!
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FAISS_PATH = os.path.join(BASE_DIR, "../../data/vector_store")

def get_rag_chain():
    print("🧠 Loading Embeddings (Local)...")
    # Embeddings run locally on your CPU (Never fails)
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'}
    )
    
    print("📂 Loading Database...")
    db = FAISS.load_local(
        DB_FAISS_PATH, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    retriever = db.as_retriever(search_kwargs={'k': 2})

    # Strict Prompt for Audit
    template = """You are a strict financial auditor. 
    Use the following invoice context to answer the question.
    If the answer is not in the text, say "Data not found".
    
    Context: {context}
    
    Question: {question}
    
    Answer:"""
    
    prompt = PromptTemplate(template=template, input_variables=['context', 'question'])
    
    # 🟢 CONNECTING TO GROQ (Llama 3.3)
    print("⚡ Connecting to Groq Cloud (Llama-3.3)...")
    llm = ChatGroq(
        temperature=0, 
        # UPDATED MODEL NAME (The old one was retired)
        model_name="llama-3.3-70b-versatile", 
        api_key=GROQ_API_KEY
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={'prompt': prompt}
    )
    
    return qa_chain

if __name__ == "__main__":
    print("🚀 Starting RAG Engine (Groq High-Speed Mode)...")
    try:
        if "gsk_" not in GROQ_API_KEY:
             print("❌ ERROR: Please paste your Groq API Key in Line 10!")
             exit()

        chain = get_rag_chain()
        
        # Test Query
        query = "What is the total amount for DarkWeb Solutions Ltd?"
        print(f"\n❓ Asking: {query}")
        result = chain.invoke({"query": query})
        
        print(f"🤖 Answer: {result['result']}")
        
    except Exception as e:
        print(f"❌ Critical Error: {e}")
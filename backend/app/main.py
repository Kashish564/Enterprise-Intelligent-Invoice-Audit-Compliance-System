from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os

# We remove 'app.' because we are already inside the folder
from .rag_engine import get_rag_chain
from .audit import check_compliance

app = FastAPI(title="Invoice Audit AI")

# --- GLOBAL STATE ---
# We load the AI Chain once when the server starts so it's fast
print("⏳ Booting up AI Audit Server...")
qa_chain = get_rag_chain()
print("✅ Server Ready!")

# Define the Input Format
class QueryRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"status": "active", "message": "Barclays Audit AI is Ready"}

@app.post("/analyze")
def analyze_invoice(request: QueryRequest):
    """
    The Core Endpoint:
    1. Receives User Question
    2. Asks AI (RAG)
    3. Audits the retrieved Invoice Text for Fraud
    4. Returns EVERYTHING (Answer + Risks)
    """
    try:
        # Step 1: Run RAG (Get Answer + Context)
        # We invoke the chain we loaded at startup
        response = qa_chain.invoke({"query": request.question})
        
        ai_answer = response['result']
        source_documents = response['source_documents']
        
       # Step 2: Run Compliance Engine on the Documents directly
        # We pass the list of docs, not just text, so we know WHICH file has the risk
        risk_flags = check_compliance(source_documents)
        
        # Step 4: Return JSON Response
        return {
            "ai_answer": ai_answer,
            "risk_analysis": risk_flags,
            "sources": [doc.metadata.get("source", "Unknown") for doc in source_documents]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the server on Port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
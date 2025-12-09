# 🛡️ Enterprise Intelligent Invoice Audit System

### An AI Platform for Financial Compliance & Fraud Detection.

This system automates the extraction, auditing, and validation of unstructured financial documents (invoices). It combines Generative AI (Llama-3 via Groq) for 
semantic understanding with Deterministic Python Logic for rigorous compliance checks
(AML Blacklists, Risk Thresholds).

---

## 🚀 Key Features

* **Hybrid Ingestion Pipeline:** Automatically routes digital PDFs to `PDFMiner` and scanned images to `Tesseract OCR`.
* **High-Speed RAG:** Uses **Groq LPU** inference for sub-second retrieval and answering.
* **Compliance Guardrails:**
    * 🔴 **Blacklist Check:** Flags vendors against a mock International Sanctions List.
    * 💰 **Risk Thresholds:** Auto-flags transactions > $10,000 for manual review.
    * 📅 **Forensic Logic:** Detects future-dating anomalies and math discrepancies.
* **Microservices Architecture:** Decoupled **FastAPI** backend and **Streamlit** frontend, containerized with **Docker**.

---

## 🛠️ Tech Stack

* **AI/LLM:** Llama-3-8B (via Groq), Hugging Face Embeddings.
* **Vector DB:** FAISS (Local CPU-based).
* **Backend:** Python, FastAPI, Uvicorn.
* **Frontend:** Streamlit.
* **DevOps:** Docker, Docker Compose.

---

## 🏃‍♂️ How to Run Locally

### Option 1: Using Docker (Recommended)
1.  Clone the repository:
    ```bash
    git clone (https://github.com/Kashish564/Enterprise-Intelligent-Invoice-Audit-Compliance-System.git)
    ```
2.  Add your API Keys in `backend/app/rag_engine.py`.
3.  Run with Docker Compose:
    ```bash
    docker-compose up --build
    ```
4.  Access the UI at `http://localhost:8501`.

### Option 2: Manual Setup
1.  Install dependencies:
    ```bash
    pip install -r backend/requirements.txt
    pip install -r frontend/requirements.txt
    ```
2.  Start Backend:
    ```bash
    python backend/app/main.py
    ```
3.  Start Frontend:
    ```bash
    streamlit run frontend/app.py
    ```

---

## 📸 Screenshots


import os
import requests
import zipfile
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# --- CONFIGURATION ---
# 1. Digital PDFs Source
REAL_DATA_URL = "https://github.com/femstac/Sample-Pdf-invoices/archive/refs/heads/master.zip"
BASE_DIR = "data"
KNOWLEDGE_BASE = os.path.join(BASE_DIR, "knowledge_base")
FRAUD_TEST = os.path.join(BASE_DIR, "fraud_test")

def download_digital_invoices():
    """Downloads digital PDFs from GitHub to mix with your Kaggle images."""
    print(f"⬇️  Downloading Digital PDFs from GitHub...")
    
    try:
        r = requests.get(REAL_DATA_URL)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        
        count = 0
        for file in z.namelist():
            if file.endswith(".pdf") and "Invoice" in file:
                filename = os.path.basename(file)
                target_path = os.path.join(KNOWLEDGE_BASE, filename)
                
                # Only save if it doesn't exist (don't overwrite Kaggle data)
                if not os.path.exists(target_path):
                    with open(target_path, "wb") as f:
                        f.write(z.read(file))
                    count += 1
                
                if count >= 30: # Limit to 30 PDFs so we have a mix
                    break
        
        print(f"✅ Added {count} Digital PDFs to {KNOWLEDGE_BASE}")
        
    except Exception as e:
        print(f"❌ Error downloading GitHub data: {e}")

def create_pdf(path, filename, vendor, date, total, line_items):
    """Generates synthetic Fraud cases."""
    c = canvas.Canvas(os.path.join(path, filename), pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, f"INVOICE - {vendor}")
    
    # Metadata
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Date: {date}")
    c.drawString(50, height - 100, f"Invoice #: INV-{hash(vendor)%10000}")
    
    # Line Items (Table)
    y = height - 150
    c.drawString(50, y, "Description")
    c.drawString(400, y, "Amount")
    c.line(50, y-5, 500, y-5)
    y -= 25
    
    for item, price in line_items:
        c.drawString(50, y, item)
        c.drawString(400, y, f"{price}")
        y -= 20
        
    # Total
    c.setFont("Helvetica-Bold", 14)
    c.drawString(300, y - 20, f"TOTAL: {total}")
    c.save()
    print(f"   --> Generated Fraud Case: {filename}")

def generate_fraud_data():
    """Creates the 5 Specific Fraud Cases for your Demo."""
    print(f"🕵️  Generating Fraud Test Data in {FRAUD_TEST}...")
    
    create_pdf(FRAUD_TEST, "invoice_001.pdf", "Reliance Jio", "2024-01-15", "INR 4,500", 
               [("Internet Services", "4,500")])
    create_pdf(FRAUD_TEST, "invoice_blacklist.pdf", "DarkWeb Solutions Ltd", "2024-02-01", "INR 12,000",
               [("Hidden Services", "12,000")])
    create_pdf(FRAUD_TEST, "invoice_high_value.pdf", "Tata Consultancy Services", "2024-02-10", "INR 50,00,000",
               [("Consulting Fee", "50,00,000")])
    create_pdf(FRAUD_TEST, "invoice_future_date.pdf", "Infosys Ltd", "2030-01-01", "INR 50,000",
               [("Future Maintenance", "50,000")])
    create_pdf(FRAUD_TEST, "invoice_bad_tax.pdf", "Local Vendor", "2024-03-01", "INR 1,500",
               [("Subtotal", "1,000"), ("Tax (50%)", "500")])

    print("✅ Fraud dataset generated.")

if __name__ == "__main__":
    os.makedirs(KNOWLEDGE_BASE, exist_ok=True)
    os.makedirs(FRAUD_TEST, exist_ok=True)
    
    download_digital_invoices()
    generate_fraud_data()
    print("\n🎉 DATA SETUP COMPLETE!")
    print(f"👉 Please ensure you have pasted your Kaggle images into '{KNOWLEDGE_BASE}'")
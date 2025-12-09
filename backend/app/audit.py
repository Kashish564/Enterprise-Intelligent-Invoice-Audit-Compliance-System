import json
import os
import re
from datetime import datetime

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLACKLIST_PATH = os.path.join(BASE_DIR, "../../config/blacklist.json")

def load_blacklist():
    try:
        with open(BLACKLIST_PATH, "r") as f:
            return json.load(f)
    except:
        return {"banned_vendors": [], "risk_thresholds": {"require_manager_approval_above": 10000}}

def check_compliance(source_documents):
    """
    Updated to check EACH document separately.
    Input: List of LangChain Document objects
    """
    data = load_blacklist()
    banned_vendors = [v.lower() for v in data.get("banned_vendors", [])]
    threshold = data.get("risk_thresholds", {}).get("require_manager_approval_above", 10000)
    
    flags = []

    # Iterate through every retrieved document chunk
    for doc in source_documents:
        text_content = doc.page_content
        text_lower = text_content.lower()
        # Get filename from metadata (or default to 'Unknown')
        source_file = doc.metadata.get("source", "Unknown File")

        # 🔴 RULE 1: Blacklist Check
        for vendor in banned_vendors:
            if vendor in text_lower:
                flags.append({
                    "rule": "Blacklisted Vendor",
                    "severity": "CRITICAL",
                    "message": f"Found '{vendor.title()}' in file '{source_file}'."
                })

        # 🔴 RULE 2: High Value Check
        matches = re.findall(r'(?:INR|Rs\.|₹|\$)\s*([\d,]+(?:\.\d{2})?)', text_content, re.IGNORECASE)
        max_found = 0.0
        for amt_str in matches:
            clean_str = amt_str.replace(",", "").strip()
            try:
                if clean_str:
                    val = float(clean_str)
                    if val > max_found: max_found = val
            except: continue

        if max_found > threshold:
            flags.append({
                "rule": "High Value Transaction",
                "severity": "HIGH",
                "message": f"Amount {max_found:,.2f} in '{source_file}' exceeds limit."
            })

        # 🔴 RULE 3: Future Date Check
        dates = re.findall(r'(\d{4}-\d{2}-\d{2})', text_content)
        today = datetime.now()
        for date_str in dates:
            try:
                inv_date = datetime.strptime(date_str, "%Y-%m-%d")
                if inv_date > today:
                    flags.append({
                        "rule": "Future Dating Anomaly",
                        "severity": "MEDIUM",
                        "message": f"Future date {date_str} detected in '{source_file}'."
                    })
            except: pass

    # Remove duplicates (if the same risk appears in multiple chunks of the same file)
    # We use a trick: Convert list of dicts to a set of tuples, then back
    unique_flags = [dict(t) for t in {tuple(d.items()) for d in flags}]
    
    return unique_flags
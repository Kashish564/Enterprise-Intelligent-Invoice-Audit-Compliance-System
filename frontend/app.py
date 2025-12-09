import streamlit as st
import requests
import json
import pandas as pd

# --- CONFIGURATION ---
# Pointing to your FastAPI Backend
import os
# If running in Docker, use the variable. If running manually, use localhost.
API_URL = os.getenv("API_URL", "http://localhost:8000/analyze")

st.set_page_config(page_title="Invoice Auditor", layout="wide")

# --- UI HEADER ---
st.title("🛡️ Enterprise Intelligent Invoice Auditor")
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .big-font {
        font-size:20px !important;
    }
</style>
""", unsafe_allow_html=True)

st.info("System Status: 🟢 Connected to Groq Llama-3 & Compliance Engine")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Audit Settings")
    st.write("Current Policy: **Global Fraud Detection v2.1**")
    st.divider()
    st.write("Checking against:")
    st.checkbox("Sanctions Blacklist", value=True, disabled=True)
    st.checkbox("High Value Thresholds", value=True, disabled=True)
    st.checkbox("Future Date Logic", value=True, disabled=True)

# --- MAIN INPUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Ask the Auditor")
    user_query = st.text_input("Enter your query about the invoices:", 
                              placeholder="e.g., What is the total for DarkWeb Solutions?",
                              help="Ask about vendors, amounts, dates, or anomalies.")
    
    run_button = st.button("🚀 Run Audit Analysis", use_container_width=True)

# --- RESULTS SECTION ---
if run_button and user_query:
    with st.spinner("🤖 AI is reading invoices & Running Compliance Checks..."):
        try:
            # 1. SEND REQUEST TO FASTAPI BACKEND
            payload = {"question": user_query}
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                # --- SECTION 1: AI ANSWER ---
                st.success("Analysis Complete")
                st.subheader("📝 AI Findings")
                st.write(data["ai_answer"])
                
                # --- SECTION 2: RISK REPORT (The Fintech Part) ---
                st.divider()
                st.subheader("🚨 Risk & Compliance Report")
                
                risks = data["risk_analysis"]
                
                if not risks:
                    st.balloons()
                    st.success("✅ No Compliance Risks Detected. Invoice is clean.")
                else:
                    # Display risks nicely
                    for risk in risks:
                        severity = risk["severity"]
                        msg = f"**{risk['rule']}**: {risk['message']}"
                        
                        if severity == "CRITICAL":
                            st.error(f"🔴 {msg}")
                        elif severity == "HIGH":
                            st.warning(f"mV {msg}")
                        else:
                            st.info(f"🔵 {msg}")
                    
                    # Show data table for "Auditor View"
                    with st.expander("View Raw Audit Data"):
                        st.json(risks)

                # --- SECTION 3: SOURCES ---
                st.divider()
                st.caption(f"Sources utilized: {data['sources']}")
                
            else:
                st.error(f"Server Error: {response.text}")
                
        except Exception as e:
            st.error(f"Connection Failed. Is the Backend running? Error: {e}")
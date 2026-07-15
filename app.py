# -*- coding: utf-8 -*-
import streamlit as st
from ocr_reader import extract_text_from_pdf, extract_text_from_image
from llm_extractor import extract_invoice_data
from validator import validate_invoice
from database import init_db, save_invoice, get_all_invoices
from rpa_entry import save_to_excel
from email_fetcher import fetch_invoice_emails
from logger import log_info, log_error, log_warning, get_logs
from fraud_detector import detect_fraud
from scheduler import start_scheduler, stop_scheduler
import os
import pandas as pd

# Page config
st.set_page_config(
    page_title="AI Invoice Bot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0f1117; }
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #00d4ff;
        padding: 20px 0px 5px 0px;
    }
    .subtitle {
        text-align: center;
        font-size: 16px;
        color: #888888;
        margin-bottom: 10px;
    }
    .stButton>button {
        background-color: #00d4ff;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 30px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #00a8cc;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize database
init_db()
log_info("Invoice Bot started successfully")

# Initialize scheduler state
if 'scheduler_running' not in st.session_state:
    st.session_state.scheduler_running = False
if 'scheduler_thread' not in st.session_state:
    st.session_state.scheduler_thread = None

# Header
st.markdown('<div class="title">🤖 AI-Powered Invoice Processing Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">LLM + RPA | Local Prototype | 100% Free & Offline</div>', unsafe_allow_html=True)
st.divider()

# Confidence helper
def confidence_label(score):
    if score >= 80:
        return f"🟢 {score}% confident"
    elif score >= 50:
        return f"🟡 {score}% confident"
    else:
        return f"🔴 {score}% confident"

def process_single_invoice(file_path, file_type):
    try:
        log_info(f"Starting processing: {os.path.basename(file_path)}")

        with st.spinner("🔍 Reading invoice..."):
            if file_type == "application/pdf" or file_path.endswith('.pdf'):
                text = extract_text_from_pdf(file_path)
            else:
                text = extract_text_from_image(file_path)
        log_info(f"Text extracted: {os.path.basename(file_path)}")

        with st.expander("📄 View Raw Extracted Text"):
            st.text_area("", text, height=120)

        with st.spinner("🧠 AI extracting data..."):
            data = extract_invoice_data(text)
        log_info(f"AI extracted: vendor={data.get('vendor')}, invoice_no={data.get('invoice_number')}, total={data.get('total')}")

        st.markdown("### 🧠 AI Extracted Data")
        fields = [
            ("🏢 Vendor", "vendor", "vendor_confidence"),
            ("🔢 Invoice No.", "invoice_number", "invoice_number_confidence"),
            ("📅 Date", "date", "date_confidence"),
            ("💰 Total", "total", "total_confidence"),
            ("🧾 Tax", "tax", "tax_confidence"),
        ]

        for label, field, conf_field in fields:
            value = data.get(field, 'N/A')
            confidence = data.get(conf_field, 0)
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.metric(label, value)
            with col_b:
                st.markdown(f"<br>{confidence_label(confidence)}", unsafe_allow_html=True)

        # Fraud Detection
        st.markdown("### 🔍 Fraud Analysis")
        with st.spinner("🔍 Analyzing for fraud..."):
            risk_level, risk_score, reasons = detect_fraud(data)

        log_info(f"Fraud: {risk_level} risk ({risk_score}/100)")

        if risk_level == "HIGH":
            st.error(f"🔴 HIGH FRAUD RISK — Score: {risk_score}/100")
            log_warning(f"HIGH fraud risk: {data.get('invoice_number')}")
        elif risk_level == "MEDIUM":
            st.warning(f"🟡 MEDIUM FRAUD RISK — Score: {risk_score}/100")
            log_warning(f"MEDIUM fraud risk: {data.get('invoice_number')}")
        else:
            st.success(f"🟢 LOW FRAUD RISK — Score: {risk_score}/100")

        if reasons:
            st.markdown("**Suspicious findings:**")
            for reason in reasons:
                st.markdown(f"- {reason}")
        else:
            st.markdown("✅ No suspicious patterns detected")

        # Validate
        is_valid, messages = validate_invoice(data)

        if is_valid:
            st.success("✅ Invoice is Valid!")
            if risk_level == "HIGH":
                st.error("❌ Flagged for manual review — HIGH fraud risk!")
                log_warning(f"Blocked due to HIGH fraud risk: {data.get('invoice_number')}")
            else:
                saved = save_invoice(data)
                if saved:
                    st.success("💾 Saved to Database!")
                    log_info(f"Saved: {data.get('invoice_number')}")
                else:
                    st.warning("⚠️ Duplicate Invoice!")
                    log_warning(f"Duplicate: {data.get('invoice_number')}")
                save_to_excel(data)
                st.success("📊 Saved to Excel!")
        else:
            st.error("❌ Validation Failed!")
            for msg in messages:
                st.warning(msg)
                log_warning(f"Validation failed: {msg}")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        log_error(f"Error: {str(e)}")

# Sidebar
with st.sidebar:
    st.title("📋 Invoice Bot")
    st.markdown("---")
    st.markdown("### ⚙️ How it works")
    st.markdown("1. 📤 Upload Invoice")
    st.markdown("2. 🔍 OCR reads the text")
    st.markdown("3. 🧠 AI extracts data")
    st.markdown("4. 🔍 Fraud analysis")
    st.markdown("5. ✅ System validates")
    st.markdown("6. 💾 Saves to Database")
    st.markdown("7. 📊 Updates Excel")
    st.markdown("---")
    st.markdown("### 🛠️ Tech Stack")
    st.markdown("🧠 Mistral LLM (Ollama)")
    st.markdown("👁️ Tesseract OCR")
    st.markdown("🗄️ SQLite Database")
    st.markdown("📊 Excel (openpyxl)")
    st.markdown("🌐 Streamlit UI")
    st.markdown("📧 Gmail API")
    st.markdown("🔍 Fraud Detection")
    st.markdown("⏰ Auto-Scheduler")
    st.markdown("---")

    # Scheduler Control
    st.markdown("### ⏰ Auto-Scheduler")
    interval = st.selectbox("Check Gmail every:", [5, 10, 15, 30, 60], index=1)

    if not st.session_state.scheduler_running:
        if st.button("▶️ Start Scheduler"):
            st.session_state.scheduler_thread = start_scheduler(interval)
            st.session_state.scheduler_running = True
            st.success(f"✅ Scheduler started! Checking every {interval} mins")
            log_info(f"Scheduler started — every {interval} minutes")
    else:
        st.success(f"🟢 Scheduler is running")
        if st.button("⏹️ Stop Scheduler"):
            stop_scheduler()
            st.session_state.scheduler_running = False
            st.warning("⏹️ Scheduler stopped")
            log_info("Scheduler stopped")

    st.markdown("---")
    invoices = get_all_invoices()
    total_invoices = len(invoices)
    total_amount = sum([inv[4] for inv in invoices]) if invoices else 0
    st.markdown("### 📈 Stats")
    st.metric("Total Processed", total_invoices)
    st.metric("Total Amount", f"${total_amount:.2f}")

# Tabs
tab1, tab2, tab3 = st.tabs(["📤 Manual Upload", "📧 Fetch from Gmail", "📋 Logs"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 📤 Upload Invoice")
        uploaded_file = st.file_uploader(
            "Drag and drop or click to upload",
            type=["pdf", "png", "jpg", "jpeg"],
            help="Supported: PDF, PNG, JPG, JPEG"
        )

        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            file_path = os.path.join("invoices", uploaded_file.name)
            os.makedirs("invoices", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            log_info(f"Uploaded: {uploaded_file.name}")

            if st.button("🚀 Process Invoice"):
                with col2:
                    process_single_invoice(file_path, uploaded_file.type)

with tab2:
    st.markdown("### 📧 Fetch Invoices from Gmail")
    st.info("Searches Gmail for emails with 'invoice' in subject and downloads attachments.")

    if st.button("📧 Fetch Invoice Emails"):
        with st.spinner("Connecting to Gmail..."):
            try:
                log_info("Manual Gmail fetch...")
                files = fetch_invoice_emails()
                if files:
                    st.success(f"✅ Found {len(files)} invoice(s)!")
                    log_info(f"Found {len(files)} invoice(s)")
                    for file_path in files:
                        st.markdown(f"**Processing:** {os.path.basename(file_path)}")
                        process_single_invoice(file_path, "")
                else:
                    st.warning("No invoice emails found.")
                    log_warning("No invoice emails found")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                log_error(f"Gmail error: {str(e)}")

with tab3:
    st.markdown("### 📋 System Logs")
    st.info("Real-time log of all bot actions")

    if st.button("🔄 Refresh Logs"):
        pass

    logs = get_logs()
    if logs:
        log_text = "".join(logs)
        st.text_area("", log_text, height=400)

        info_count = sum(1 for l in logs if "INFO" in l)
        warning_count = sum(1 for l in logs if "WARNING" in l)
        error_count = sum(1 for l in logs if "ERROR" in l)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("✅ Info Logs", info_count)
        with c2:
            st.metric("⚠️ Warnings", warning_count)
        with c3:
            st.metric("❌ Errors", error_count)
    else:
        st.info("No logs yet.")

st.divider()

# All invoices table
st.markdown("### 📋 All Processed Invoices")
invoices = get_all_invoices()
if invoices:
    df = pd.DataFrame(invoices, columns=["ID", "Vendor", "Invoice No.", "Date", "Total", "Tax", "Status"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No invoices processed yet. Upload an invoice to get started!")
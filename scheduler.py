# -*- coding: utf-8 -*-
import schedule
import time
import threading
from email_fetcher import fetch_invoice_emails
from ocr_reader import extract_text_from_pdf, extract_text_from_image
from llm_extractor import extract_invoice_data
from validator import validate_invoice
from database import init_db, save_invoice
from rpa_entry import save_to_excel
from fraud_detector import detect_fraud
from logger import log_info, log_error, log_warning
import os

def process_invoice_file(file_path):
    try:
        log_info(f"Auto-scheduler processing: {os.path.basename(file_path)}")

        # Extract text
        if file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_image(file_path)

        # Extract data with LLM
        data = extract_invoice_data(text)
        log_info(f"Auto-extracted: vendor={data.get('vendor')}, total={data.get('total')}")

        # Fraud detection
        risk_level, risk_score, reasons = detect_fraud(data)
        log_info(f"Fraud check: {risk_level} risk ({risk_score}/100)")

        if risk_level == "HIGH":
            log_warning(f"HIGH fraud risk — invoice flagged: {data.get('invoice_number')}")
            return

        # Validate
        is_valid, messages = validate_invoice(data)

        if is_valid:
            saved = save_invoice(data)
            if saved:
                log_info(f"Auto-saved to database: {data.get('invoice_number')}")
                save_to_excel(data)
                log_info(f"Auto-saved to Excel: {data.get('invoice_number')}")
            else:
                log_warning(f"Duplicate skipped: {data.get('invoice_number')}")
        else:
            for msg in messages:
                log_warning(f"Validation failed: {msg}")

    except Exception as e:
        log_error(f"Scheduler error: {str(e)}")

def check_gmail_and_process():
    log_info("⏰ Auto-scheduler: Checking Gmail for new invoices...")
    try:
        files = fetch_invoice_emails()
        if files:
            log_info(f"Auto-scheduler found {len(files)} invoice(s)")
            for file_path in files:
                process_invoice_file(file_path)
        else:
            log_info("Auto-scheduler: No new invoices found")
    except Exception as e:
        log_error(f"Auto-scheduler Gmail error: {str(e)}")

def start_scheduler(interval_minutes=5):
    """Start the auto-scheduler in background thread"""
    init_db()
    log_info(f"⏰ Auto-scheduler started — checking every {interval_minutes} minutes")
    schedule.every(interval_minutes).minutes.do(check_gmail_and_process)

    def run():
        while True:
            schedule.run_pending()
            time.sleep(30)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread

def stop_scheduler():
    schedule.clear()
    log_info("⏰ Auto-scheduler stopped")
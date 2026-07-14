# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime

# Create logs folder
os.makedirs("logs", exist_ok=True)

# Log file name with date
log_file = os.path.join("logs", f"invoice_bot_{datetime.now().strftime('%Y-%m-%d')}.log")

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("InvoiceBot")

def log_info(message):
    logger.info(message)

def log_error(message):
    logger.error(message)

def log_warning(message):
    logger.warning(message)

def get_logs():
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            return f.readlines()
    return []
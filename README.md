# 🤖 AI-Powered Invoice Processing Bot (LLM + RPA)

> Automatically reads, extracts, validates, and processes invoices using Local LLM and RPA — 100% free and offline.

---

## 📌 Overview

A fully automated invoice processing system that combines **Large Language Model (Mistral via Ollama)** and **RPA (Robotic Process Automation)** to eliminate manual invoice data entry.

The bot can:
- Read invoices from **PDF or scanned images**
- **Automatically fetch** invoices from Gmail
- Use **AI to extract** key data (vendor, invoice number, date, total, tax)
- Show **confidence scores** for each extracted field
- **Validate** the data and detect duplicates
- **Auto-fill Excel** like a real robot
- Save everything to a **local SQLite database**
- Show real-time **system logs**

All running **locally on your laptop** — no internet required, no API costs, completely free.

---

## 🎥 Demo

| Upload Invoice | AI Extraction | Gmail Auto-Fetch |
|---|---|---|
| Upload PDF or image | AI extracts all fields with confidence scores | Bot fetches invoices directly from Gmail |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python** | Core programming language |
| **Ollama + Mistral LLM** | Local AI model for invoice understanding |
| **Tesseract OCR** | Converts scanned images to text |
| **pdfplumber** | Extracts text from digital PDFs |
| **SQLite** | Local database for storing invoice data |
| **openpyxl** | RPA — auto-fills Excel with extracted data |
| **Streamlit** | Web dashboard UI |
| **Gmail API** | Auto-fetches invoice attachments from Gmail |
| **Git + GitHub** | Version control |

---

## ✨ Features

- ✅ **PDF & Image Support** — handles both digital and scanned invoices
- ✅ **Local LLM** — runs Mistral AI completely offline
- ✅ **Confidence Scores** — shows how confident AI is for each field
- ✅ **Gmail Auto-Fetch** — automatically pulls invoice attachments from email
- ✅ **Duplicate Detection** — prevents same invoice from being saved twice
- ✅ **Real RPA** — automatically opens and fills Excel
- ✅ **System Logging** — logs every action with timestamps
- ✅ **100% Free** — no paid APIs, no subscriptions, no cloud required

---

## 📁 Project Structure
---

## 🚀 Setup & Installation

### Prerequisites
- Windows 10/11
- Python 3.x
- Ollama installed
- Tesseract OCR installed

### Step 1 — Clone the repository
```bash
git clone https://github.com/vishu567-ai/invoice-bot.git
cd invoice-bot
```

### Step 2 — Install dependencies
```bash
pip install pdfplumber pdf2image pytesseract streamlit ollama openpyxl pyautogui selenium pillow pandas google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 3 — Install Tesseract OCR
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### Step 4 — Install Ollama and pull Mistral
```bash
ollama pull mistral
```

### Step 5 — Setup Gmail API (optional)
- Go to Google Cloud Console
- Enable Gmail API
- Download credentials.json
- Place in project folder

### Step 6 — Run the app
```bash
python -m streamlit run app.py
```

---

## 📊 What Gets Extracted

| Field | Example | Confidence |
|---|---|---|
| Vendor Name | ABC Solutions Pvt. Ltd. | 🟢 95% |
| Invoice Number | INV-2026-001 | 🟢 98% |
| Date | 03-Jul-2026 | 🟢 100% |
| Total Amount | ₹64,900 | 🟢 99% |
| Tax Amount | ₹9,900 | 🟡 75% |

---

## 🔮 Future Work

- 📧 Scheduled email monitoring (auto-check every X minutes)
- 🌍 Multi-language invoice support
- 🔍 AI-based fraud detection
- 🏢 ERP system integration (Tally, QuickBooks)
- ☁️ Cloud deployment for team access
- 📱 Mobile-friendly dashboard

---

## 👨‍💻 Author

**Vishesh Singh**
- GitHub: [@vishu567-ai](https://github.com/vishu567-ai)
- LinkedIn: [Vishesh Singh](https://www.linkedin.com/in/vishesh-singh-aa7542368)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> Built with ❤️ using Python, Mistral LLM, and RPA — running 100% locally for free.
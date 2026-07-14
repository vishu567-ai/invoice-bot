# -*- coding: utf-8 -*-
import ollama
import json

def extract_invoice_data(text):
    prompt = f"""
    You are an invoice data extraction assistant.
    Extract the following fields from the invoice text below and return ONLY a JSON object with no extra text.
    
    Also provide a confidence score (0-100) for each field based on how clearly it appeared in the invoice.

    Fields to extract:
    - vendor (company name)
    - invoice_number
    - date
    - total (numeric value only)
    - tax (numeric value only)

    If any field is not found, use "N/A" for text fields and 0 for numeric fields, with confidence 0.

    Invoice Text:
    {text}

    Return ONLY this JSON format:
    {{
        "vendor": "",
        "vendor_confidence": 0,
        "invoice_number": "",
        "invoice_number_confidence": 0,
        "date": "",
        "date_confidence": 0,
        "total": 0,
        "total_confidence": 0,
        "tax": 0,
        "tax_confidence": 0
    }}
    """

    try:
        response = ollama.chat(
            model='mistral',
            messages=[{'role': 'user', 'content': prompt}]
        )
        result = response['message']['content']
        result = result.strip()
        if "```" in result:
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        data = json.loads(result)
        return data
    except Exception as e:
        return {
            "vendor": "N/A",
            "vendor_confidence": 0,
            "invoice_number": "N/A",
            "invoice_number_confidence": 0,
            "date": "N/A",
            "date_confidence": 0,
            "total": 0,
            "total_confidence": 0,
            "tax": 0,
            "tax_confidence": 0,
            "error": str(e)
        }
# -*- coding: utf-8 -*-
import ollama
import json

def extract_invoice_data(text):
    prompt = f"""
    You are an invoice data extraction assistant.
    Extract the following fields from the invoice text below and return ONLY a JSON object with no extra text:
    - vendor (company name)
    - invoice_number
    - date
    - total (numeric value only)
    - tax (numeric value only)

    If any field is not found, use "N/A" for text fields and 0 for numeric fields.

    Invoice Text:
    {text}

    Return ONLY this JSON format:
    {{
        "vendor": "",
        "invoice_number": "",
        "date": "",
        "total": 0,
        "tax": 0
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
            "invoice_number": "N/A",
            "date": "N/A",
            "total": 0,
            "tax": 0,
            "error": str(e)
        }
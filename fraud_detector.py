# -*- coding: utf-8 -*-
import sqlite3
import os

def get_vendor_history(vendor_name):
    """Get historical invoice data for a vendor"""
    conn = sqlite3.connect("invoice_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT total, tax, invoice_number FROM invoices 
        WHERE vendor = ? ORDER BY id DESC LIMIT 10
    """, (vendor_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def detect_fraud(data):
    """
    Analyze invoice data and return fraud risk score and reasons
    Returns: (risk_level, risk_score, reasons)
    risk_level: "LOW", "MEDIUM", "HIGH"
    risk_score: 0-100
    reasons: list of suspicious findings
    """
    reasons = []
    risk_score = 0

    vendor = data.get('vendor', 'N/A')
    total = float(data.get('total', 0))
    tax = float(data.get('tax', 0))
    invoice_number = data.get('invoice_number', 'N/A')

    # Check 1: Round number detection
    if total > 0 and total % 1000 == 0:
        reasons.append(f"⚠️ Suspiciously round total amount: {total}")
        risk_score += 15

    # Check 2: Zero or missing tax on large amounts
    if total > 10000 and tax == 0:
        reasons.append(f"⚠️ No tax on large invoice amount: {total}")
        risk_score += 20

    # Check 3: Tax ratio check
    if total > 0 and tax > 0:
        tax_ratio = (tax / total) * 100
        if tax_ratio > 30:
            reasons.append(f"⚠️ Unusually high tax ratio: {tax_ratio:.1f}%")
            risk_score += 25
        elif tax_ratio < 1:
            reasons.append(f"⚠️ Unusually low tax ratio: {tax_ratio:.1f}%")
            risk_score += 10

    # Check 4: Compare with vendor history
    history = get_vendor_history(vendor)
    if history:
        historical_totals = [h[0] for h in history]
        avg_total = sum(historical_totals) / len(historical_totals)
        max_total = max(historical_totals)

        # If current invoice is 3x more than average
        if total > avg_total * 3:
            reasons.append(f"⚠️ Amount {total} is {total/avg_total:.1f}x higher than vendor average ({avg_total:.0f})")
            risk_score += 35

        # If current invoice is 2x more than highest ever
        if total > max_total * 2:
            reasons.append(f"⚠️ Amount {total} is much higher than vendor's previous maximum ({max_total:.0f})")
            risk_score += 25

    else:
        # New vendor with high amount
        if total > 50000:
            reasons.append(f"⚠️ New vendor '{vendor}' with high invoice amount: {total}")
            risk_score += 20

    # Check 5: Extremely high amount
    if total > 500000:
        reasons.append(f"⚠️ Extremely high invoice amount: {total}")
        risk_score += 30

    # Check 6: Invoice number pattern check
    if invoice_number != 'N/A':
        if not any(char.isdigit() for char in invoice_number):
            reasons.append(f"⚠️ Invoice number has no digits: {invoice_number}")
            risk_score += 10

    # Cap risk score at 100
    risk_score = min(risk_score, 100)

    # Determine risk level
    if risk_score >= 60:
        risk_level = "HIGH"
    elif risk_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return risk_level, risk_score, reasons
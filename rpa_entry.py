# -*- coding: utf-8 -*-
import openpyxl
import os
import time

def save_to_excel(data):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "invoice_records.xlsx")

    if os.path.exists(file_path):
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
    else:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Invoices"
        headers = ["Vendor", "Invoice Number", "Date", "Total", "Tax", "Status"]
        sheet.append(headers)

    row = [
        data['vendor'],
        data['invoice_number'],
        data['date'],
        data['total'],
        data['tax'],
        'Processed'
    ]
    sheet.append(row)
    workbook.save(file_path)

    try:
        os.startfile(file_path)
        time.sleep(3)
    except Exception as e:
        print(f"Could not open Excel: {e}")

    return True
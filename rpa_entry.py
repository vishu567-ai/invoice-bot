# -*- coding: utf-8 -*-
import openpyxl
import os

def save_to_excel(data):
    file_path = "invoice_records.xlsx"
    
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
    return True
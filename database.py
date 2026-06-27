# -*- coding: utf-8 -*-
import sqlite3

def init_db():
    conn = sqlite3.connect("invoice_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor TEXT,
            invoice_number TEXT UNIQUE,
            date TEXT,
            total REAL,
            tax REAL,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_invoice(data):
    conn = sqlite3.connect("invoice_data.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO invoices (vendor, invoice_number, date, total, tax, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['vendor'], data['invoice_number'], data['date'], data['total'], data['tax'], 'processed'))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_invoices():
    conn = sqlite3.connect("invoice_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices")
    rows = cursor.fetchall()
    conn.close()
    return rows
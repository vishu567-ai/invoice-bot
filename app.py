# -*- coding: utf-8 -*-
import streamlit as st
from ocr_reader import extract_text_from_pdf, extract_text_from_image
from llm_extractor import extract_invoice_data
from validator import validate_invoice
from database import init_db, save_invoice, get_all_invoices
from rpa_entry import save_to_excel
import os

init_db()

st.title("AI-Powered Invoice Processing Bot")
st.subheader("LLM + RPA | Local Prototype")

uploaded_file = st.file_uploader("Upload Invoice (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    file_path = os.path.join("invoices", uploaded_file.name)
    os.makedirs("invoices", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File uploaded: {uploaded_file.name}")

    if st.button("Process Invoice"):
        with st.spinner("Reading invoice..."):
            if uploaded_file.type == "application/pdf":
                text = extract_text_from_pdf(file_path)
            else:
                text = extract_text_from_image(file_path)

        st.subheader("Extracted Text")
        st.text_area("Raw Text", text, height=150)

        with st.spinner("AI is extracting data..."):
            data = extract_invoice_data(text)

        st.subheader("AI Extracted Data")
        st.json(data)

        is_valid, messages = validate_invoice(data)

        if is_valid:
            st.success("Invoice is Valid!")
            saved = save_invoice(data)
            if saved:
                st.success("Saved to Database!")
            else:
                st.warning("Duplicate Invoice - Already exists in database!")
            save_to_excel(data)
            st.success("Data saved to Excel!")
        else:
            st.error("Invoice Validation Failed!")
            for msg in messages:
                st.warning(msg)

st.subheader("All Processed Invoices")
invoices = get_all_invoices()
if invoices:
    st.table(invoices)
else:
    st.info("No invoices processed yet.")
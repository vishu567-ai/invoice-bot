def validate_invoice(data):
    errors = []

    # Check required fields
    if data['vendor'] == "N/A" or data['vendor'] == "":
        errors.append("Vendor name is missing")

    if data['invoice_number'] == "N/A" or data['invoice_number'] == "":
        errors.append("Invoice number is missing")

    if data['date'] == "N/A" or data['date'] == "":
        errors.append("Date is missing")

    if data['total'] == 0:
        errors.append("Total amount is missing or zero")

    # Check if total and tax are valid numbers
    try:
        float(data['total'])
        float(data['tax'])
    except:
        errors.append("Total or tax is not a valid number")

    if errors:
        return False, errors
    else:
        return True, ["Invoice is valid"]
from flask import Flask, request, render_template, make_response
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-bill', methods=['POST'])
def generate_bill():
    # Get customer details
    customer_name = request.form['customer_name']
    customer_address = request.form['customer_address']
    customer_contact = request.form['customer_contact']

    # Get Item details
    product_names = request.form.getlist('product_name[]')
    quantities = request.form.getlist('quantity[]')
    prices = request.form.getlist('price[]')

    # Calculate totals
    items = []
    subtotal = 0
    for name, qty, price in zip(product_names, quantities, prices):
        total_price = int(qty) * float(price)
        subtotal += total_price
        items.append([name, qty, price, f"{total_price:.2f}"])

    tax = round(subtotal * 0.1, 2)  # Example: 10% tax, rounded to 2 decimal places
    grand_total = subtotal + tax

    # Create PDF in memory
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Add Customer Details
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 750, "Customer Details")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 730, f"Name: {customer_name}")
    pdf.drawString(50, 710, f"Address: {customer_address}")
    pdf.drawString(50, 690, f"Contact: {customer_contact}")

    # Add Table Header
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, 650, "Items Purchased")
    table_data = [["Product Name", "Quantity", "Price", "Total Price"]] + items

    # Add Totals Row
    table_data.append(["", "", "Subtotal", f"{subtotal:.2f}"])
    table_data.append(["", "", "Tax (10%)", f"{tax:.2f}"])
    table_data.append(["", "", "Grand Total", f"{grand_total:.2f}"])

    # Create Table
    table = Table(table_data, colWidths=[150, 100, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))

    # Add Table to PDF
    table.wrapOn(pdf, 50, 400)
    table.drawOn(pdf, 50, 400)

    # Save and return PDF
    pdf.save()
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename="bill_{customer_name}.pdf"'
    return response

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template, make_response
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
import numpy as np
import random

app = Flask(__name__)

# Register DejaVu Sans Font for ₹ support
pdfmetrics.registerFont(TTFont('DejaVuSans', 'fonts/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'fonts/dejavu-sans-bold.ttf'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-bill', methods=['POST'])
def generate_bill():
    try:
        # Store Details
        store_name = "SuperMart"
        store_address = "123 Main Street, Cityville"
        store_contact = "Phone : +91 9876543210"
        store_email = "Email : contact@support.com"

        # Generate Invoice Number
        invoice_number = f"INV-{random.randint(1000, 9999)}"

        # Get customer details
        customer_name = request.form['customer_name']
        customer_contact = request.form['customer_contact']
        customer_address = request.form.get('customer_address', "N/A")

        # Get item details
        product_names = request.form.getlist('product_name[]')
        quantities = [int(qty) for qty in request.form.getlist('quantity[]')]
        prices = [float(price) for price in request.form.getlist('price[]')]

        # Validate inputs
        if not product_names or not quantities or not prices:
            return "Please provide complete product details.", 400

        # NumPy calculations
        quantities_np = np.array(quantities)
        prices_np = np.array(prices)
        total_prices_np = quantities_np * prices_np
        subtotal = np.sum(total_prices_np)
        tax = round(subtotal * 0.1, 2)  # 10% tax
        grand_total = round(subtotal + tax, 2)

        # Create item data
        items = [[name, qty, f"₹{price:.2f}", f"₹{total:.2f}"]
                 for name, qty, price, total in zip(product_names, quantities, prices, total_prices_np)]

        # Add column headers
        table_data = [["Product Name", "Quantity", "Unit Price", "Total Price"]] + items

        # Add totals
        table_data.append(["", "", "Subtotal", f"₹{subtotal:.2f}"])
        table_data.append(["", "", "Tax (10%)", f"₹{tax:.2f}"])
        table_data.append(["", "", "Grand Total", f"₹{grand_total:.2f}"])

        # Create PDF in memory
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)

        # Set the custom font
        pdf.setFont("DejaVuSans", 12)

        # Header: Store Details
        pdf.setFont("DejaVuSans-Bold", 18)
        pdf.drawString(50, 750, store_name)
        pdf.setFont("DejaVuSans", 12)
        pdf.drawString(50, 735, store_address)
        pdf.drawString(50, 720, store_contact)
        pdf.drawString(50, 705, store_email)

        # Add a gap (leave blank space)
        gap_start = 685  # Start position after store details
        gap_height = 20   # Height of the gap
        pdf.drawString(50, gap_start - gap_height, "")  # Ensures space between sections

        # Customer Details
        pdf.setFont("DejaVuSans-Bold", 14)
        pdf.drawString(50, gap_start - gap_height - 20, "Customer Details")
        pdf.setFont("DejaVuSans", 12)
        pdf.drawString(50, gap_start - gap_height - 35, f"Name: {customer_name}")
        pdf.drawString(50, gap_start - gap_height - 50, f"Contact: {customer_contact}")
        pdf.drawString(50, gap_start - gap_height - 65, f"Address: {customer_address}")

        # Add Table
        pdf.setFont("DejaVuSans-Bold", 14)
        pdf.drawString(50, gap_start - gap_height, "Items Purchased")
        table = Table(table_data, colWidths=[200, 80, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))
        table.wrapOn(pdf, 50, 400)
        table.drawOn(pdf, 50, 400)

        # Footer: Thank You Message
        pdf.setFont("DejaVuSans", 10)
        pdf.drawString(50, 50, "Thank you for shopping with us!")
        pdf.drawString(50, 35, "Visit us again at SuperMart.")

        # Save and return PDF
        pdf.save()
        buffer.seek(0)

        response = make_response(buffer.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename="bill_{invoice_number}.pdf"'  # Change to "attachment" for download
        return response

    except ValueError:
        return "Invalid input: Please ensure quantities and prices are numeric values.", 400
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
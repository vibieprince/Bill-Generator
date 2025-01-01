from flask import Flask,request,render_template,make_response
from weasyprint import HTML
import io
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-bill',methods=['POST'])
def generate_bill():
    # Get customer details
    customer_name = request.form['customer_name']
    customer_address = request.form['customer_address']
    customer_contact = request.form['customer_contact']

    # Get Item details
    product_names = request.form.getlist('product_name[]')
    quantities = request.form.getlist('quantity[]')
    prices = request.form.getlist('price[]')

    #Calculate totals
    items = []
    subtotal = 0
    for name,qty,price in zip(product_names,quantities,prices):
        total_price = int(qty)*float(price)
        subtotal += total_price
        items.append({'name':name,'quantity':qty,'price':price,'total_price':total_price})
    tax = round(subtotal*0.1,2) #Example:10% tax,rounded to 2 decimal places
    grand_total = subtotal+tax

    # Render the HTML bill 
    # Pass data to the template for rendering
    html = render_template('bill.html',customer_name=customer_name,customer_address=customer_address,customer_contact=customer_contact,items=items,subtotal=subtotal,tax=tax,grand_total=grand_total)

    # Generate PDF
    pdf = HTML(string=html).write_pdf()

    # Serve PDF as a response 
    response = make_response(pdf)
    response.headers['Content-Disposition'] = f'inline;
    filename = bill_{customer_name}.pdf'

    return response



if __name__ == '__main__':
    app.run(debug=True)
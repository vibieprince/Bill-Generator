from flask import Flask,request,render_template
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
    tax = subtotal*0.1 #Example:10% tax
    grand_total = subtotal+tax

    # Pass data to the template for rendering
    return render_template('bill.html',customer_name=customer_name,customer_address=customer_address,customer_contact=customer_contact,items=items,subtotal=subtotal,tax=tax,grand_total=grand_total)

if __name__ == '__main__':
    app.run(debug=True)
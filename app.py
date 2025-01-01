from flask import Flask,request,render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit',methods=['POST'])
def submit():
    customer_name = request.form['customer_name']
    return f"Hello,{customer_name}! Your bill will be generated soon."

if __name__ == '__main__':
    app.run(debug=True)
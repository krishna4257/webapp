from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = '220021'

@app.route("/")
def login():
    return render_template('index.html')
@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']

    valid_username = "user"
    valid_password = "pass"

    if username == valid_username and password == valid_password:
        flash("Login successful!", "success")
        return redirect(url_for('intermediate'))
    else:
        flash("Invalid username or password.", "danger")
        return redirect(url_for('login'))

# Route for intermediate page
@app.route('/intermediate')
def intermediate():
    return render_template('intermediate.html')

@app.route('/goto_posting')
def goto_posting():
    return redirect(url_for('posting'))

@app.route('/goto_customer')
def goto_customer():
    return redirect(url_for('customer'))

# Route for posting form
@app.route('/posting', methods=['GET', 'POST'])
def posting():
    if request.method == 'POST':
        customer_id = request.form['customerId']
        posting_date = request.form['postingDate']
        amount = request.form['amount']
        
        # Log data for demonstration
        app.logger.info({
            'customerId': customer_id,
            'postingDate': posting_date,
            'amount': amount
        })
        
        flash("Customer data saved successfully!", "success")
        return redirect(url_for('posting'))
    return render_template('posting.html')

# Route for customer form
@app.route('/customer', methods=['GET', 'POST'])
def customer():
    if request.method == 'POST':
        customer_id = request.form['customerId']
        customer_name = request.form['customerName']
        customer_date = request.form['customerDate']
        customer_address = request.form['customerAddress']
        amount = request.form['amount']
        options = request.form['options']

        # Log data for demonstration
        app.logger.info({
            'customerId': customer_id,
            'customerName': customer_name,
            'customerDate': customer_date,
            'customerAddress': customer_address,
            'amount': amount,
            'options': options
        })

        flash("Customer data saved successfully!", "success")
        return redirect(url_for('customer'))
    return render_template('customer.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
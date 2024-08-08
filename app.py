from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import pypyodbc as odbc
import pandas as pd
from datetime import datetime
import mysql.connector

app = Flask(__name__)
app.secret_key = '220021'

@app.route("/")
def login():
    return render_template('index.html')
@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']

    valid_username = "jay"
    valid_password = "login"

    if username == valid_username and password == valid_password:
        flash("Login successful!", "success")
        return redirect(url_for('intermediate'))
    else:
        flash("Invalid username or password.", "danger")
        return redirect(url_for('login'))

# Routejay for intermediate page
@app.route('/intermediate')
def intermediate():
    return render_template('intermediate.html')

@app.route('/index')
def goto_index():
    return render_template('index.html')

@app.route('/goto_posting')
def goto_posting():
    return redirect(url_for('posting'))

@app.route('/goto_data')
def goto_data():
    return redirect(url_for('data'))

@app.route('/goto_customer')
def goto_customer():
    return redirect(url_for('customer'))

# Route for posting form
@app.route('/posting', methods=['GET', 'POST'])
def posting():
    return render_template('posting.html')

@app.route('/submitpost', methods=['POST'])
def submitpost():
    # Connect to the database
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:finanacedata.database.windows.net,1433;Database=findata;Uid=jaya;Pwd={Krishna@2244};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    if request.method == 'POST':
        customer_id = request.form.get('customerId')
        posting_date = request.form.get('postingDate')
        postingdate = datetime.strptime(posting_date, '%Y-%m-%d').date()
        amount = request.form.get('amount')
        
    cursor.execute("INSERT INTO POSTING (customerId, date, amount) VALUES (?, ?, ?)", (customer_id, postingdate, amount))

    conn.commit()
    cursor.close()
    conn.close()   
    return redirect(url_for('posting'))

db_config = {
    'user' : 'jaya',
    'password' : 'Krishna@2244',
    'host' : 'finanacedata.database.windows.net',
    'database' : 'findata'
}



# Route for customer form
@app.route('/customer', methods=['GET', 'POST'])
def customer():
    return render_template('customer.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Connect to the database
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:finanacedata.database.windows.net,1433;Database=findata;Uid=jaya;Pwd={Krishna@2244};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()

    if request.method == 'POST':
        customer_id = request.form.get('customerId')
        customer_name = request.form.get('customerName')
        customer_address = request.form.get('customerAddress')
        term = request.form.get('term')
        fromDate = request.form.get('fromDate')
        fromdate = datetime.strptime(fromDate, '%Y-%m-%d').date()
        toDate = request.form.get('toDate')
        todate = datetime.strptime(toDate, '%Y-%m-%d').date()
        amount = request.form.get('amount')
        intrest = request.form.get('intrest')
        installmentAmount = request.form.get('installmentAmount')
        totalPaid = request.form.get('totalPaid')
        totalBalance = request.form.get('totalBalance')


    # Insert data into the table
    cursor.execute("INSERT INTO CUSTOMERS (customerId, customerName, customerAddress, term, fromDate, toDate, amount, interest, installmentAmount, totalPaid, totalBalance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (customer_id, customer_name, customer_address, term, fromdate, todate, amount, intrest, installmentAmount, totalPaid, totalBalance))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/customer')

@app.route('/data', methods=['GET', 'POST'])
def data():
     # Connect to the database
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:finanacedata.database.windows.net,1433;Database=findata;Uid=jaya;Pwd={Krishna@2244};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()

    # Fetch data from the table
    cursor.execute("SELECT * FROM customers")
    customers_data = cursor.fetchall()

    cursor.execute("SELECT * FROM posting")
    postings_data = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    return render_template('data.html', customers=customers_data, postings=postings_data)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
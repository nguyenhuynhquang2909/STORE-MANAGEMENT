from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt,generate_password_hash,check_password_hash
from werkzeug.security import check_password_hash

import sqlite3

TEMPLATE_AUTO_RELOAD = True 
app = Flask(__name__)
app.secret_key = 'supersecretkey'
bcrypt = Bcrypt(app)

@app.route('/')     
def home():
    return render_template('home.html')

@app.route('/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        storename = request.form['storename']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']

    # Hash the password 

        conn = sqlite3.connect('account.db')
        cur = conn.cursor()
        try: 
            conn.execute('INSERT INTO account(storename, email, password) VALUES (?,?,?)', (storename, email, password))
            conn.commit()
            conn.close()
        except sqlite3.Error as error: 
            print("Failed to insert data into SQLite table:", error)
            conn.rollback()
            conn.close()
            flash('Registration failed. Please try again later', 'danger')
            return redirect(url_for('register'))
        print("storename: ", storename)
        print("email: ", email)
        print("password: ", password)

        flash('Registration successful. Please login to continue', 'success')
        return redirect(url_for('home')) 
    else:
        return render_template('register.html')  
        

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('account.db')
        cur = conn.cursor()
        cur.execute('SELECT email, password FROM account WHERE email = ? AND password = ?', (email, password,))
        account = cur.fetchall()
        if account:
            session['id'] = account[0]
            flash('Login successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect email or password', 'danger')
    return render_template('login.html')

@app.route('/logout/')
def logout():
    session.pop('storename', None)
    flash('You have been logout', 'info')
    return redirect('/login')   

@app.route('/')
def index():
    conn = sqlite3.connect('store.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory")
    inventory = cur.fetchall()
    conn.close()
    return render_template('home.html')

@app.route('/add/', methods = ['POST', 'GET'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        conn = sqlite3.connect('store.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO inventory (name, category, price, quantity) VALUES (?,?,?,?)", (name, category, price, quantity))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    else:
        return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session, Bcrypt
from flask_bcrypt import check_password_hash
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return redirect(url_for('login'))
@app.route('/register/', methods = ['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        storename = request.form['storename']
        password = request.form['password']
        email = request.form['email']

    # Hash the password 
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = sqlite3.connect('account.db')
        cur = conn.cursor()
        conn.execute('INSERT INTO account(storename, email, password) VALUES (?,?,?)', (storename, email, hashed_password))
        conn.commit()
        session['id'] = cur.lastrowid
        session['storename'] = storename
        return redirect('/')
    return render_template('register.html')

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('account.db')
        cur = conn.cursor()
        conn.execute('SELECT * FROM account WHERE LOWER(email) = ? AND password = ?', (email.lower(), password))
        account = cur.fetchone()
        if account and check_password_hash(account[2], password):
            session['id'] = account[0]
            session['storename'] = account[1]
            return redirect('/')
        else:
            return render_template('login.html', error='Wrong email or password')
    return render_template('login.html')


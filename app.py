from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import secrets  # Add this import

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generates a random 32-character hex string

# Temporary storage (replace with database later)
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users and users[email]['password'] == password:
            session['user'] = email
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid email or password')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        firstname = request.form.get('firstname')
        secondname = request.form.get('secondname')
        lastname = request.form.get('lastname')
        secondlastname = request.form.get('secondlastname')
        email = request.form.get('email')
        password = request.form.get('password')
        birthdate = request.form.get('birthdate')
        country = request.form.get('country')
        
        # Basic validation
        if not all([firstname, lastname, email, password, birthdate, country]):
            return render_template('signup.html', error='Please fill in all required fields')
        
        if email in users:
            return render_template('signup.html', error='Email already registered')
        
        # Store user data (temporarily)
        users[email] = {
            'firstname': firstname,
            'secondname': secondname,
            'lastname': lastname,
            'secondlastname': secondlastname,
            'password': password,
            'birthdate': birthdate,
            'country': country
        }
        
        # Log the user in
        session['user'] = email
        return redirect(url_for('index'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
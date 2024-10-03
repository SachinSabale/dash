from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

# Create a Blueprint for user management
user_management_blueprint = Blueprint('user_management', __name__, template_folder='templates')

# MySQL instance (initialize in main app)
mysql = MySQL()

# Route to display all user messages
@user_management_blueprint.route('/user_messages')
def user_messages():
    if 'user' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('home'))

    # Fetch all user messages from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_messages")
    messages = cur.fetchall()
    cur.close()

    return render_template('user_messages.html', messages=messages)

# Route to delete a user message
@user_management_blueprint.route('/delete_message/<int:message_id>')
def delete_message(message_id):
    if 'user' not in session:
        return redirect(url_for('home'))

    # Delete the message from the database
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM user_messages WHERE message_id = %s", (message_id,))
    mysql.connection.commit()
    cur.close()

    flash('Message deleted successfully!', 'success')
    return redirect(url_for('user_management.user_messages'))

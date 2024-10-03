from flask import Blueprint, render_template, request, redirect, url_for, flash

messages_bp = Blueprint('messages', __name__)

# Initialize MySQL instance
mysql = None

# This function will initialize the blueprint with the MySQL instance
def init_app(mysql_instance):
    global mysql
    mysql = mysql_instance

# Define the route for the messages page
@messages_bp.route('/', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        message = request.form['message']

        # Insert the message into the database
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user_messages(name, contact_number, email, message) VALUES (%s, %s, %s, %s)", 
                        (name, contact_number, email, message))
            mysql.connection.commit()
            cur.close()
            flash('Message sent successfully!', 'success')
            return redirect(url_for('messages.messages'))
        except Exception as e:
            flash('An error occurred while sending the message.', 'danger')
            return redirect(url_for('messages.messages'))

    # Fetch messages from the database to display
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_messages")
    messages_list = cur.fetchall()
    cur.close()
    
    return render_template('messages.html', messages=messages_list)

@messages_bp.route('/delete_message/<int:message_id>')
def delete_message(message_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM user_messages WHERE id = %s", (message_id,))
        mysql.connection.commit()
        cur.close()
        flash('Message deleted successfully!', 'success')
    except Exception as e:
        flash('An error occurred while deleting the message.', 'danger')
    return redirect(url_for('messages.messages'))

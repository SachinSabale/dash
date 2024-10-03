from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

# Create a Blueprint for event-related routes
events_blueprint = Blueprint('events', __name__, template_folder='templates')

# MySQL instance (initialize in main app)
mysql = MySQL()

# Route to display all events
@events_blueprint.route('/events')
def events():
    if 'user' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('home'))

    # Fetch all events from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events")
    event_data = cur.fetchall()
    cur.close()

    return render_template('events.html', events=event_data)

# Route to add a new event
@events_blueprint.route('/add_event', methods=['POST'])
def add_event():
    if 'user' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        title = request.form['event_title']
        date_time = request.form['event_datetime']  # Field name corrected
        description = request.form['event_description']  # Field name corrected

        # Insert new event into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO events (event_title, event_datetime, event_description) VALUES (%s, %s, %s)", 
                    (title, date_time, description))
        mysql.connection.commit()
        cur.close()

        flash('Event added successfully!', 'success')
        return redirect(url_for('events.events'))

# Route to delete an event
@events_blueprint.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    if 'user' not in session:
        return redirect(url_for('home'))

    # Delete the event from the database
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM events WHERE event_id = %s", (event_id,))  # Field name corrected
    mysql.connection.commit()
    cur.close()

    flash('Event deleted successfully!', 'success')
    return redirect(url_for('events.events'))

# Route to edit an event
@events_blueprint.route('/edit_event/<int:event_id>', methods=['POST', 'GET'])
def edit_event(event_id):
    if 'user' not in session:
        return redirect(url_for('home'))

    # Fetch event details to pre-populate the form for editing
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))  # Field name corrected
    event = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        title = request.form['event_title']
        date_time = request.form['event_datetime']  # Field name corrected
        description = request.form['event_description']  # Field name corrected

        # Update the event details in the database
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE events
            SET event_title = %s, event_datetime = %s, event_description = %s
            WHERE event_id = %s
        """, (title, date_time, description, event_id))  # Field name corrected
        mysql.connection.commit()
        cur.close()

        flash('Event updated successfully!', 'success')
        return redirect(url_for('events.events'))

    return render_template('edit_event.html', event=event)

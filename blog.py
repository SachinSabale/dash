from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

# Create a Blueprint for blog-related routes
blogs_blueprint = Blueprint('blogs', __name__, template_folder='templates')

# MySQL instance (initialize in main app)
mysql = MySQL()

# Route to display all popular blogs
@blogs_blueprint.route('/')
def blogs():
    if 'user' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('home'))

    # Fetch all popular blogs from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM popular_blogs")
    blog_data = cur.fetchall()
    cur.close()

    return render_template('blogs.html', blogs=blog_data)

# Route to add a new blog
@blogs_blueprint.route('/add_blog', methods=['POST'])
def add_blog():
    if 'user' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        title = request.form['blog_title']
        date = request.form['blog_date']
        description = request.form['blog_description']
        link = request.form['blog_link']  # Add the blog link

        # Insert new blog into the popular_blogs table
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO popular_blogs (blog_title, blog_date, blog_description, blog_link) VALUES (%s, %s, %s, %s)", 
                    (title, date, description, link))
        mysql.connection.commit()
        cur.close()

        flash('Blog added successfully!', 'success')
        return redirect(url_for('blogs.blogs'))

# Route to delete a blog
@blogs_blueprint.route('/delete_blog/<int:blog_id>')
def delete_blog(blog_id):
    if 'user' not in session:
        return redirect(url_for('home'))

    # Delete the blog from the popular_blogs table
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM popular_blogs WHERE blog_id = %s", (blog_id,))
    mysql.connection.commit()
    cur.close()

    flash('Blog deleted successfully!', 'success')
    return redirect(url_for('blogs.blogs'))

# Route to edit a blog
@blogs_blueprint.route('/edit_blog/<int:blog_id>', methods=['POST', 'GET'])
def edit_blog(blog_id):
    if 'user' not in session:
        return redirect(url_for('home'))

    # Fetch blog details to pre-populate the form for editing
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM popular_blogs WHERE blog_id = %s", (blog_id,))
    blog = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        title = request.form['blog_title']
        date = request.form['blog_date']
        description = request.form['blog_description']
        link = request.form['blog_link']  # Add the blog link

        # Update the blog details in the popular_blogs table
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE popular_blogs
            SET blog_title = %s, blog_date = %s, blog_description = %s, blog_link = %s
            WHERE blog_id = %s
        """, (title, date, description, link, blog_id))
        mysql.connection.commit()
        cur.close()

        flash('Blog updated successfully!', 'success')
        return redirect(url_for('blogs.blogs'))

    return render_template('edit_blog.html', blog=blog)

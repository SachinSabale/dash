from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os

publications_blueprint = Blueprint('publications', __name__)
mysql = MySQL()

# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
PDF_FOLDER = os.path.join(UPLOAD_FOLDER, 'pdfs')
COVER_FOLDER = os.path.join(UPLOAD_FOLDER, 'covers')

# Ensure upload folders exist
os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(COVER_FOLDER, exist_ok=True)

# Route to list all publications
@publications_blueprint.route('/')
def list_publications():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM publications")
    publications = cur.fetchall()
    cur.close()
    return render_template('publications.html', publications=publications)

# Route to add a publication
@publications_blueprint.route('/add', methods=['GET', 'POST'])
def add_publication():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        file = request.files['pdf_file']
        cover = request.files['cover_image']

        if file and cover:
            # Save PDF file
            pdf_filename = file.filename
            file.save(os.path.join(PDF_FOLDER, pdf_filename))
            
            # Save cover image
            cover_filename = cover.filename
            cover.save(os.path.join(COVER_FOLDER, cover_filename))

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO publications (title, author, pdf_file, cover_image) VALUES (%s, %s, %s, %s)",
                        (title, author, pdf_filename, cover_filename))
            mysql.connection.commit()
            cur.close()

            flash('Publication added successfully!', 'success')
            return redirect(url_for('publications.list_publications'))

    return render_template('add_publication.html')

# Route to edit a publication
@publications_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_publication(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM publications WHERE id = %s", (id,))
    publication = cur.fetchone()
    
    if request.method == 'POST':
        title = request.form['book_title']
        author = request.form['author']
        file = request.files['pdf_file']
        cover = request.files['cover_image']

        pdf_filename = publication[3]  # existing PDF filename
        cover_filename = publication[4]  # existing cover image filename

        if file:
            # Save new PDF file
            pdf_filename = file.filename
            file.save(os.path.join(PDF_FOLDER, pdf_filename))
        
        if cover:
            # Save new cover image
            cover_filename = cover.filename
            cover.save(os.path.join(COVER_FOLDER, cover_filename))

        cur.execute("UPDATE publications SET title = %s, author = %s, pdf_file = %s, cover_image = %s WHERE id = %s",
                    (title, author, pdf_filename, cover_filename, id))
        mysql.connection.commit()
        cur.close()

        flash('Publication updated successfully!', 'success')
        return redirect(url_for('publications.list_publications'))

    return render_template('edit_publication.html', publication=publication)

# Route to delete a publication
@publications_blueprint.route('/delete/<int:id>', methods=['POST'])
def delete_publication(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM publications WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Publication deleted successfully!', 'success')
    return redirect(url_for('publications.list_publications'))

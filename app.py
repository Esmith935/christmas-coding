# imports
from flask import Flask, render_template, redirect, url_for, request, flash
import sqlite3
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = '987dg239476fgywiuen'

DATABASE = 'database.db'

DOC_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = DOC_FOLDER
os.makedirs(DOC_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# -- Initialise Database

def init_db():
    with sqlite3.connect(DATABASE) as conn:

        conn.execute('''
            CREATE TABLE IF NOT EXISTS gifts (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     price REAL NOT NULL,
                     image TEXT NOT NULL
                     )
            ''')
        conn.commit()

# ------------------------------------------ #

# -- Route: Index

@app.route('/')
def index():

    return render_template('index.html')

# -- Route: Age Checker

@app.route('/agechecker', methods=["GET", "POST"])
def agechecker():
    result = None
    if request.method == "POST":
        age = request.form.get("age")
        try:
            age = int(age)
            if age < 0:
                result = "Please enter a valid age."
            elif age < 18:
                result = "You are a sweatshop worker."
            else:
                result = "You are a Santa's Helper."
        except ValueError:
            result = "Please enter a valid number."

        return render_template('agechecker.html', result=result)
    return render_template('agechecker.html')

# -- Route: Gift List

@app.route('/gift_list')
def gift_list():

    with sqlite3.connect(DATABASE) as conn:
        gifts = conn.execute('SELECT * FROM gifts').fetchall()

    return render_template('gift_list.html', gifts=gifts)

# -- Route: Add Gift

@app.route('/add_gift', methods=['GET', 'POST'])
def add_gift():

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.files.get('image')
        image_filename = None

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_filename = f"{name}_{filename}"
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        with sqlite3.connect(DATABASE) as conn:
            conn.execute('INSERT INTO gifts (name, price, image) VALUES (?, ?, ?)', (name, price, image_filename))
            conn.commit()

        return redirect(url_for('gift_list'))

    return render_template('add_gift.html')

@app.route('/countdown')
def countdown():
    return render_template('countdown.html')

if __name__ == '__main__':
    init_db()
    app.run(debug = True)
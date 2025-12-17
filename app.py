# imports
from flask import Flask, render_template, redirect, url_for, request, flash
import sqlite3
import os 


app = Flask(__name__)
app.secret_key = '987dg239476fgywiuen'

DATABASE = 'database.db'

DOC_FOLDER = os.path.join('images')
app.config['UPLOAD_FOLDER'] = DOC_FOLDER

# -- Initialise Database

def init_db():
    with sqlite3.connect(DATABASE) as conn:

        conn.execute('''
            CREATE TABLE IF NOT EXISTS gifts (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     price REAL NOT NULL,
                     image TEXT
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
def gift_lift():

    with sqlite3.connect(DATABASE) as conn:
        gifts = conn.execute('SELECT * FROM gifts').fetchall()

    return render_template('gift_list.html', gifts=gifts)

@app.route('/countdown')
def countdown():
    return render_template('countdown.html')

if __name__ == '__main__':
    init_db()
    app.run(debug = True)
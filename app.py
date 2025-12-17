# imports
from flask import Flask, render_template, redirect, url_for
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
    return render_template('agechecker.html')

# -- Route: Gift List

@app.route('/gift_list')
def gift_lift():

    return render_template('gift_list.html')
    

if __name__ == '__main__':
    app.run(debug = True)
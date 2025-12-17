# imports
from flask import Flask, render_template
import os 


app = Flask(__name__)

# -- Route: Index

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/agechecker', methods=["GET", "POST"])
def agechecker():
    return render_template('agechecker.html')


if __name__ == '__main__':
    app.run(debug = True)
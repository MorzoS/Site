from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy

SHARED_TEMPLATE_FOLDER = "wikiflex/beeld/sh_templates"
SHARED_STATIC_FOLDER = "wikiflex/beeld/sh_static"

app = Flask(__name__, template_folder=SHARED_TEMPLATE_FOLDER, static_folder=SHARED_STATIC_FOLDER)

@app.route('/')
def home():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from wikiflex.beeld.home.__init__ import blueprint

SHARED_TEMPLATE_FOLDER = "wikiflex/beeld/sh_templates"
SHARED_STATIC_FOLDER = "wikiflex/beeld/sh_static"

def page_not_found(e):
	return render_template("404.html"), 404


def general_error(e):
	return render_template("bad_request.html")

app = Flask(__name__, template_folder=SHARED_TEMPLATE_FOLDER, static_folder=SHARED_STATIC_FOLDER)
app.register_blueprint(blueprint, url_prefix="")

@app.route('/')
def basic():
    return render_template('basic.html')

if __name__ == "__main__":
    app.run(debug=True)

#blueprints laden


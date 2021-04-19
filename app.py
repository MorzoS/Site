from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from wikiflix.beeld.home.__init__ import blueprint

import wikiflix

SHARED_TEMPLATE_FOLDER = "wikiflex/beeld/sh_templates"
SHARED_STATIC_FOLDER = "wikiflex/beeld/sh_static"

def pagina_niet_gevonden(e):
	return render_template("404.html"), 404


def general_error(e):
	return render_template("bad_request.html")

def main():
    app = app_aanmaken()
    app.run(debug=True)

def app_aanmaken():
    app = Flask(__name__, template_folder=SHARED_TEMPLATE_FOLDER, static_folder=SHARED_STATIC_FOLDER)
    app.register_error_handler(404, pagina_niet_gevonden)
    app.register_error_handler(HTTPException, general_error)

    #blueprints laden

    app.register_blueprint(blueprint, url_prefix="")

    app.run(debug=True)

    return app

    if __name__ == "__main__":
        app_aanmaken()
        app.run(debug=True)

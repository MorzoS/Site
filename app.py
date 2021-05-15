from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from wikiflix.beeld.home.__init__ import blueprint
from werkzeug.exceptions import HTTPException

import wikiflix
import wikiflix.db

SHARED_TEMPLATE_FOLDER = "wikiflix/beeld/sh_templates"
SHARED_STATIC_FOLDER = "wikiflix/beeld/sh_static"

def pagina_niet_gevonden(e):
	return render_template("404.html"), 404


def algemene_fout(e):
	return render_template("bad_request.html")

def main():
    app = app_aanmaken()
    app.run(debug=True)

def app_aanmaken():
    app = Flask(__name__, template_folder=SHARED_TEMPLATE_FOLDER, static_folder=SHARED_STATIC_FOLDER)
    app.register_error_handler(404, pagina_niet_gevonden)
    app.register_error_handler(HTTPException, algemene_fout)

    #database toevoegen
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wikiflix.db'
    app.config['SECRET_KEY'] = "DeGeheimeSleutel"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    wikiflix.db.init_db(app)
    from wikiflix.core import auth_handler
    auth_handler.init(app)

    #blueprints laden
    app.register_blueprint(blueprint)

    return app

if __name__ == "__main__":
    main()

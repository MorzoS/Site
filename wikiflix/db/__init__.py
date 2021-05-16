from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_inst: SQLAlchemy = None

def init_db(flask_app):
    global db_inst

    db_inst = SQLAlchemy(flask_app)

    # importing the modules
    from wikiflix import models
    from wikiflix.models import wiki
    models: models
    wiki: wiki

    # create Database
    db_inst.create_all()
    print("Database aangemaakt", db_inst)
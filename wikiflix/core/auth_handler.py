from flask import Flask
from flask_login import LoginManager

from wikiflix.models import User


def _load_user(id):
	return User.query.filter_by(id=id).first()


def init(app: Flask):
	login_manager = LoginManager()
	login_manager.login_view = "auth.index"

	login_manager.user_loader(_load_user)

	login_manager.init_app(app)
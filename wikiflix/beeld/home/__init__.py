from flask import Blueprint, render_template
from flask_login import current_user, login_required

from wikiflix.core import NavBar

blueprint = Blueprint("home", __name__, template_folder="templates", static_folder="static")

@blueprint.route("/")
@blueprint.route("/home")
def home():
	navbar = NavBar.default_bar(active_page="Home")
	return render_template("home.html", navbar=navbar)

@blueprint.route("/profile")
@login_required
def profile():
	navbar = NavBar.default_bar()
	return render_template("profile.html", navbar=navbar)
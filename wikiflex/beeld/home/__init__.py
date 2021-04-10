from flask import Blueprint, render_template
from flask_login import current_user, login_required


blueprint = Blueprint("home", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/")
def home():
	return render_template("home.html")
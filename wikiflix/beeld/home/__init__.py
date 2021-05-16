from flask import Blueprint, render_template
from flask_login import current_user, login_required

from wikiflix.core import NavBar
from wikiflix.models import CarouselImage
from wikiflix.models.wiki import wiki


blueprint = Blueprint("home", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/")
def home():
	recently_added_wiki = wiki.query.order_by(wiki.titel.desc()).limit(3).all()
	
	carousel = CarouselImage.query.all()

	navbar = NavBar._default_bar(active_page="Home")
	return render_template("home.html", navbar=navbar, recently_added_wiki=recently_added_wiki, carousel=carousel)

@blueprint.route("/profile")
@login_required
def profile():
	navbar = NavBar._default_bar()

	collected_wiki = current_user.collected_wiki[:5]
	wiki_collected_count = len(current_user.collected_wiki)

	return render_template("profile.html", collected_wiki=collected_wiki, wiki_collected_count=wiki_collected_count)

@blueprint.route("/profile/collected")
def profile_collected_wiki():
	navbar = NavBar._default_bar()

	collected_wiki = current_user.collected_wiki

	return render_template("profile_collected.html", navbar=navbar, collected_wiki=collected_wiki)
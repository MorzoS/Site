from datetime import datetime

from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import FileField, IntegerField, SelectField, StringField, TextAreaField, validators

from wikiflix.core import NavBar
from wikiflix.core.form import InlineValidatedForm
from wikiflix.db import db_inst as db
from wikiflix.Models.wiki import wiki

blueprint = Blueprint("wiki", __name__, template_folder="templates", static_folder="static")

@blueprint.route("/", methods=['GET', 'POST'])
def index():
	navbar = NavBar.default_bar(active_page="wiki")

	current_page = request.args.get('p', 1, type=int)

	if request.args.get('search'):
		# Straight from the form into the query, what can go wrong..
		query = wiki.query.filter(wiki.title.like(f"%{request.args['search']}%"))
	else:
		query = wiki.query

	wiki = query.paginate(page=current_page, per_page=10, error_out=True)

	return render_template("wiki_front.html", navbar=navbar, wiki=wiki)

class CommentForm(FlaskForm):
	text = TextAreaField("", render_kw={"class": "form-control", "placeholder": "Add a comment!"},
						 validators=[validators.DataRequired()])

@blueprint.route("/<int:wiki_id>", methods=['GET', 'POST'])
def page(wiki_id):
	wiki = wiki.get(id=wiki_id)

	if not wiki:
		abort(404)

	is_liked = False

	if current_user.is_authenticated:
		if wiki in current_user.collected_wiki:
			is_liked = True

	navbar = NavBar.default_bar()

	return render_template(
		"wiki_page.html",
		navbar=navbar,
		wiki=wiki,
		liked=is_liked)

@blueprint.route("/<int:wiki_id>/collect")
@login_required
def user_collect(wiki_id):
	wiki = wiki.get(id=wiki_id)

	if not wiki:
		abort(404)

	current_user.collected_wiki.append(wiki)
	db.session.commit()

	return redirect(url_for('wiki.page', wiki_id=wiki_id))

@blueprint.route("/<int:wiki_id>/uncollect")
@login_required
def user_remove(wiki_id):
	wiki = wiki.get(id=wiki_id)

	if not wiki:
		abort(404)

	if wiki in current_user.collected_wiki:
		current_user.collected_wiki.remove(wiki)

	db.session.commit()

	return redirect(url_for('wiki.page', wiki_id=wiki_id))

@blueprint.route("/<int:wiki_id>/delete")
@login_required
def delete(wiki_id):
	wiki = wiki.get(id=wiki_id)

	if not wiki:
		abort(404)

	db.session.delete(wiki)
	db.session.commit()

	return redirect(url_for('wiki.index'))

@blueprint.route("/<int:wiki_id>/edit")
@login_required
def edit(wiki_id):
	wiki = wiki.get(id=wiki_id)

	if not wiki:
		abort(404)

	return redirect(url_for('wiki.index'))

class AddWikiForm(InlineValidatedForm):
	cover_art = FileField(
		render_kw={'accept': '.jpg,.png, application/vnd.sealedmedia.softseal.jpg,vnd.sealed.png'},
		validators=[validators.DataRequired("Please select a cover picture.")]
	)
	title = StringField(
		'Title',
		render_kw={"placeholder": "Title"},
		validators=[validators.DataRequired(message="Every wiki needs a title."), validators.Length(min=4, max=32)]
	)
	synopsis = TextAreaField(
		'Synopsis',
		render_kw={"placeholder": "Synopsis..."},
		validators=[]
	)
	episodes = IntegerField(
		'Episodes',
		validators=[validators.NumberRange(min=1, max=999)],
		render_kw={"placeholder": "Amount of episodes.."}
	)
	premiered = StringField(
        'Premiered',
        render_kw={"placeholder": "Premiered"},
        validators=[validators.DataRequired(message="Every wiki needs a premiered date."), validators.Length(min=10, max=18)]
    )
	
@blueprint.route("/add", methods=['GET', 'POST'])
@login_required
def add():
	form = AddWikiForm()
	navbar = NavBar.default_bar()

	if form.validate_on_submit():
		img_data: bytes = form.cover_art.data.stream.read()
		
		new_wiki = wiki(
			title=form.title.data,
			synopsis=form.synopsis.data,
			premiered=form.premiered.data,
			episodes=form.episodes.data,
			cover_art=img_data
		)

        db.session.add(new_wiki)
        db.session.commit()

        alert = Markup(
			f"Added wiki <b>{form.title.data}</b>. Go to <a href='{url_for('wiki.page', wiki_id=new_wiki.id)}'>page</a>.")
		#return render_template("wiki_add.html", navbar=navbar, form=form, success_alert=alert)

	#return render_template("wiki_add.html", navbar=navbar, form=form)
import flask_login
from flask import Blueprint, redirect, render_template, request, url_for
from wtforms import BooleanField, PasswordField, StringField, validators

from wikiflix.core import NavBar, validation
from wikiflix.core.form import InlineValidatedForm
from wikiflix.db import db_inst as db
from wikiflix.models import User

blueprint = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


class LoginForm(InlineValidatedForm):
	email = StringField(
		"E-mail",
		render_kw={
			"placeholder": "E-mail",
		},
		validators=[
			validators.DataRequired("Voer een Email adres in."),
			validators.Regexp(
				"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,3})$",
				message="Dit is niet een correct Email adres.")
		]

	)

	password = PasswordField(
		"Password",
		render_kw={
			"placeholder": "Password",
		},
		validators=[
			validators.DataRequired("Voer een wachtwoord in."),
			validators.Length(min=8, max=64, message="Het wachtwoord moet langer dan 8 tekens zijn")
		]

	)

	remember_me = BooleanField(
		"Remember me?",
		render_kw={
			"placeholder": "Password",
			"class": "form-check-input"
		}
	)


@blueprint.route("/", methods=['GET', 'POST'])
def index():
	if flask_login.current_user.is_authenticated:
		return redirect(url_for("home.home"))

	navbar = NavBar.default_bar()

	login_form = LoginForm()

	if login_form.validate_on_submit():
		print("Validating")
		valid = False

		user = User.query.filter(User.email.like(login_form.email.data)).first()

		if user:
			if user.check_password(login_form.password.data):
				valid = True

		if valid:
			flask_login.login_user(user, remember=login_form.remember_me.data)
			next = request.args.get("next")
			return redirect(next or url_for("home.home"))

		return render_template("login.html", navbar=navbar, login_form=login_form, login_error="Login failed.")

	return render_template("login.html", navbar=navbar, login_form=login_form)


@blueprint.route("/register", methods=['GET', 'POST'])
def register():
	if flask_login.current_user.is_authenticated:
		return redirect(url_for("home.home"))

	navbar = NavBar.default_bar()

	if request.method == "POST":
		valid = True

		errors = {}

		# Validate
		email = request.form.get('email')
		display_name = request.form.get('display_name')
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		password = request.form.get('password')
		password_repeat = request.form.get('password_repeat')

		if not email:
			errors['email_error'] = "Vul een geldig email adres in."
			valid = False
		else:
			if len(email) < 6:
				errors['email_error'] = "Ongeldige email lengte."
				valid = False
			else:
				if not validation.is_email(email):
					errors['email_error'] = "Incorrect email adres formaat."
					valid = False
				else:
					if User.user_exists(email):
						errors['email_error'] = "Email is al in gebruik."
						valid = False

		if not display_name:
			errors['display_name_error'] = "Vul een gebruikers naam in."
			valid = False

		if not first_name:
			errors['first_name_error'] = "Vul u voornaam in."
			valid = False

		if not last_name:
			errors['last_name_error'] = "Vul u achternaam in."
			valid = False

		if not password:
			errors['password_error'] = "Vul een wachtwoord in."
			valid = False

		if password:
			if not password_repeat:
				errors['repeat_password_error'] = "Herhaal u wachtwoord."
				valid = False
			else:
				if password_repeat != password:
					errors['password_repeat_error'] = "Wachtwoord komt niet overeen."
					valid = False

		if valid:
			new_user = User(
				email=email,
				display_name=display_name,
				first_name=first_name,
				last_name=last_name,
				password=User.secure_password(password)
			)

			db.session.add(new_user)
			db.session.commit()

			return redirect(url_for("auth.index"))

		return render_template("register.html", navbar=navbar, posted=True, **errors)

	return render_template("register.html", navbar=navbar)


@blueprint.route("/logout")
def logout():
	if flask_login.current_user.is_authenticated:
		flask_login.logout_user()

	return redirect(url_for("home.home"))
from flask_wtf import FlaskForm
from markupsafe import Markup

from wtforms import SelectField


class InlineValidatedForm(FlaskForm):
	"""Adds bootstrap inline validation classes to its fields"""

	def render(self, field, **kwargs):
		field_attr = self.__getattribute__(field)
		hint = 'form-select' if isinstance(field_attr, SelectField) else 'form-control'
		end = ''
		if self.is_submitted():
			if self.errors.get(field):
				hint += ' is-invalid'
				end = f"<div class='invalid-feedback'>{self.errors[field][0]}</div>"
			else:
				hint += ' is-valid'

		if kwargs.get('class_'):
			kwargs['class_'] += ' ' + hint
		else:
			kwargs['class_'] = hint

		return field_attr(**kwargs) + Markup(end)
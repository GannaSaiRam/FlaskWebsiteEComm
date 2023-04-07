from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError #, Email
from learn.models import User

class RegisterForm(FlaskForm):

	def validate_username(self, username_to_check):
		user = User.query.filter_by(username=username_to_check.data).first()
		if user: # User doesn't exist this value is None
			raise ValidationError("Username already exists! Please try a different username")

	username = StringField(label='User Name: ', validators=[Length(min=2, max=30), DataRequired()])
	# email = StringField(label="Email Address: ", validators=[Email(), DataRequired()])
	password1 = PasswordField(label='Password: ', validators=[Length(min=3), DataRequired()])
	password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
	submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
	username = StringField(label="User Name:", validators=[DataRequired()])
	password = PasswordField(label="Password:", validators=[DataRequired()])
	submit = SubmitField(label="Sign in")


class SellItemForm(FlaskForm):
	submit = SubmitField(label="Sell Item!")


class PurchaseItemForm(FlaskForm):
	submit = SubmitField(label="Purchase Item!")
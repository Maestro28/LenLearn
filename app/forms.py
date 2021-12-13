from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User, Vocabular
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    level = RadioField('Language Level', validators=[DataRequired()], choices=["A1", "A2", "B1", "B2", "C1", "C2"])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class VokaPracticeForm(FlaskForm):
    answer = StringField('answer', validators=[DataRequired()])
    submit = SubmitField('check')

    def validate_answer(self, answer):
        t = current_user.translations.order_by(Vocabular.last_check).first().text
        if t != answer.data.strip():
            raise ValidationError('Please try again')

class VokaAddForm(FlaskForm):
    text = StringField('text', validators=[DataRequired()])
    translation = StringField('translation', validators=[DataRequired()])
    submit = SubmitField('add')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('Tell your learning language reason', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
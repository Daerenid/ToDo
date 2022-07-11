from wtforms import StringField, PasswordField, validators, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError,  EqualTo, Email
from flask_wtf import FlaskForm
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Pole wymagane!')])
    password = PasswordField('Password', validators=[DataRequired('Pole wymagane!')])
    submit = SubmitField('Sign In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Podana nazwa użytkownika nie istnieje')
        

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Pole wymagane!')])
    email = StringField('Email Address', validators=[DataRequired('Pole wymagane!'), Email('Niepoprawny adres email')])
    password = PasswordField('Password', [
        validators.DataRequired('Pole wymagane!')

    ])
    confirm = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Wybrana nazwa użytkownika jest zajęta')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Wybrany adres email jest już zajęty')

class NewRepository(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    rep_submit = SubmitField('Dodaj')

class NewContent(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    cont_submit = SubmitField('Dodaj')

class NewTodo(FlaskForm):
    description = StringField('Todo', validators=[DataRequired()])
    
    todo_submit = SubmitField('Dodaj')

class NewTask(FlaskForm):
    name = StringField('Task', validators=[DataRequired()])
    task_submit = SubmitField('Dodaj')
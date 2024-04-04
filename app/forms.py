from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Length


class loginForm(FlaskForm):
    # Assuming userID is the id of the user creating the event, it's not a form field
    email = StringField('Username', validators=[DataRequired(), Length(max=80)])
    password = StringField('Password', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField('Login')

class registerForm(FlaskForm):
    # Assuming userID is the id of the user creating the event, it's not a form field
    email = StringField('Email', validators=[DataRequired(), Length(max=80)])
    password = StringField('Password', validators=[DataRequired(), Length(max=80)])
    role = StringField('Role', validators=[DataRequired(), Length(max=80)])
    name = StringField('Name', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField('Register')


class EventForm(FlaskForm):
    # Assuming userID is the id of the user creating the event, it's not a form field
    title = StringField('Title', validators=[DataRequired(), Length(max=80)])
    status = StringField('Status', validators=[DataRequired(), Length(max=80)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=255)])  # Textarea for longer input
    eventTime = DateTimeField('Event Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])  # Example format
    location = StringField('Location', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField('Create Event')

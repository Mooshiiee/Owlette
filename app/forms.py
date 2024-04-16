from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateTimeLocalField, TextAreaField, PasswordField, validators
from wtforms.validators import DataRequired, Length, Email, DataRequired, InputRequired
class loginForm(FlaskForm):
    # Assuming userID is the id of the user creating the event, it's not a form field
    email = StringField(label='Email', validators=[DataRequired(),  Length(max=80)])
    password = StringField(label='Password', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField(label='Login')

class registerForm(FlaskForm):
    # Assuming userID is the id of the user creating the event, it's not a form field
    email = StringField(label='Southern Email', validators=[InputRequired(), Email()])
    username = StringField(label='username', validators=[DataRequired(), Length(max=80)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    name = StringField(label='Name', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField(label='Register')


## This is for creating a post/event
class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=80)])
    status = StringField('Status', validators=[Length(max=80)]) ## STATUS NOT REQUIRED. ASSUMED EVENT IS ACTIVE UNTILL CANCELD
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=255)])  # Textarea for longer input
    eventTime = DateTimeLocalField('Event Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])  
    location = StringField('Location', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField('Create Event')

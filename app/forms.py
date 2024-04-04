from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Length

class EventForm(FlaskForm):
    # Assuming userID is the id of the user creating the event, it's not a form field
    title = StringField('Title', validators=[DataRequired(), Length(max=80)])
    status = StringField('Status', validators=[DataRequired(), Length(max=80)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=255)])  # Textarea for longer input
    eventTime = DateTimeField('Event Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])  # Example format
    location = StringField('Location', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField('Create Event')

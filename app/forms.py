from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Length


## This is for creating a post/event
class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=80)])
    status = StringField('Status', validators=[DataRequired(), Length(max=80)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=255)])  # Textarea for longer input
    eventTime = DateTimeField('Event Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])  
    location = StringField('Location', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField('Create Event')

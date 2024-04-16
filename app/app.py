from flask import Flask, render_template, request, flash, redirect, url_for, current_app, session
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, IntegerField, SubmitField, DateTimeLocalField, TextAreaField, PasswordField, validators
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms import EventForm, loginForm
from models import db, User, Event
from wtforms.validators import DataRequired, Length
from wtforms.validators import Email, DataRequired
from forms import EventForm

#flask --app app.py --debug run

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeforprod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///owlettedb.sqlite3'

from models import db, User, Event, Flair

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

migrate = Migrate(app, db)

@app.route('/testdb')
def testdb():
    dbtest = db.get_or_404(Event, 1)
    event = Event.query.get(1)
    print(event)
    return f"<h1>('Event: ' + {str(event)})</h1>"

# SPLASH PAGE
@app.route('/')
def index():
    return render_template('index.html')

# LOGIN

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = loginForm()
    if form.validate_on_submit():
        current_app.logger.info('Form submitted successfully')  # Add this line for debugging

        user = User.query.filter_by(email=form.email.data).first()

        if user and user.password == form.password.data and user.email == form.email.data:
            session['userID'] = user.userid
            session['firstName'] = user.firstname
            current_app.logger.info(user.firstname)  # Add this line for debugging

            login_user(user)
            return redirect(url_for('home')) # Change this to the home page
        
        else:
            flash('Login unsuccessful. Please check your credentials.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))




class registerForm(FlaskForm):
    # Assuming userID is the id of the user creating the event, it's not a form field
    email = StringField(label='Email', validators=[DataRequired(), Length(max=80)])
    username = StringField(label='Username', validators=[DataRequired(), Length(max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password')
    firstname = StringField(label='First Name', validators=[DataRequired(), Length(max=80)])
    lastname = StringField(label='Last Name', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField(label='Register')



# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    print('rendering')
    rform = registerForm()  # Create an instance of the registerForm
    if rform.validate_on_submit():
        # Process the form data here
        # Perform registration logic here
        # Redirect to a success page or render a success template
        db.session.add(rform)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('register.html', form=rform)

# HOME PAGE
@app.route('/home')
@login_required
def home():

    events = Event.query.all()
    return render_template('home.html', events=events)

@app.route('/myevents')
@login_required
def myevents():
    return render_template('myevents.html')

@app.route('/eventview/<int:eventID>')
@login_required
def eventdetailview(eventID):
    #gets entry from primarky key value
    singleEvent = Event.query.get(eventID)
    flairs = [flair.name for flair in singleEvent.flairs]  # Retrieve the flairs for the event
    return render_template("eventdetailview.html", singleEvent=singleEvent, flairs=flairs)

@app.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():

    form = EventForm(request.form)
    form.flair.choices = [(flair.flairID, flair.name) for flair in Flair.query.all()]
    if request.method == 'POST':
        for fieldName, fieldObject in form._fields.items():
            print(f"Field Name: {fieldName}, Field Value: {fieldObject.data}, Errors: {fieldObject.errors}")

   
    if form.validate_on_submit():

        #### temp user for now, need user id to post ## CHANGE WHEN LOGIN AND REGISTER IS DONE
        temp_user_id = 1  
        try:
            new_event = Event(
                userID=temp_user_id,
                title=form.title.data,
                description=form.description.data,
                eventTime=form.eventTime.data,
                location=form.location.data,

            )
            db.session.add(new_event)
            db.session.flush()
            selected_flairs = form.flair.data  # This will be a list of selected flair IDs
            print(selected_flairs)
            for flair_id in selected_flairs:
                flair = Flair.query.get(flair_id)
                if flair:
                    new_event.flairs.append(flair)

            
          
            db.session.commit()
            db.session.close()

            print('Event created successfully!')
            flash('Event created successfully!', 'success')
        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback() ## REVERT CHANGES IF ERROR
            flash('Error creating event.', 'error')
        return redirect(url_for('home'))
    else:
        print("Form not validated.")
        print(form.errors)  # Log form errors to help diagnose validation failures

    return render_template('createEvent.html', form=form)






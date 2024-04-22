from flask import Flask, render_template, request, flash, redirect, url_for, current_app, session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms import EventForm, loginForm, registerForm
from models import db, User, Event
from flask_migrate import Migrate

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



# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    print('rendering')
    rform = registerForm(request.form)  # Create an instance of the registerForm
    if  request.method == 'POST' and rform.validate_on_submit():
        # Check if email is from "@southernct.edu" domain
        if not rform.email.data.endswith('@southernct.edu'):
            flash('You must register with a Southern Connecticut State University email address.')
            return redirect(url_for('register'))

        # Create a User object
        user = User(
            email=rform.email.data,
            username=rform.username.data,
            firstname=rform.firstname.data,
            lastname=rform.lastname.data,
            password=rform.password.data
        )
        # Save the user to the database
        db.session.add(user)
        db.session.commit()
        # Redirect to a success page or render a success template
        return redirect(url_for('login'))

    return render_template('register.html', form=rform)


# HOME PAGE
@app.route('/home')
@login_required
def home():
    flair_filter = request.args.get('flair_filter', 'All')

    # Fetch flairs for the dropdown
    flairs = Flair.query.all()

    # Fetch events based on the selected flair
    if flair_filter == 'All':
        events = Event.query.all()  # Fetch all events if no specific flair is selected
    else:
        # Fetch events based on the selected flair
        events = Event.query.join(Event.flairone).filter(Flair.name == flair_filter).all()
    return render_template('home.html', events=events, flairs=flairs)

@app.route('/myevents')
@login_required
def myevents():
    print(current_user.userid)
    user_events = Event.query.filter_by(userID=current_user.userid).all() # Fetch events created by the current user by id
    return render_template('myevents.html', events=user_events)

@app.route('/eventview/<int:eventID>')
@login_required
def eventdetailview(eventID):
    #gets entry from primarky key value
    singleEvent = Event.query.get(eventID)
    print(singleEvent)
    flairName = singleEvent.flairone.name if singleEvent.flairone else "None"  # Retrieve the flairs for the event
    return render_template("eventdetailview.html", singleEvent=singleEvent, flairName=flairName)

@app.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm(request.form)

    form.flair.choices = [(0, 'None')] + [(flair.flairID, flair.name) for flair in Flair.query.all()]
    if request.method == 'POST':
        print("Form submitted")  # Debug statement
        if form.validate_on_submit():
            print("Form validated successfully")  # Debug statement

            # Temporary user ID for now, replace with actual user ID when login is implemented
            temp_user_id = 1  

            try:
                # Create a new event instance
                new_event = Event(
                    userID=temp_user_id,
                    title=form.title.data,
                    description=form.description.data,
                    eventTime=form.eventTime.data,
                    location=form.location.data,
                    flairone_id=form.flair.data if form.flair.data else None
                )

                # Add the new event to the database
                db.session.add(new_event)
                db.session.flush()  # Flush to ensure new_event gets an ID


                # Commit changes to the database
                db.session.commit()
                print('Event created successfully!')  # Debug statement
                flash('Event created successfully!', 'success')
            except Exception as e:
                # Handle errors
                print(f"An error occurred: {e}")  # Debug statement
                db.session.rollback()
                flash('Error creating event.', 'error')
            return redirect(url_for('home'))
        else:
            print("Form not validated.")  # Debug statement
            print(f"Form Errors: {form.errors}")  # Log form errors to help diagnose validation failures
    else:
        print("Form not submitted via POST")  # Debug statement

    return render_template('createEvent.html', form=form, flair=form.flair.choices)








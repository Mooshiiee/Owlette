from flask import Flask, render_template, request, flash, redirect, url_for, current_app, session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms import EventForm, loginForm, registerForm, commentForm, userBioForm
from models import db, User, Event, Comment
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

'''
    This is the main file of the project. This file contains all view functions and backend logic
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeforprod'
#setting our url to the db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///owlettedb.sqlite3'


from models import db, User, Event, Flair, RSVP
from flask import flash, url_for

db.init_app(app)
#initialize the app and flask login
login_manager = LoginManager()
login_manager.init_app(app)
default ={}


#user loader decorator to load a user given their id
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

#implementing migrate for easier migrations
migrate = Migrate(app, db)

#test page for our db
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
    #if the user is logged in and authenticated it will redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    #intialize a new form using our login form class
    form = loginForm()
    if form.validate_on_submit():

        #we find the user using the query function using the email address
        user = User.query.filter_by(email=form.email.data).first()

        #if the the password and email matches we will set the session for the user
        if user and user.password == form.password.data and user.email == form.email.data:
            session['userID'] = user.userid
            session['firstName'] = user.firstname
            #if the user's ismod attribute is true it will login the user and redirect to the admin page
            if user.ismod:
                login_user(user, remember=True)
                return redirect('/admin')

            login_user(user)
            
            #IMPORTANT SECURITY STEP IN https://flask-login.readthedocs.io/en/latest/
            next = flask.request.args.get('next')
            if not url_has_allowed_host_and_scheme(next, request.host):
                return flask.abort(400)

            return redirect(url_for('home')) # Change this to the home page
        
        else:
            #if the login is unsuccessful it will flash this image
            flash('Login unsuccessful. Please check your credentials.', 'danger')
    #this is where we pass the form to the login template usign WTFforms
    return render_template('login.html', form=form)

#logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


'''
    flask-admin has preset model view, but to add unique restrictions a custom model view is implemented to only
    allow is mod users to view the data
'''
class AdminModelView(ModelView):
    def is_accessible(self):
        # Check if user is logged in and is a moderator
        return current_user.is_authenticated and current_user.ismod

    def inaccessible_callback(self, name, **kwargs):
        # If user is not logged in, redirect to login page, else home page
        if not current_user.is_authenticated:
            current_app.logger.info('User is not authenticated')  # Add this line for debugging

        flash('You do not have permission to view the admin page.', 'error')
        return redirect(url_for('login'))
# ADMIN PAGE

admin = Admin(app, name='Admin View', template_mode='bootstrap3')
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Event, db.session))   


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
            password=rform.password.data,
            bio=rform.bio.data
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
    return render_template('home.html', events=events, flairs=flairs, 
                            current_user=current_user )

@app.route('/myevents')
@login_required
def myevents():
    event_type = request.args.get('type', 'posted')  # Default to showing posted events
    if event_type == 'posted':
        events = Event.query.filter_by(userID=current_user.userid).all()
    else:  # Assuming 'type' is 'rsvped'
        events = Event.query.join(RSVP, RSVP.eventID == Event.eventID).filter(RSVP.userID == current_user.userid).all()
    return render_template('myevents.html', events=events, event_type=event_type)


#EVENT VIEW ROUTE
@app.route('/eventview/<int:eventID>', methods=['GET','POST'])
@login_required
def eventdetailview(eventID):

    form = commentForm(request.form)
    rsvp_count = RSVP.query.filter_by(eventID=eventID).count() 


    #if comment form is submitted
    if request.method == 'POST' and form.validate():
        #we make a new object and pass in the parameters
        comment = Comment(
            userID = current_user.userid,
            eventID = eventID,
            message = form.message.data,     
        )
        #we add the comment to the db
        db.session.add(comment)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        flash('There was an issue submitting you comment.')

        newURL = f'/eventview/{eventID}'
        return redirect(newURL)
    #gets entry from primarky key value
    singleEvent = Event.query.get(eventID)
    flairName = singleEvent.flairone.name if singleEvent.flairone else "None"  # Retrieve the flairs for the event
    user_has_rsvped = RSVP.query.filter_by(userID=current_user.userid, eventID=eventID).first() is not None




    return render_template("eventdetailview.html", singleEvent=singleEvent, flairName=flairName, 
                user_has_rsvped=user_has_rsvped, form=form)


@app.route('/event/<int:event_id>/rsvp', methods=['POST'])
@login_required
def rsvp_to_event(event_id):
    #print(f"Attempting to RSVP for user {current_user.userid} to event {event_id}")
    
    #check for:
    existing_rsvp = RSVP.query.filter_by(userID=current_user.userid, eventID=event_id).first()

    if existing_rsvp: #delete rsvp entry
        print(f"Found existing RSVP for event {event_id}, deleting")
        db.session.delete(existing_rsvp)
        try:
            db.session.commit()
            flash('Your RSVP has been removed.', 'info')
        except Exception as e:
            db.session.rollback()
            flash('There was an issue removing your RSVP.', 'danger')
    else: #create new rsvp entry
        #print(f"No RSVP found for event {event_id}, creating new")
        new_rsvp = RSVP(userID=current_user.userid, eventID=event_id)
        db.session.add(new_rsvp)
        try:
            db.session.commit()
            flash('Your RSVP has been recorded!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('There was an issue recording your RSVP.', 'danger')
            print(f"Error: {str(e)}")
    #redirect
    return redirect(url_for('eventdetailview', eventID=event_id))


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
            temp_user_id = current_user.userid

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

@app.route('/profile/<int:userid>')
@login_required
def profileView(userid):
    user = User.query.get(userid)
    return render_template('profileview.html', user=user )

@app.route('/editProfile', methods=['GET', 'POST'])
@login_required
def editProfile():
    userid = current_user.userid
    user = User.query.get(userid)
    if user.userid == current_user.userid:
        # Retrieve the user's current bio from the database
        current_bio = user.bio

        # Create the form and pass the user's current bio as the initial value
        form = userBioForm(request.form, bio=current_bio)

        if request.method == 'POST' and form.validate_on_submit():
            user.bio = form.bio.data
            db.session.commit()
            
            return redirect(url_for('home', userid=userid))

        return render_template('editProfile.html', form=form)
    else:
        print('not the same user')

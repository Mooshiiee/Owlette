from flask import Flask, render_template, request, flash, redirect, url_for, current_app
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms import EventForm, loginForm
from models import db, User, Event

#flask --app app.py --debug run

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeforprod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///owlettedb.sqlite3'

from models import db, User, Event

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
        current_app.logger.info(user)  # Add this line for debugging

        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful!', 'success')
            current_app.logger.info('login works')  # Add this line for debugging

            return redirect(url_for('home')) # Change this to the home page
        
        else:
            flash('Login unsuccessful. Please check your credentials.', 'danger')
            current_app.logger.info('credentials wrong')  # Add this line for debugging

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
# REGISTER
@app.route('/register')
def register():
    return 'register page'

# HOME PAGE
@app.route('/home')
#@login_required
def home():
    events = Event.query.all()
    return render_template('home.html', events=events)

@app.route('/myevents')
def myevents():
    return render_template('myevents.html')

@app.route('/eventview/<int:eventID>')
def eventdetailview(eventID):
    #gets entry from primarky key value
    singleEvent = Event.query.get(eventID)
    return render_template("eventdetailview.html", singleEvent = singleEvent)

@app.route('/create-event', methods=['GET', 'POST'])
def create_event():
    print("Handling a request to the create-event route...")
    form = EventForm(request.form)

    if request.method == 'POST':
        for fieldName, fieldObject in form._fields.items():
            print(f"Field Name: {fieldName}, Field Value: {fieldObject.data}, Errors: {fieldObject.errors}")

    if form.validate_on_submit():
        print("Form validated.")
        #### temp user for now, need user id to post ## CHANGE WHEN LOGIN AND REGISTER IS DONE
        temp_user_id = 1  
        try:
            new_event = Event(
                userID=temp_user_id,
                title=form.title.data,
                description=form.description.data,
                eventTime=form.eventTime.data,
                location=form.location.data
            )
            db.session.add(new_event)
            db.session.commit()
            
            #grab the primary key of the event that was just created
            event_id = new_event.id
            #check how many flairs there are 
            if form.flair1.data:
                flairone = form.flair2.data
            else:
                flairone = None

            if form.flair2.data:
                flairtwo = form.flair2.data
            else:
                flairtwo = None

            if form.flair3.data:
                flairthree = form.flair3.data
            else:
                flairthree = None
            #create flair object 
            flair = Flair(
                eventID = event_id,
                flairone = form.flair1.data,
                flairtwo = form.flair2.data,
                flairthree = form.flair3.data
            )
            db.session.add(flair)
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






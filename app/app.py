# RUN WITH
# (in /app directory) 
# > flask run

from flask import Flask
from flask import render_template, request, flash, redirect, url_for
from flask_migrate import Migrate

from forms import EventForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeforprod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///owlettedb.sqlite3'

from models import db, User, Event, Flair

db.init_app(app)

migrate = Migrate(app,db)

#below is snippet for an alternate structure WITH views.py and def register_routes(app, db)
#from views import register_routes
#register_routes(app, db)

@app.route('/testdb')
def testdb():
    dbtest = db.get_or_404(Event, 1)
    event = Event.query.get(1)
    print(event)
    return f"<h1>('Event: ' + {str(event)})</h1>"

#SPLASHPAGE
@app.route('/')
def index():
    return render_template('index.html')

#LOGIN
@app.route('/login')
def login():
    return render_template('login.html')

#REGISTER
@app.route('/register')
def register():
    return 'register page'

#HOME PAGE
@app.route('/home')
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
    print(singleEvent)
    flairName = singleEvent.flairone.name if singleEvent.flairone else "None"  # Retrieve the flairs for the event
    return render_template("eventdetailview.html", singleEvent=singleEvent, flairName=flairName)

@app.route('/create-event', methods=['GET', 'POST'])
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



if __name__ == '__main__':
    app.run(debug=True)
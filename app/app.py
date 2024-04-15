# RUN WITH
# (in /app directory) 
# > flask run

from flask import Flask
from flask import render_template, request, flash, redirect, url_for
from flask_migrate import Migrate

from forms import EventForm, registerForm

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
@app.route('/register', methods=['GET', 'POST'])
def register():
    print('rendering')
    form = registerForm()  # Create an instance of the registerForm
    if form.validate_on_submit():
        # Process the form data here
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        name = request.form['full name']

        # Perform registration logic here
        # For example, store the user in a database

        # Redirect to a success page or render a success template
        return redirect(url_for('success'))

    return render_template('register.html', form=form)


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

if __name__ == '__main__':
    app.run(debug=True)
# RUN WITH
# (in /app directory) 
# > flask run

from flask import Flask
from flask import render_template, request, flash, redirect, url_for
from flask_migrate import Migrate

from .forms import EventForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeforprod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///owlettedb.sqlite3'

from models import db, Event, User



db.init_app(app)

migrate = Migrate(app,db)

#below is snippet for an alternate structure WITH views.py and def register_routes(app, db)
#from views import register_routes
#register_routes(app, db)

@app.route('/testdb')
def testdb():
    events = Event.query.all()
    return str(events)

#SPLASHPAGE
@app.route('/')
def hello():
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
    return render_template('home.html')

@app.route('/myevents')
def myevents():
    return render_template('myevents.html')

@app.route('/create-event', methods=['GET', 'POST'])
def create_event():
    form = EventForm(request.form)
    if request.method == 'POST' and form.validate():

        # ADD LOGIC TO SAVE TO DATABASE HERE, WHEN COMPLETED

        flash('Event created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('createEvent.html', form=form)






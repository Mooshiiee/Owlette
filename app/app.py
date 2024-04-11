from flask import Flask, render_template, request, flash, redirect, url_for, current_app
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms import EventForm, loginForm
from models import db, User, Event

#flask --app app.py --debug run

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeforprod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///owlettedb.sqlite3'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

migrate = Migrate(app, db)

@app.route('/testdb')
def testdb():
    dbtest = db.get_or_404(Event, 1)
    return str(dbtest)

# SPLASH PAGE
@app.route('/')
def index():
    return render_template('index.html')

# LOGIN

@app.route('/testuser')
def testuser():
    test = db.get_or_404(User, 2)
    return str(test)


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

@app.route('/create-event', methods=['GET', 'POST'])
def create_event():
    form = EventForm(request.form)
    if request.method == 'POST' and form.validate():

        # ADD LOGIC TO SAVE TO DATABASE HERE, WHEN COMPLETED

        flash('Event created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('createEvent.html', form=form)

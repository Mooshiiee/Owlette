from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeforprod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///owlettedb.sqlite3'

from models import db
db.init_app(app)

#ALTERNATIVE FORM WITH views.py and def register_routes(app, db)
#from views import register_routes
#register_routes(app, db)

@app.route('/testdb')
def testdb():
    #events = Event.query.all()
    return 0

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







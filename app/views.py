# > flask --debug --app app.views run
from flask import Flask, render_template
from models import db


def register_routes(app, db):

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


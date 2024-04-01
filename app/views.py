# > flask --debug --app app.views run

from flask import Flask

app = Flask(__name__)

#SPLASHPAGE
@app.route('/')
def hello():
    return "Hello ffasd, World! <a href='/login'>login</a> "

@app.route('/login')
def login():
    return 'login page'

@app.route('/register')
def register():
    return 'register page'
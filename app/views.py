# > flask --debug --app app.views run

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from app.forms import loginForm, registerForm, EventForm
#from app.models import User, Event

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] ='owl'

#SPLASHPAGE
@app.route('/')
def hello():
    return render_template('index.html')

#LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    '''if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User(email=email, password=password)

        db.session.add(user)
        db.session.commit()

        form.email.data = ''
        form.password.data = ''
        return redirect(url_for('login'))'''
    return render_template('login.html', form=form)

#REGISTER
@app.route('/register')
def register():
    return render_template('register.html')

#HOME PAGE
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/myevents')
def myevents():
    return render_template('myevents.html')


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)

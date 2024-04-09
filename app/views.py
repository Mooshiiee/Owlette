# > flask --debug --app app.views run

from flask import Flask, render_template, request, flash, redirect, url_for
from .forms import EventForm

app = Flask(__name__)
## CSRF token needed for working with form. 
app.config['SECRET_KEY'] = 'dnwadniuadniwd373h22'

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


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)


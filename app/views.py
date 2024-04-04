# > flask --debug --app app.views run

from flask import Flask, render_template

app = Flask(__name__)

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

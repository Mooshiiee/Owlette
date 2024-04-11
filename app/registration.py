# from flask import Flask, render_template, request, redirect, url_for, session
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
# import re

# app = Flask(__name__)
# app.config['Southern School Email'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'your_password'
# app.config['MYSQL_DB'] = 'geeklogin'

# # mysql = MySQL(app)

# @app.route('/')
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     msg = ''
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         username = request.form['username']
#         password = request.form['password']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
#         account = cursor.fetchone()
#         if account:
#             session['loggedin'] = True
#             session['id'] = account['id']
#             session['username'] = account['username']
#             msg = 'Logged in successfully!'
#             return render_template('index.html', msg=msg)
#         else:
#             msg = 'Incorrect username/password!'
#             return render_template('login.html', msg=msg)
#     return render_template('login.html', msg=msg)

# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     # Add any other cleanup or redirection logic here
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run(debug=True)



from app import db
db.create_all()

# HOW TO INSERT DATA
# >>> 
from app import db, Event, User
newuser = User(username='john_doe', email='john@example.com', password='password123', firstname='John', lastname='Doe', bio='Some bio')

db.session.add(newuser)

db.session.commit()

db.session.close()
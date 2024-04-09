from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(80))
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, email, password, role, name):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.name = name

    def __repr__(self):
        return '<User {}>'.format(self.username)



class Event(db.Model):
    __tablename__ = 'event'
    eventID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userid'))
    title = db.Column(db.String(80))
    status = db.Column(db.String(80), default='active')
    description = db.Column(db.String(389))
    eventTime = db.Column(db.DateTime)
    location = db.Column(db.String(80))

    def __repr__(self):
        return '<Event %r>' % self.title


class Flair(db.Model):
    __tablename__ = 'flair'
    flairID = db.Column(db.Integer, primary_key=True)
    eventID = db.Column(db.Integer, db.ForeignKey('event.eventID'), unique=True)
    flairone = db.Column(db.String(80))
    flairtwo = db.Column(db.String(80))
    flarirthree = db.Column(db.String(80))

    def __repr__(self):
        return '<Flair %r>' % self.name
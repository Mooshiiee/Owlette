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
        return '<User %r>' % self.username
    
class Event(db.Model):
    __tablename__ = 'event'
    eventID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer(80), db.ForeignKey('user.id'), unique=True)
    title = db.Column(db.String(80))
    status = db.Column(db.String(80))
    description = db.Column(db.String(80))
    eventTime = db.Column(db.String(80))
    location = db.Column(db.String(80))

    def __init__(self, name, date, location, description, title, status, eventTime):
        self.name = name
        self.date = date
        self.location = location
        self.description = description
        self.title = title
        self.status = status
        self.eventTime = eventTime

    def __repr__(self):
        return '<Event %r>' % self.name
    
class comment(db.Model):
    __tablename__ = 'comment'
    commentID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer(80), db.ForeignKey('user.id'), unique=True)
    eventID = db.Column(db.Integer(80), db.ForeignKey('event.eventID'), unique=True)
    message = db.Column(db.String(80))
    timestamp = db.Column(db.String(80))

    def __init__(self, userID, eventID, comment, time):
        self.userID = userID
        self.eventID = eventID
        self.comment = comment
        self.time = time

    def __repr__(self):
        return '<Comment %r>' % self.comment

class RSVP(db.Model):
    __tablename__ = 'rsvp'
    rsvpID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer(80), db.ForeignKey('user.id'), unique=True)
    eventID = db.Column(db.Integer(80), db.ForeignKey('event.eventID'), unique=True)
    timestamp = db.Column(db.String(80))

    def __init__(self, userID, eventID, timestamp):
        self.userID = userID
        self.eventID = eventID
        self.timestamp = timestamp

    def __repr__(self):
        return '<RSVP %r>' % self.status
    

class Flair(db.Model):
    __tablename__ = 'flair'
    flairID = db.Column(db.Integer, primary_key=True)
    eventID = db.Column(db.Integer(80), db.ForeignKey('event.eventID'), unique=True)
    name = db.Column(db.String(80))

    def __init__(self, eventID, flairID, name):       
        self.eventID = eventID
        self.flairID = flairID
        self.name = name
    
    def __repr__(self):
        return '<Flair %r>' % self.name
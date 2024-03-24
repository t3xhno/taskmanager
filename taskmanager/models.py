from taskmanager import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=True)
    creatorid = db.Column(db.Integer, nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    contact = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=True)

class TaskUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taskid = db.Column(db.Integer, nullable=False)
    userid = db.Column(db.Integer, nullable=False)


import configparser
import os

from flask import render_template, request, redirect

from taskmanager import app, db
from taskmanager.functions import *
from taskmanager.models import *

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(PROJECT_PATH, "config.ini")

config = configparser.ConfigParser()
config.read(CONFIG_PATH)
ADMINPASS = config.get('credentials', 'ADMINPASS')

@app.route('/', methods=['GET'])
def index():
    tasks = Task.query.all()
    return render_template('pages/index.html', tasks = tasks)

@app.route('/addtask', methods=['GET','POST']) 
def addtask():
    if request.method == 'GET':
        return render_template('pages/addtask.html')
    elif request.method == 'POST':
        taskname = request.form['taskname']
        taskdesc = request.form['taskdesc']
        username = request.form['username']
        # Input sanitation
        # Task name
        if not taskname.isprintable() or ("<" in taskname and ">" in taskname):
            return render_template('pages/response.html', response = "Task name has to be made only of letters or numbers.")
        if len(taskname) < 1 or len(taskname) > 40:
            return render_template('pages/response.html', response = "Task name lenght invalid, only smaller then 40 charachters allowed")

        # Username
        if username == "":
            creatorid = None
        else:
            try:
                creatorid = User.query.filter_by(username = username).first().id
            except:
                return render_template('pages/response.html', response = 'No user with this username. Please register')
            if creatorid is None:
                return render_template('pages/response.html', response = 'No user with this username. Please register.')
 
        # Task descripton
        if taskdesc != '':
            if not taskdesc.isprintable() or ("<" in taskdesc and ">" in taskdesc):
                return render_template('pages/response.html', response = "Task description has to be made of printable characters.")
            if len(taskdesc) > 2000:
                return render_template('pages/response.html', response = "Task description lenght invalid, only smaller then 2000 charachters allowed")
        sqladdtask = Task(name = taskname, desc = taskdesc, creatorid = creatorid)
        try:
            db.session.add(sqladdtask)
            db.session.commit()
            return render_template('pages/response.html', response = 'Task added')
        except:
            return render_template('pages/response.html', response = 'Adding task failed')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('pages/register.html')
    elif request.method == 'POST':
        username = request.form['username']
        contact = request.form['contact']
        password = request.form['password']

        # Username
        if not username.isalnum():
            return render_template('pages/response.html', response = "Username has to be made only of letters or numbers.")
        if len(username) < 1 or len(username) > 40:
            return render_template('pages/response.html', response = "Username lenght invalid, only smaller then 40 charachters allowed")

        # Contact
        if contact != '':
            if not contact.isprintable() or ("<" in contact and ">" in contact):
                return render_template('pages/response.html', response = "Contact information has to be made of printable characters.")
            if len(contact) > 100:
                return render_template('pages/response.html', response = "Contact lenght invalid, only smaller then 100 charachters allowed")

        # Password
        if password != '':
            if not password.isprintable():
                return render_template('pages/response.html', response = "Password has to be made of printable characters.")
            if len(password) > 500:
                return render_template('pages/response.html', response = "Password lenght invalid, only smaller then 500 charachters allowed")

        sqladduser = User(username = username, contact = contact, password = password)
        try:
            db.session.add(sqladduser)
            db.session.commit()
            return render_template('pages/response.html', response = 'User added')
        except:
            return render_template('pages/response.html', response = 'Adding user failed')

    else:
        return render_template('pages/response.html', response = 'HTTP request method not recogniezed')


@app.route('/projects/<int:task_id>', methods=['GET','POST']) 
def project(task_id:int):
    try:
        task = Task.query.get(task_id)
    except:
        return render_template('pages/response.html', response = 'Task not found, bad URL')
    if task is None:
        return render_template('pages/response.html', response = 'Task not found, bad URL')
    users = gettaskusers(task_id)
    if request.method == 'GET':
        return render_template("pages/project.html", task = task, users = users)
    elif request.method == 'POST':
        # Assigning user to task
        username = request.form['username']
        for user in users:
            if username == user.username:
                return render_template('pages/response.html', response = 'User already added to task')
        try:
            userid = User.query.filter_by(username = username).first().id
        except:
            return render_template('pages/response.html', response = 'User not found, please register.')
        if userid is None:
            return render_template('pages/response.html', response = 'User not found, please register.')
        sqladduser = TaskUser(userid = userid, taskid = task_id)
        try:
            db.session.add(sqladduser)
            db.session.commit()
            return render_template('pages/response.html', response = 'User added')
        except:
            return render_template('pages/response.html', response = 'Adding user failed')

@app.route('/projects/<int:task_id>/del', methods=['GET','POST']) 
def deltask(task_id:int):
    try:
        task = Task.query.get(task_id)
    except:
        return render_template('pages/response.html', response = 'Task not found, bad URL')
    if task is None:
        return render_template('pages/response.html', response = 'Task not found, bad URL')
    try:
        taskusers = TaskUser.query.filter_by(taskid = task_id).all()
    except:
        taskusers = None
    creatorid = task.creatorid
    if request.method == 'GET':
        if creatorid is None:
            try:
                db.session.delete(task)
                db.session.commit()
            except:
                return render_template('pages/response.html', response = 'Deleting task failed')
            try:
                if taskusers != None:
                    for taskuser in taskusers:
                        db.session.delete(taskuser)
                        db.session.commit()
            except:
                return render_template('pages/response.html', response = 'Deleting user assignment to task failed')
            return render_template('pages/response.html', response = 'Task deleted')
        else:
            return render_template('pages/deltask.html', task = task)
    if request.method == 'POST':
        password = request.form['password']
        if len(password) < 1 or len(password) > 500:
            return render_template('pages/response.html', response = "Password lenght invalid, only smaller then 500 charachters allowed")
        # Check password
        if password != ADMINPASS and password != User.query.get(creatorid).password:
            return render_template('pages/response.html', response = 'Wrong password')
        # Delete task
        try:
            db.session.delete(task)
            db.session.commit()
        except:
            return render_template('pages/response.html', response = 'Deleting task failed')
        try:
            if taskusers != None:
                for taskuser in taskusers:
                    db.session.delete(taskuser)
                    db.session.commit()
        except:
                return render_template('pages/response.html', response = 'Deleting user assignment to task failed')
        return render_template('pages/response.html', response = 'Task deleted')

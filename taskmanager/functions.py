from taskmanager.models import *

def gettaskusers(taskid):
    users = list()
    userids = list()
    try:
        taskusers = TaskUser.query.filter_by(taskid = taskid).all()
    except:
        taskusers = list()

    for taskuser in taskusers:
        userids.append(taskuser.userid)

    for userid in userids:
        users.append(User.query.get(userid))

    return users

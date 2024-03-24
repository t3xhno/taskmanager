#!/usr/bin/env python3
from taskmanager import db, app

print('[i] Trying to create databse...')
try:
    with app.app_context():
        db.create_all()
    print('[+] Success you can proceed with deployment!')
except:
    print('[-] Creating db failed :/')


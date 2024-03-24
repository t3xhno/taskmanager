# Task Manager

Interactive TODO list web application

# Development Setup

Install python and pip on local machine

```bash
pip install virtualenv
python -m venv venv #/path/to/new/virtual/environment
source venv/bin/activate #activate virtual env
pip install -r requirments.txt
python3 ./init_db.py #initialize database

python3 ./run.py #run project
```

# On database changes

Delete file `/instance/taskmanager.db`
And reinit the db

```shell
python3 ./init_db.py  
```

# Build app

```bash
cd build-deb/
make
```

# Install app

```bash
apt install ./build-deb/taskmanager.deb
```

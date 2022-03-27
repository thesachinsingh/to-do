from flask import Flask, render_template, session
from application.models import db, notes, users
# from application.controllers import *
import os

app = Flask(__name__)

app.secret_key = "jsvnsvjksvjsnvslknvksnjvorieoe"
db.init_app(app)
app.app_context().push()
# from application.controllers import *
basedir = os.path.abspath(os.path.dirname(__file__))
SQLITE_DB_DIR = os.path.join(basedir, "./db_directory")
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "db.sqlite3")

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
from application.controllers import *


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

#homepage
#loginpage
#signup page
#dashboard

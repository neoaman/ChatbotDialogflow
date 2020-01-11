from flask_sqlalchemy import SQLAlchemy
import json
from flask import Flask

app = Flask(__name__)

with open("config.json") as c:
    params = json.load(c)["params"]

app.config['SQLALCHEMY_DATABASE_URI'] = params['neomi_uri']
db = SQLAlchemy(app)
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40),nullable=False)
    course = db.Column(db.String(40),nullable=False)
    branch = db.Column(db.String(40),nullable=False)
    phone_num = db.Column(db.String(13),nullable=False)
    date = db.Column(db.String(12),nullable=True)
    email = db.Column(db.String(20),nullable=False)


# User.query.filter(User.email.endswith('@example.com')).all()
del_post= Contacts.query.filter(Contacts.date.between("11-01-2020","13-01-2020")).filter_by(branch='Bengaluru').all()
#Hyphen
print(del_post)
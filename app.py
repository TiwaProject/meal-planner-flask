import syslog
import uuid

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name


db.create_all()


@app.route("/")
def hello_world():
    user_list = db.session.query(User).all()
    return render_template('users.html', user_list=user_list)


@app.route("/users", methods=['GET'])
def get_users():
    users = db.session.query(User).all()
    print(users)
    return render_template('users.html', users=users)


@app.route("/users/<name>", methods=['GET'])
def save_user(name=None):
    user = User(name=name, email='ew@fdf.com')
    db.session.add(user)
    db.session.commit()
    print(name)
    print(user)
    return redirect(url_for('get_users'))


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

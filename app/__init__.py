import os
from flask import Flask, render_template, send_from_directory, redirect, url_for, session, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import smtplib

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}'.format(
    user=os.getenv('POSTGRES_USER'),
    passwd=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=5432,
    table=os.getenv('POSTGRES_DB'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UserModel(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"

@app.route('/health')
def health():
	return "<p>Works</p>", 200

@app.route('/logout')
def logout():
    return render_template('index.html', title="Rodrigo Luna", session_type=0, url=os.getenv("URL")), 200 

@app.route('/login', methods=('GET', 'POST'))
def login():
    error = 'e'
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        user = UserModel.query.filter_by(username=username).first()

        if user is username:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            return render_template('index.html', title="Rodrigo Luna", session_type=0, url=os.getenv("URL")), 200 
        else:
            return render_template('login.html', title="Login", session_type=0, err=error), 418

    return render_template('login.html', title="Login", session_type=0, err=error)

@app.route('/register', methods=('GET', 'POST'))
def register():
    error = 'e'
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return render_template('register.html',  title="Register", session_type=0, err="Register successful")
        else:
            return render_template('register.html',  title="Register", session_type=0, err=error), 418

    return render_template('register.html', title="Register", session_type=0, err=error)

@app.route('/')
def index():
    return render_template('index.html', title="Rodrigo Luna", session_type=0, url=os.getenv("URL"))


@app.route('/contact')
def contact():
    return render_template('contacts.html', title="Contact", session_type=0, url=os.getenv("URL"))

@app.route('/form',methods=["POST"])
def form():
	name = request.form.get("name")
	email = request.form.get("email")
	msg = request.form.get("msg")
	
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login("irodrigoro@gmail.com", os.getenv("PASS"))
	server.sendmail("irodrigoro@gmail.com", "irodrigoro@gmail.com", name+" "+email+" "+msg)
	
	return render_template("form.html", title="Form",na=name, em=email, mens=msg)

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    return "Blog"


@app.route('/projects')
def projects():
    # Hardcoded projects names
    robotics_projects = ['Sumo Robot/sumo.jpg', 'Line Following Robot/line_follower.png', 'Soccer Robot/soccer_robot.jpeg', 'Fire Extinguishing Robot/fire_robot.jpg']
    electronics_projects = ['Cell Phone Detector/Cell-phone-detector.jpg', 'Mobile Jammer Circuit/Mobile-Jammer.jpg']
    ai_projects = ['Font Classifier Perceptron/robot_img_example.png']
    misc_projects = ['Snake Video Game/snake.png']
    projects_names = [robotics_projects, electronics_projects, ai_projects, misc_projects]
	
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
	    page = 1
	
    return render_template('projects.html', title="Projects", session_type=0, url=os.getenv("URL"), projects=projects_names,pag = page)

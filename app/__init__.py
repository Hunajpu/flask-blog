import os
from flask import Flask, render_template, send_from_directory, redirect, url_for, session, request
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import smtplib

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


class PostForm(FlaskForm):
    body = TextAreaField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/health')
def health():
	return "<p>Hello</p>"

def index():
    return render_template('index.html', title="Firstname Lastname", url=os.getenv("URL"))

@app.route('/')


@app.route('/contact')
def contact():
	
    return render_template('contacts.html', title="Contact", url=os.getenv("URL"))

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
    form = PostForm()
    if form.validate_on_submit():
        session['post'] = form.body.data
        return redirect(url_for('blog'))
    return render_template('blog.html', title="Blog", url=os.getenv("URL"), form=form, post=session.get('post'))


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
	
	return render_template('projects.html', title="Projects", url=os.getenv("URL"), projects=projects_names,pag = page)

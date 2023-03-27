from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from sendMail import sendmail

# Define app
with open('config.json', 'r') as c: 
    params = json.load(c)["params"]

local_Server = params['local_server']
app = Flask(__name__)

if(local_Server) :
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else :
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

@app.route("/login")
def login() : 
    return render_template('login.html', params=params)

@app.route("/")
def home() :
    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]

    return render_template('index.html', params=params, posts=posts)

@app.route("/about")
def about() :
    return render_template('about.html', params=params)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), unique=True, nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), unique=True,nullable=False)

@app.route("/contact", methods = ['GET','POST'])
def contact() :
    if(request.method == 'POST') :
        ''' Add entry to the database '''  
        '''Fetch data and add it to the database''' 
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone_no')
        message = request.form.get('message')

        entry = Contacts(name=name, phone_num=phone, message=message, date=datetime.now(), email=email)

        db.session.add(entry)
        db.session.commit()

        sendmail(name, phone, email, message)

    return render_template('contact.html', params=params)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    admin = db.Column(db.String(20), nullable=False)
    slug = db.Column(db.String(30), unique=True, nullable=False)
    content = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(25), nullable=False)
    date = db.Column(db.String(12), nullable=True)

@app.route("/post/<string:post_slug>", methods=['GET'])
def post(post_slug) :
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)


app.run(debug=True)

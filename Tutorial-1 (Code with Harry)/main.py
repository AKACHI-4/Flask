from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json
from sendMail import send_mail

# Define app
with open('config.json', 'r') as c: 
    params = json.load(c)["params"]

local_Server = params['local_server']
app = Flask(__name__)
# Ref. - flask-Mail documentation
app.config.update (
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465', 
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)

mail = Mail(app)

if(local_Server) :
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else :
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

@app.route("/")
def home() :
    return render_template('index.html', params=params)

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

        send_mail(customer, dealer, rating, comments); 

    return render_template('contact.html', params=params)

@app.route("/post")
def post() :
    return render_template('post.html', params=params)

app.run(debug=True)

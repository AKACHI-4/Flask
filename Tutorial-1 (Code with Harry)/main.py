from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Define app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/codingthunder'
db = SQLAlchemy(app)

@app.route("/")
def home() :
    return render_template('index.html')

@app.route("/about")
def about() :
    return render_template('about.html')

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), unique=True, nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

@app.route("/contact", method = ['GET','POST'])
def contact() :
    if(request.method == 'POST') :
        ''' Add entry to the database '''   
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone_no')
        message = request.form.get('message')

        entry = Contacts(name=name, phone_num=phone, msg=message, email=email)

        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html')

@app.route("/post")
def post() :
    return render_template('post.html')

app.run(debug=True)

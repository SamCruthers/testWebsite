from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


app = Flask(__name__)  #helps flask find directories
#add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "a super key"
#init dbase
db = SQLAlchemy(app)

#create a model

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime,default=datetime.utcnow)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])

    submit = SubmitField("Submit")


#Create a form class
#CRF token as a key
class NamerForm(FlaskForm):
    name = StringField("Whats your name", validators=[DataRequired()])#change field to be ' 'Field e.g. DateField
    #validators = e.g. email
    submit = SubmitField("Submit")


@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()#filter to make sure email is unique
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name =form.name.data 
        form.name.data = ''
        form.email.data = ''
        flash("User added Successfully!")
    our_users = Users.query.order_by(Users.date_added)



    return render_template("add_user.html",form=form,name=name,our_users=our_users)


#Create a route decorator
@app.route('/') #any time you have website it needs urls, these are create by creating routes

#safe title striptags #title will capitililze first letter of all words
#trim removes trailing space at end

def index():
    firstname = "Johm"
    stuff = "This is <b>Bold</b>"#striptags in html removes
    #flash("Welcome ot our website")
    favourite_pizza = ["Cheese","Ham",67]
    return render_template("index.html", first_name=firstname, stuff=stuff,favourite_pizza=favourite_pizza)

#localhost:500/user/john
@app.route('/user/<name>')

def user(name):
    current_datetime = str(datetime.now())
    return render_template("user.html", username=name,datetime=current_datetime[:19])#username access on webpage, name is the python variable here

#def user(name):
#    current_datetime = datetime.now()
#    return "<h1>Hello {}<h1> <h2>it is {}".format(name,current_datetime)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    #validate
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = '' #clear it
        flash("Form submitted successfully")

    return render_template("name.html",name=name,form=form)



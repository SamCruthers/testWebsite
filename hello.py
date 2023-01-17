from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)  #helps flask find directories

#Create a route decorator
@app.route('/') #any time you have website it needs urls, these are create by creating routes

#def index():
#    return "<h1>Hello Fudger</h1>"

#safe title striptags #title will capitililze first letter of all words
#trim removes trailing space at end

def index():
    firstname = "Johm"
    stuff = "This is <b>Bold</b>"#striptags in html removes
    favourite_pizza = ["Cheese","Ham",67]
    return render_template("index.html", first_name=firstname, stuff=stuff,favourite_pizza=favourite_pizza)

#localhost:500/user/john
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", username=name)#username access on webpage, name is the python variable here

#def user(name):
#    current_datetime = datetime.now()
#    return "<h1>Hello {}<h1> <h2>it is {}".format(name,current_datetime)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
from pymongo import MongoClient
from flask_pymongo import PyMongo
import pymongo
import datetime
from flask import Flask, render_template, url_for, request, redirect

# Grab User/Password - Ensure these files are part of your .gitignore
connection_string = open("connection_string.txt")
connection_string = connection_string.read()

# Assign Flask app
app = Flask(__name__)

#DB Connetion String
client = pymongo.MongoClient(connection_string)
collection = client['test']['worldairquality']

@app.route("/")
def index():
    return render_template('index.html', title = "Layout Page")

@app.route("/", methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        search_field = request.form.get("search_field")
        try:
            country_search = collection.find_one({ "Country Code": search_field })
            latitude = country_search['Latitude']
            longitude = country_search['Longitude']
            return render_template('index.html', title = "Results Found", country_search = country_search, latitude = latitude, longitude =longitude)
        except Exception as e:
            return e
        
@app.route("/results")
def results():
    return render_template('results.html', title = "Layout Page")

if __name__ == "__main__":
    app.run(debug=True)
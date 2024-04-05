from pymongo import MongoClient
import pymongo
import datetime
from flask import Flask, render_template, url_for, request, redirect

# Grab User/Password - Ensure these files are part of your .gitignore
user = open("user.txt")
user = user.read()

password = open("pw.txt")
password = password.read()

# Assign Flask app
app = Flask(__name__)

#DB Connetion String
client = MongoClient(f'mongodb+srv://{user}:{password}@cluster0.ywxe5we.mongodb.net/')

@app.route("/", methods=['GET', 'POST'])

def index():
    return render_template('index.html')


# collection = client['test']['worldairquality']
# result = collection.find_one({ "Country Code": "JP" })
# print("Document found:\n", result)

if __name__ == "__main__":
    app.run(debug=True)
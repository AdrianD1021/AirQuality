from pymongo import MongoClient
import pymongo
import datetime
import folium
from flask import Flask, render_template, url_for, request, redirect

# Grab Connection String - Ensure this file are part of your .gitignore
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

    m = folium.Map()

    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()
    
    if request.method == "POST":
        search_field = request.form.get("search_field")
        try:
            country_search = collection.find_one({ "Country Code": search_field })

            latitude = country_search['Latitude']
            longitude = country_search['Longitude']

            folium.CircleMarker(
                location=[latitude, longitude],
                radius = 10,
            ).add_to(m)

            return render_template('index.html', title = "Results Found", country_search = country_search, latitude = latitude, longitude = longitude, iframe=iframe)
        except Exception as e:
            return e    

        
@app.route("/results")
def results():
    return render_template('results.html', title = "Layout Page")

@app.route("/map")
def iframe():
    """Embed a map as an iframe on a page."""

    country_search = collection.find_one({ "Country Code": "JP" })
    latitude = country_search['Latitude']
    longitude = country_search['Longitude']
    m = folium.Map(
        location=(latitude, longitude)
    )

    folium.CircleMarker(
        location=[latitude, longitude],
        radius = 10,
    ).add_to(m)

    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()

    return render_template('map.html',
        iframe=iframe
    )

if __name__ == "__main__":
    app.run(debug=True)
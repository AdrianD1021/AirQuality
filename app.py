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
collection = client['GEOJSON']['GEOJSONTest']
#collection = client['test']['worldairquality']

l = list(collection.find({}))


@app.route("/")
def index():
    return render_template('index.html', title = "Layout Page")

@app.route("/", methods=['GET', 'POST'])
def search():
    m = folium.Map()
    if request.method == "POST":        
        # Create      

        search_field = request.form.get("search_field")
        try:
            magnitude = collection.find_one({"properties.mag": {"$gte": float(search_field)}}) # {'properties.mag': {$gte: 4.5, $lt: 4.7}}

            ## Error handling for null results
            longitude = magnitude['geometry']['coordinates'][0] 
            latitude = magnitude['geometry']['coordinates'][1]

            print("Before IF statement")

            if magnitude and latitude and longitude:

                folium.CircleMarker(
                    location=[latitude, longitude],
                    radius=10,
                ).add_to(m)
                m.save("static/folium.html")
                # return redirect("/folium")
            

            return render_template(
                "index.html",
                title="Results Found",
                magnitude=magnitude,
                latitude=latitude,
                longitude=longitude,
                # iframe=iframe,
            )
        except Exception as e:
            return e

            # return render_template('index.html', title = "Results Found", magnitude = magnitude, latitude = latitude, longitude = longitude)
        # except Exception as e:
        #     return e    

# @app.route("/", methods=['GET', 'POST'])
# def search():
#     if request.method == "POST":
#         m = folium.Map(zoom_start=1)
#         # print("in post handler")
#         search_field = request.form.get("search_field")
#         # print(f"search field: {search_field}")
#         try:
#             country_search = collection.find_one({"Country Code": search_field})
#             # print(f"country_search: {country_search}")

#             latitude = country_search["Latitude"]
#             longitude = country_search["Longitude"]
#             # print(f"lat and long: {latitude}, {longitude}")

#             # Latitude': 35.908333, 'Longitude': 140.052778
#             if country_search and latitude and longitude:

#                 folium.CircleMarker(
#                     location=[latitude, longitude],
#                     radius=10,
#                 ).add_to(m)
#                 m.save("static/folium.html")
#                 # return redirect("/folium")

#             return render_template(
#                 "index.html",
#                 title="Results Found",
#                 country_search=country_search,
#                 latitude=latitude,
#                 longitude=longitude,
#                 # iframe=iframe,
#             )
#         except Exception as e:
#             return e


@app.route("/folium")
def folium_endpoint():
    return render_template("folium.html", title="Folium Page")
        
@app.route("/results")
def results():
    return render_template('results.html', title = "Layout Page")


### Delete?
@app.route("/map")
def geo():
    m = folium.Map([43, -100], zoom_start=4)
    folium.GeoJson(l).add_to(m)
    return m.get_root().render()

if __name__ == "__main__":
    app.run(debug=True)
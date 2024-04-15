from pymongo import MongoClient
import pymongo
import folium
from flask import Flask, render_template, url_for, request, redirect
import branca

# Grab Connection String - Ensure this file are part of your .gitignore
connection_string = open("connection_string.txt")
connection_string = connection_string.read()

# Assign Flask app
app = Flask(__name__)

#DB Connetion String
client = pymongo.MongoClient(connection_string)
collection = client['GEOJSON']['GEOJSONTest']

@app.route("/")
def index():
    return render_template('index.html', title = "Layout Page")

@app.route("/", methods=['GET', 'POST'])
def search():
    # Create basic Folium Map for page load
    m = folium.Map()

    if request.method == "POST":        

        # Grab field values     
        min_mag = request.form.get("min_mag")
        max_mag = request.form.get("max_mag")

        # Look through results
        try:
            for eq in collection.find({"properties.mag": {"$gte": float(min_mag), "$lte": float(max_mag)}}):

                title = eq['properties']['title']
                longitude = eq['geometry']['coordinates'][0] 
                latitude = eq['geometry']['coordinates'][1]
                magnitude = eq['properties']['mag']
                link = eq['properties']['url']
                
                # For every result that has a location, populate HTML and add a marker to map.                     
                if eq and latitude and longitude:

                    popup_html = """
                        <!DOCTYPE html>
                        <style>
                        
                        </style>
                        <base target="_blank">
                        <h4>{}</h4>
                        <p>
                        <b>Latitude:</b> {}
                        <br>
                        <b>Longitude:</b> {}
                        <br>
                        <b>Magnitude:</b> {}
                        <br>
                        <hr>
                        For more Info: <br> <a href="{}">Visit USGS</a>
                        </p>
                            """.format(title, latitude, longitude, magnitude, link)
                    iframe = branca.element.IFrame(html=popup_html, width=350, height=250)
                    popup = folium.Popup(iframe, max_width=500)

                    folium.Marker(
                        location=[latitude, longitude],
                        radius=10,
                        popup=popup
                    ).add_to(m)

            m.save("static/folium.html")

            return render_template(
                "index.html",
                title="Results Found",
                magnitude=eq,
                latitude=latitude,
                longitude=longitude,
                max_mag=max_mag,
            )

        except Exception as e:
            return e

@app.route("/folium")
def folium_endpoint():
    return render_template("folium.html", title="Folium Page")


@app.route("/graph")
def graph():
    return
        
if __name__ == "__main__":
    app.run(debug=True)
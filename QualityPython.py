from pymongo import MongoClient
import pymongo
import datetime

client = MongoClient('mongodb+srv://adriandd1021:AirQuality1@cluster0.ywxe5we.mongodb.net/')

collection = client['test']['worldairquality']

result = collection.find_one({ "Country Code": "JP" })

print("Document found:\n", result)
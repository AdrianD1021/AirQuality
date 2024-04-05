from pymongo import MongoClient
import pymongo
import datetime

user = open("user.txt")
user = user.read()

password = open("pw.txt") # SAMPLE DIRECTORY AND FILE NAME, CREATE FILE, CHANGE DIR
password = password.read()

client = MongoClient(f'mongodb+srv://{user}:{password}@cluster0.ywxe5we.mongodb.net/')

collection = client['test']['worldairquality']

result = collection.find_one({ "Country Code": "JP" })

print("Document found:\n", result)
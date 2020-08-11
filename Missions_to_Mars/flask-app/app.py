# import pymongo
from flask import Flask, jsonify
# from sqlalchemy import create_engine
from flask_pymongo import PyMongo
import scrape_mars

conn = 'mongodb://localhost:27017'



# client = pymongo.MongoClient(conn)

# Define the 'classDB' database in Mongo
# db = client.classDB



app = Flask(__name__)

app.config["MONGO_URI"] = conn+"/Mars_DB"
mongo_db = PyMongo(app)

mongo_db.db.Mars.delete_many({})
data = scrape_mars.scrape()
#add data to database
mongo_db.db.Mars.insert_one(data)


if(not mongo_db.db.Mars):
    print("No MARS data yet!")
    #find information to add to database
    data = scrape_mars.scrape()
    #add data to database
    mongo_db.db.Mars.insert_one(data)

print("MARS data available!")
    

# home route, to show the main page
@app.route('/')
def home():
    results = mongo_db.db.Mars.find_one()
    #render the template with the data from the database
    output = dict(results)
    output.pop("_id")
    print(output)
    return output


if __name__ == "__main__":
    app.run(debug=False)

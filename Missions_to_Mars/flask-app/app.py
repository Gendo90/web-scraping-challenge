# import pymongo
from flask import Flask, jsonify, render_template, request, redirect
# from sqlalchemy import create_engine
from flask_pymongo import PyMongo
import scrape_mars

conn = 'mongodb://localhost:27017'

app = Flask(__name__)

app.config["MONGO_URI"] = conn+"/Mars_DB"
mongo_db = PyMongo(app)
    

# home route, to show the main page
@app.route('/')
def home():
    # add try/except to add robustness to function,
    # creates a skeleton page with no data if no data loaded yet!
    try:
        results = mongo_db.db.Mars_Info2.find_one()
        # render the template with the data from the database
        output = dict(results)
        output.pop("_id")
        return render_template("index.html", info=output)
    except:
        dummy_dict = {
            "headline":"",
            "description":"",
            "featured_image":"",
            "Data Table":{},
            "Hemispheres":[]
        }
        return render_template("index.html", info=dummy_dict)

# route to scrape data
@app.route('/scrape')
def scrape_data_now():

    # refreshes the Mars data upon scraping
    # remove previous Mars data (if any)
    try:
        mongo_db.db.Mars_Info2.delete_many({})
    except:
        pass
    # scrape the Mars data online
    data = scrape_mars.scrape()

    # add data to database
    mongo_db.db.Mars_Info2.insert_one(data)

    # following line used for debugging that 
    # data is scraped correctly - working!
    #print(data, flush=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

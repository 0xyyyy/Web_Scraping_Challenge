import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = mars_scrape.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

@app.route("/")
def home():
    mars = mongo.db.mars.find_one() 
    return render_template("index.html, mars=mars")



if __name__ == "__main__":
    app.run(debug=True)
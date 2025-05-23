from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connessione al database MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["car_project"]  # <-- nome del tuo database
cars_col = db["cars"]
reviews_col = db["reviews"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/cars')
def show_cars():
    cars = list(cars_col.find())
    return render_template("cars.html", cars=cars)

@app.route('/reviews')
def show_reviews():
    reviews = list(reviews_col.find())
    return render_template("reviews.html", reviews=reviews)

if __name__ == "__main__":
    app.run(debug=True)

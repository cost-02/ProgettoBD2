from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connessione al database MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["car_project"] #nome database
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

@app.route('/join')
def show_join():
    joined_reviews = list(reviews_col.aggregate([
    {
        "$lookup": {
        "from": "cars",
        "localField": "car_id", # presente nella recensione
        "foreignField": "id", # campo 'id' presente nell'auto
        "as": "car_info"
         }
    }
    ]))
    return render_template("join.html", reviews=joined_reviews)

if __name__ == "__main__":
    app.run(debug=True)

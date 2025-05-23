from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import uuid 
from bson.objectid import ObjectId


app = Flask(__name__)

# Connessione al database MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["car_project"] #nome database
cars_col = db["cars"]
reviews_col = db["reviews"]

@app.route('/')
def index():
    return render_template("index.html")

#ROUTE DELLE MACCHINE
@app.route('/cars')
def show_cars():
    cars = list(cars_col.find())
    return render_template("cars.html", cars=cars)

#ROUTE DELLE RECENSIONI
@app.route('/reviews')
def show_reviews():
    reviews = list(reviews_col.find())
    return render_template("reviews.html", reviews=reviews)

#ROUTE DELLE JOIN
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


#ROUTE AGGIUNTA RECENSIONI (CRUD)
@app.route('/add_review', methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        new_review = {
            "id": "rev" + str(uuid.uuid4())[:8],
            "car_id": request.form['car_id'],
            "Author_Name": request.form['author'],
            "Rating": float(request.form['rating']),  
            "Review_Title": request.form['title_review'],
            "Review": request.form['text']
        }
        reviews_col.insert_one(new_review)
        return redirect(url_for('show_reviews'))
    
    cars = list(cars_col.find({}, {"id": 1, "Make": 1, "Model": 1}))
    return render_template("add_review.html", cars = cars)

#AGGIORNAMENTO RECENSIONE
@app.route('/edit_review/<review_id>', methods=["GET", "POST"])
def edit_review(review_id):
    review = reviews_col.find_one({"_id": ObjectId(review_id)})

    if request.method == "POST":
        updated_review = {
            "car_id": request.form['car_id'],
            "Author_Name": request.form['author'],
            "Rating": float(request.form['rating']),
            "Review": request.form['text']
        }
        reviews_col.update_one({"_id": ObjectId(review_id)}, {"$set": updated_review})
        return redirect(url_for('show_reviews'))

    cars = list(cars_col.find({}, {"id": 1, "Make": 1, "Model": 1}))
    return render_template("edit_review.html", review=review, cars=cars)

#CANCELLAZIONE RECENSIONE
@app.route('/delete_review/<review_id>', methods=["POST"])
def delete_review(review_id):
    reviews_col.delete_one({"_id": ObjectId(review_id)})
    return redirect(url_for('show_reviews'))



#OPERAZIONI CRUD PER AUTO
#AGGIUNTA AUTO
@app.route('/add_car', methods=["GET", "POST"])
def add_car():
    if request.method == "POST":
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        cars_col.insert_one({
        "Make": make,
        "Model": model,
        "Year": year
        })
        return redirect(url_for('show_cars'))
    return render_template("add_car.html")

#MODIFICA AUTO
@app.route('/edit_car/<car_id>', methods=["GET", "POST"])
def edit_car(car_id):
    car = cars_col.find_one({"_id": ObjectId(car_id)})
    if request.method == "POST":
        updated_data = {
        "Make": request.form['make'],
        "Model": request.form['model'],
        "Year": request.form['year']
        }
        cars_col.update_one({"_id": ObjectId(car_id)}, {"$set": updated_data})
        return redirect(url_for('show_cars'))
    return render_template("add_car.html")


#ELIMINA AUTO
@app.route('/delete_car/<car_id>', methods=["POST"])
def delete_car(car_id):
    cars_col.delete_one({"_id": ObjectId(car_id)})
    return redirect(url_for('show_cars'))


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import uuid 
from bson.objectid import ObjectId
from itertools import groupby
from operator import itemgetter
from collections import defaultdict


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
def cars():
    make_filter = request.args.get('make')

    if make_filter and make_filter.lower() != 'tutte':
        cars_list = list(cars_col.find({"Make": make_filter}))
    else:
        cars_list = list(cars_col.find())

    cars_by_make = defaultdict(list)
    for car in cars_list:
        cars_by_make[car['Make']].append(car)

    # Per i bottoni: prendi tutte le marche distinte per mostrarle
    all_makes = cars_col.distinct("Make")
    all_makes.sort()

    return render_template('cars.html', cars_by_make=cars_by_make, all_makes=all_makes, selected_make=make_filter)


#ROUTE DELLE RECENSIONI
@app.route('/reviews')
def show_reviews():
    car_id = request.args.get('car_id')
    if car_id:
      reviews = list(reviews_col.find({"car_id": car_id}))
    else:
        reviews = list(reviews_col.find())
    return render_template("reviews.html", reviews=reviews)


#ROUTE DELLE JOIN
from flask import request

@app.route('/join')
def show_join():
    # Prendo il filtro marca dalla query string (es: /join?make=Audi)
    selected_make = request.args.get('make')

    joined_reviews = list(reviews_col.aggregate([
        {
            "$lookup": {
                "from": "cars",
                "localField": "car_id",
                "foreignField": "id",
                "as": "car_info"
            }
        }
    ]))

    for review in joined_reviews:
        if review.get('car_info') and len(review['car_info']) > 0:
            review['car_make'] = review['car_info'][0].get('Make', 'Unknown')
        else:
            review['car_make'] = 'Unknown'

    # Ordino per car_make per groupby
    joined_reviews.sort(key=lambda r: r['car_make'])

    # Lista marche uniche per i bottoni filtro
    makes = sorted(set(r['car_make'] for r in joined_reviews))

    # Se è stato selezionato un filtro, applico la selezione
    if selected_make and selected_make != "Tutti":
        filtered_reviews = [r for r in joined_reviews if r['car_make'] == selected_make]
    else:
        filtered_reviews = joined_reviews

    return render_template("join.html", reviews=filtered_reviews, makes=makes, selected_make=selected_make or "Tutti")




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
        return redirect(url_for('cars'))
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
        return redirect(url_for('cars'))  # la tua route per lista auto è 'cars', non 'show_cars'
    return render_template("edit_car.html", car=car)



#ELIMINA AUTO
@app.route('/delete_car/<car_id>', methods=["POST"])
def delete_car(car_id):
    cars_col.delete_one({"_id": ObjectId(car_id)})
    return redirect(url_for('cars'))


if __name__ == "__main__":
    app.run(debug=True)

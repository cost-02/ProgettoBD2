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
        try:
            car_obj_id = ObjectId(car_id)
        except:
            return "ID macchina non valido", 400
        reviews = list(reviews_col.find({"car_id": car_obj_id}))
        car = cars_col.find_one({"_id": car_obj_id}) # <-- recupera i dati dell'auto
    else:
        reviews = list(reviews_col.find())
        car = None

    return render_template("reviews.html", reviews=reviews, car=car)

from bson import ObjectId


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
                "foreignField": "_id",
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



from bson import ObjectId
#ROUTE AGGIUNTA RECENSIONI (CRUD)
@app.route('/add_review', methods=["GET", "POST"])
def add_review(car_id=None):
    cars = list(db.cars.find())
    selected_car_id = request.args.get('car_id')  # <-- Prendi l'ID dall'URL
    if request.method == "POST":
        new_review = {
            "car_id": ObjectId(request.form['car_id']),
            "Author_Name": request.form['author'],
            "Rating": float(request.form['rating']),
            "Review_Title": request.form['title_review'],
            "Review": request.form['text']
        }
        reviews_col.insert_one(new_review)
        return redirect(url_for('show_reviews', car_id=request.form['car_id']))

    cars = list(cars_col.find({}, {"_id": 1, "Make": 1, "Model": 1}))
    return render_template('add_review.html', cars=cars, selected_car_id=selected_car_id)

from bson.errors import InvalidId
#AGGIORNAMENTO RECENSIONE
@app.route('/edit_review/<review_id>', methods=["GET", "POST"])
def edit_review(review_id):
    review_obj_id = ObjectId(review_id)
    review = reviews_col.find_one({"_id": review_obj_id})
    if request.method == "POST":
        updated_review = {
            "car_id": ObjectId(request.form['car_id']),
            "Author_Name": request.form['author'],
            "Rating": float(request.form['rating']),
            "Review_Title": request.form['title_review'],
            "Review": request.form['text']
        }
        reviews_col.update_one({"_id": review_obj_id}, {"$set": updated_review})
        return redirect(url_for('show_reviews', car_id=request.form['car_id']))

    cars = list(cars_col.find({}, {"_id": 1, "Make": 1, "Model": 1}))
    return render_template("edit_review.html", review=review, cars=cars)

#CANCELLAZIONE RECENSIONE
@app.route('/delete_review/<review_id>', methods=["POST"])
def delete_review(review_id):
    review_obj_id = ObjectId(review_id)
    review = reviews_col.find_one({"_id": review_obj_id})
    car_id = review.get("car_id")
    reviews_col.delete_one({"_id": review_obj_id})
    # Redirect alla pagina recensioni di quella macchina
    return redirect(url_for('show_reviews', car_id=str(car_id)))

#OPERAZIONI CRUD PER AUTO
#AGGIUNTA AUTO
@app.route('/add_car', methods=["GET", "POST"])
def add_car():
    if request.method == "POST":
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        fuel = request.form['fuel']
        engine_size = int(request.form['engine_size'])
        hp = int(request.form['hp'])
        transmission = request.form['transmission']
        launch_price = float(request.form['launch_price'])
        cars_col.insert_one({
        "Make": make,
        "Model": model,
        "Year": year,
        "Engine Fuel Type": fuel,
        "Engine Cylinders": engine_size,
        "Engine HP": hp,
        "Transmission Type": transmission,
        "MSRP": launch_price
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
            "Year": request.form['year'],
            "Engine Fuel Type": request.form['fuel'],
            "Engine Cylinders": int(request.form['engine_size']),
            "Engine HP": int(request.form['hp']),
            "Transmission Type": request.form['transmission'],
            "MSRP": float(request.form['launch_price'])
        }
        cars_col.update_one({"_id": ObjectId(car_id)}, {"$set": updated_data})
        return redirect(url_for('show_reviews', car_id=car_id))
    return render_template("edit_car.html", car=car)



#ELIMINA AUTO
@app.route('/delete_car/<car_id>', methods=["POST"])
def delete_car(car_id):
    cars_col.delete_one({"_id": ObjectId(car_id)})
    return redirect(url_for('cars'))


if __name__ == "__main__":
    app.run(debug=True)

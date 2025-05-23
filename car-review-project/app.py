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

if __name__ == "__main__":
    app.run(debug=True)

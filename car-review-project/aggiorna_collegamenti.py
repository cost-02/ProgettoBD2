from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["car_project"] 
cars_col = db["cars"]
reviews_col = db["reviews"]

# Step 1: mappa ID vecchi con ObjectId reali
id_map = {}
for car in cars_col.find({"id": {"$exists": True}}):
    id_map[car["id"]] = car["_id"]

# Step 2: rimuovi campo "id" dalle auto
for old_id in id_map:
    cars_col.update_many({"id": old_id}, {"$unset": {"id": ""}})

# Step 3: aggiorna recensioni usando ObjectId delle auto
for old_id, object_id in id_map.items():
    reviews_col.update_many({"car_id": old_id}, {"$set": {"car_id": object_id}})

# Step 4: Rimuove il campo personalizzato chiamato "id", se presente (non l'_id di MongoDB!)
reviews_col.update_many(
    {"id": {"$exists": True}},
    {"$unset": {"id": ""}}
)

print("Mappatura completata.")

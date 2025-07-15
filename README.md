# ProgettoBD2
# 🚗 Car Reviews App (NoSQL + Flask + MongoDB)

Questo progetto è stato realizzato per un progetto universitario NoSQL, e si basa su un'applicazione web sviluppata in **Python (Flask)** che interagisce con un database **MongoDB**, dove sono memorizzati dati relativi a **modelli di auto** e **recensioni**.

---

## 🗃️ Struttura del Database

Il progetto utilizza due collection in MongoDB:

- `cars`: contiene le informazioni sui modelli di auto.
- `reviews`: contiene le recensioni degli utenti relative ai modelli di auto.

Le due collection sono collegate tramite il campo `id_car`, che funge da chiave logica (equivalente a una foreign key).

---

## 📦 Requisiti

- Python 3.7+
- MongoDB installato in locale o in cloud (es. MongoDB Atlas)
- pip

---

## 🧰 Installazione

1. **Clona il repository**
   
2. **Crea un ambiente virtuale (opzionale ma consigliato)
   
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows

4. **Installa le dipendenze
   
pip install -r requirements.txt

6. **Avvia MongoDB (oppure assicurati che sia attivo su Atlas/localhost)

7. **Importa i file JSON nel tuo database MongoDB

mongoimport --db car_project --collection cars --file cars.json --jsonArray
mongoimport --db car_project --collection reviews --file reviews.json --jsonArray

nb. Assicurati che MongoDB sia attivo e che i file siano nella directory corretta.

9. **Avvio dell'app Flask 🚀
    
Per eseguire l'app localmente:
python app.py
L'app sarà disponibile su http://127.0.0.1:5000.

---

📁 Struttura del progetto
car-reviews-app/
│
├── app.py
├── requirements.txt
├── cars.json
├── reviews.json
├── templates/
│   ├── index.html
│   ├── cars.html
│   ├── reviews.html
│   └── join.html (se presente)
├── static/ (opzionale per CSS/JS)
└── README.md

---

📌 Autore
  - Nome: Costantino Paciello, Andrea Salurno
  - Corso: Basi di Dati 2 - Progetto NoSQL
  - Anno: 2024/2025

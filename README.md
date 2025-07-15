# 🚗 Car Reviews App (NoSQL + Flask + MongoDB)

**ProgettoBD2** — Applicazione web sviluppata per il corso universitario *Basi di Dati 2*, utilizzando **Python (Flask)** e **MongoDB** come database NoSQL.

L'app consente la gestione e visualizzazione di **modelli di auto** e **recensioni** utenti, con dati strutturati in due collection collegate logicamente.

---

## 🗃️ Struttura del Database

Il database `car_project` contiene le seguenti collection:

- `cars`: Informazioni sui modelli di auto.
- `reviews`: Recensioni associate ai modelli.

🔗 Le collection sono collegate tramite il campo `id_car`, che funge da chiave logica (simile a una *foreign key*).

---

## 📦 Requisiti

- Python **3.7+**
- MongoDB (locale o in cloud — es. MongoDB Atlas)
- Gestore pacchetti `pip`

---

## 🧰 Installazione

1. **Clona il repository:**
   ```bash
   git clone https://github.com/tuo-username/car-reviews-app.git
   cd car-reviews-app
   ```

2. **Crea un ambiente virtuale (opzionale ma consigliato):**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. **Installa le dipendenze:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Avvia MongoDB** (oppure assicurati che sia attivo su Atlas/localhost)

5. **Importa i file JSON nel database:**
   ```bash
   mongoimport --db car_project --collection cars --file cars.json --jsonArray
   mongoimport --db car_project --collection reviews --file reviews.json --jsonArray
   ```
   ℹ️ Assicurati che MongoDB sia attivo e che i file siano nella directory corretta.

6. **Avvia l'app Flask 🚀**
   ```bash
   python app.py
   ```
   L'app sarà disponibile su [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 📁 Struttura del progetto

```
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
│   └── join.html          # Se presente
├── static/                # Opzionale per CSS/JS
└── README.md
```

---

## 📌 Autori

- **Costantino Paciello**
- **Andrea Salurno**

📚 *Corso:* Basi di Dati 2 — Progetto NoSQL  
📅 *Anno Accademico:* 2024/2025

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/health")
def health():
    return "Flask kører!"

# Opret eller forbind til databasen
def get_db_connection():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    return conn

# Opret tabel, hvis den ikke eksisterer
with get_db_connection() as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, navn TEXT, alder INTEGER, by TEXT)")
    conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        navn = request.form["navn"]
        alder = request.form["alder"]
        by = request.form["by"]

        # Gem data i databasen
        with get_db_connection() as conn:
            conn.execute("INSERT INTO users (navn, alder, by) VALUES (?, ?, ?)", (navn, alder, by))
            conn.commit()

        return f"Tak for dit svar! Navn: {navn}, Alder: {alder}, By: {by}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

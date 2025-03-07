from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import sqlite3

app = Flask(__name__, template_folder="templates")

# Konfigurer Flask-Session til at gemme sessionsdata i filsystemet
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Opret eller forbind til databasen
def get_db_connection():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    return conn

# Opret tabel, hvis den ikke eksisterer
with get_db_connection() as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, navn TEXT, alder INTEGER, by TEXT)")
    conn.commit()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    step = session.get("step", 0)  # Hvilket trin brugeren er på
    svar = data.get("svar", "").strip()  # Brugerens svar

    # Liste over spørgsmål i chatbotten
    spørgsmål = ["Hvad er dit navn?", "Hvor gammel er du?", "Hvor bor du?"]

    if step == 0:
        session["navn"] = svar
    elif step == 1:
        session["alder"] = svar
    elif step == 2:
        session["by"] = svar
        # Gem i databasen
        with get_db_connection() as conn:
            conn.execute("INSERT INTO users (navn, alder, by) VALUES (?, ?, ?)", 
                         (session["navn"], session["alder"], session["by"]))
            conn.commit()
        return jsonify({"besked": f"Tak {session['navn']}! Dine oplysninger er gemt.", "done": True})

    session["step"] = step + 1  # Opdater step
    return jsonify({"besked": spørgsmål[step], "step": session["step"]})

@app.route("/")
def index():
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True)

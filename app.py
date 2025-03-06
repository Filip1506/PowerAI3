from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Opret eller forbind til databasen
def get_db_connection():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    return conn

# Opret tabel, hvis den ikke eksisterer
with get_db_connection() as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, navn TEXT, alder INTEGER, by TEXT)")
    conn.commit()

# API til at modtage brugerens svar
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    step = data.get("step", 0)  # Hvilket trin brugeren er på
    svar = data.get("svar", "")  # Brugerens seneste svar

    # Liste over spørgsmål i chatbotten
    spørgsmål = [
        "Hvad er dit navn?",
        "Hvor gammel er du?",
        "Hvor bor du?"
    ]

    # Gem svar baseret på trin
    session = data.get("session", {"navn": "", "alder": "", "by": ""})
    if step == 1:
        session["navn"] = svar
    elif step == 2:
        session["alder"] = svar
    elif step == 3:
        session["by"] = svar
        # Gem data i databasen
        with get_db_connection() as conn:
            conn.execute("INSERT INTO users (navn, alder, by) VALUES (?, ?, ?)", (session["navn"], session["alder"], session["by"]))
            conn.commit()
        return jsonify({"besked": f"Tak {session['navn']}! Dine oplysninger er gemt.", "done": True})

    # Send næste spørgsmål
    return jsonify({"besked": spørgsmål[step], "step": step + 1, "session": session})

@app.route("/")
def index():
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True)

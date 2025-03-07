from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import psycopg2

DATABASE_URL = "postgresql://powerai3_db_user:fkP4gIaTrJsVnKxQcH1WfqC5wroVYeaw@dpg-cv53r3dumphs73fdbqf0-a/powerai3_db"

app = Flask(__name__, template_folder="templates")

# Konfigurer Flask-Session til at gemme sessionsdata i filsystemet
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Opret eller forbind til databasen
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Opret tabel, hvis den ikke eksisterer
with get_db_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                navn TEXT NOT NULL,
                alder INTEGER,
                by TEXT
            )
        """)
        conn.commit()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    step = int(data.get("step", 0))  # Hvilket trin brugeren er på
    svar = data.get("svar", "").strip()  # Brugerens seneste svar

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
            conn.execute("INSERT INTO users (navn, alder, by) VALUES (?, ?, ?)", 
                         (session["navn"], session["alder"], session["by"]))
            conn.commit()
        return jsonify({"besked": f"Tak {session['navn']}! Dine oplysninger er gemt.", "done": True})

    # Send næste spørgsmål
    return jsonify({"besked": spørgsmål[step], "step": step + 1, "session": session})


@app.route("/")
def index():
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True)

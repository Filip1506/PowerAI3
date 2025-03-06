from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        navn = request.form["navn"]
        alder = request.form["alder"]
        by = request.form["by"]
        return f"Tak for dit svar! Navn: {navn}, Alder: {alder}, By: {by}"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
from inspiration_engine import InspirationEngine

app = Flask(__name__)

engine = InspirationEngine()

@app.route("/", methods=["GET","POST"])
def home():

    result = None

    if request.method == "POST":

        subject = request.form["subject"]

        result = engine.solve(subject)

    return render_template("index.html", result=result)

app.run(host="0.0.0.0", port=3000)

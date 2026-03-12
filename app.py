from flask import Flask, render_template, request
from inspiration_engine_enhanced import InspirationEngine

app = Flask(__name__)

engine = InspirationEngine()


@app.route("/", methods=["GET","POST"])
def home():

    result = None

    if request.method == "POST":

        if request.form.get("mode") == "discover":

            result = engine.discovery_mode()

        else:

            subject = request.form["subject"]

            result = engine.solve(subject)

    return render_template("index.html", result=result)


app.run(host="0.0.0.0", port=5000)
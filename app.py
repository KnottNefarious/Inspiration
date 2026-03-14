from flask import Flask, render_template, request
import traceback

# UPDATE THIS LINE to match your current engine file
from inspiration_engine_phase2 import InspirationEngine

app = Flask(__name__)

engine = InspirationEngine()


@app.route("/", methods=["GET","POST"])
def home():

    result = None
    error = None

    if request.method == "POST":

        try:
            if request.form.get("mode") == "discover":

                result = engine.discovery_mode()

            else:

                subject = request.form.get("subject", "")

                result = engine.solve(subject)

        except Exception as e:
            # Capture the full error
            error = {
                'message': str(e),
                'traceback': traceback.format_exc(),
                'type': type(e).__name__
            }

    return render_template("index.html", result=result, error=error)


app.run(host="0.0.0.0", port=5000)

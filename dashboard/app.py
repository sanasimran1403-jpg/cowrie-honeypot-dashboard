from flask import Flask, render_template
from parse_data import get_dashboard_data

app = Flask(__name__)

@app.route("/")
def dashboard():
    data = get_dashboard_data()
    return render_template("dashboard.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

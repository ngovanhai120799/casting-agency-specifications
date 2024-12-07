from flask import Flask

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"
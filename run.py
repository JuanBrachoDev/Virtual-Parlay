import os
from flask import Flask, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    topics = list(mongo.db.topics.find())
    return render_template("index.html", topics=topics)


@app.route("/discussion")
def discussion():
    return render_template("discussion.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/edit_profile")
def edit_profile():
    return render_template("edit_profile.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
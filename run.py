import os
from flask import (
    Flask, flash, render_template,
     redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            flash("Account already exists")
            return redirect(url_for("register"))

        register = {
            "rank": "user",
            "display_name": request.form.get("display_name").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "profile_picture": "default.jpg",
            "posts": "0",
            "password_status": "set",
        }
        mongo.db.users.insert_one(register)

        # Put the new user into 'session' cookie
        session["display_name"] = request.form.get("display_name").lower()
        session["email"] = request.form.get("email").lower()
        flash("Registration Successful!")
        return redirect(url_for(
            "profile",
            display_name=session["display_name"],
            email=session["email"]))
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    flash("You have been logged out.")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
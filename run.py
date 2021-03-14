import os
from datetime import datetime
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
@app.route("/index", methods=["GET", "POST"])
def index():
    
    topics = list(mongo.db.topics.find())

    if request.method == "POST":
        submit = {
            "author": session['user_id'],
            "author_name": session['display_name'],
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "posts": "0",
            "date": datetime.now()
        }
        mongo.db.topics.insert_one(submit)
        flash("Topic Successfully Updated")
        return redirect(url_for("index"))

    return render_template("index.html", topics=topics)


@app.route("/edit_topic/<topic>", methods=["GET", "POST"])
def edit_topic(topic):

    topic_info = mongo.db.topics.find_one({'_id': ObjectId(topic)})

    if request.method == "POST":
        submit = {
            "author": topic_info['author'],
            "author_name": topic_info['author_name'],
            "title": request.form.get("topic_title"),
            "description": request.form.get("topic_description"),
            "posts": topic_info['posts'],
            "date": topic_info['date']
        }
        mongo.db.topics.update({"_id": ObjectId(topic)}, submit)
        flash("Topic Successfully Updated")

    return redirect(url_for("discussion", topic=topic_info['_id']))


@app.route("/delete_topic/<topic>")
def delete_topic(topic):
    mongo.db.topics.remove({"_id": ObjectId(topic)})
    flash("Topic has been deleted.")
    return redirect(url_for("index"))


@app.route("/discussion/<topic>", methods=["GET", "POST"])
def discussion(topic):

    topic_info = mongo.db.topics.find_one({'_id': ObjectId(topic)})
    posts = list(mongo.db.posts.find({'topic': topic}))

    if request.method == "POST":
        submit = {
            "topic": topic,
            "author": session['user_id'],
            "date": datetime.now(),
            "post": request.form.get("post")
        }
        mongo.db.posts.insert_one(submit)
        return redirect(url_for("discussion", topic=topic))

    return render_template(
        "discussion.html", topic_info=topic_info, posts=posts)


@app.route("/profile/<user_id>")
def profile(user_id):

    user = mongo.db.users.find_one(
            {"_id": ObjectId(user_id)})

    return render_template("profile.html", user=user)


@app.route("/edit_profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):

    user = mongo.db.users.find_one(
            {"_id": ObjectId(user_id)})

    if request.method == "POST":
        submit = {
            "rank": "user",
            "display_name": request.form.get("display_name"),
            "email": user['email'],
            "password": user['password'],
            "profile_picture": request.form.get("profile_picture"),
            "posts": user['posts'],
            "password_status": "set"
        }
        mongo.db.users.update({"_id": ObjectId(user_id)}, submit)
        flash("Profile Successfully Updated")

    if user_id == session['user_id']:
        return render_template("edit_profile.html", user=user)
    
    return redirect(url_for("index"))


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
            "display_name": request.form.get("display_name"),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "profile_picture": "default.png",
            "posts": "0",
            "password_status": "set",
        }
        mongo.db.users.insert_one(register)

        # Put the new user into 'session' cookie
        session['display_name'] = register['display_name']
        user_id = str(mongo.db.users.find_one(
        {"email": register["email"]})["_id"])
        flash("Registration Successful!")
        session['user_id'] = user_id
        return redirect(url_for(
            "profile",
            user_id=user_id))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if usernarme exists in db
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            # Ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"],
                request.form.get("password")):
                session["display_name"] = existing_user["display_name"]
                session["user_id"] = str(existing_user["_id"])
                flash("Welcome, {}".format(existing_user["display_name"]))
                return redirect(url_for(
                    "profile",
                    user_id=session["user_id"]))
            else:
                # Invalid passwords match
                flash("Incorrect Email and/or Password")
                return redirect(url_for("login"))

        else:
            # Username doesn't exist
            flash("Incorrect Email and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    flash("You have been logged out.")
    session.pop("display_name")
    session.pop("user_id")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
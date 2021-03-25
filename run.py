import os
from datetime import datetime
import shutil
from flask import (
    Flask, flash, render_template, send_from_directory,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

# App config
app = Flask(__name__) 

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['UPLOAD_FOLDER'] = f'{app.root_path}/profile_images/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.environ.get("SECRET_KEY")

# Database
mongo = PyMongo(app)


# Helper route to load images stored in profile_images
@app.route("/send_file/<filename>")
def send_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# Helper functions for routes

# Checks if the user owns the topic/post or is admin, shows message to user
# if 'False'
def check_owner_or_admin(author):
    if author == session['user_id'] or session['rank'] == 'admin':
        return True
    else:
        flash("You are not the owner.")
        return False


# Grabs topics collection from db
def fetch_topics():
    return list(mongo.db.topics.find())


# Grabs single topic based on the id
def fetch_single_topic(topic_id):
    topic_info = mongo.db.topics.find_one({'_id': ObjectId(topic_id)})
    return topic_info


# Checks if user is logged in
def check_user_is_logged_in():
    if session.get('user_id') is not None:
        return True


# Creates insert topic document dict
def create_topic_document():
    topic = {
        "author": session['user_id'],
        "author_name": session['display_name'],
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "posts": 0,
        "date": datetime.now().strftime("%d %b")
    }
    return topic


# Creates new topic document, inserts into db, flashes a message confirming
# the insertion
def insert_new_topic():
    submit = create_topic_document()
    mongo.db.topics.insert_one(submit)
    flash("Topic Successfully Created")


# Creates update topic document dict
def update_topic_document(topic_info):
    topic = {
        "author": topic_info['author'],
        "author_name": topic_info['author_name'],
        "title": request.form.get("topic_title"),
        "description": request.form.get("topic_description"),
        "posts": topic_info['posts'],
        "date": topic_info['date']
    }
    return topic


# Creates update topic document, update db and flashes message confirming the
# update
def update_topic(topic_info):
    if check_owner_or_admin(topic_info['author']):
        submit = update_topic_document(topic_info)
        mongo.db.topics.update({"_id": topic_info["_id"]}, submit)
        flash("Topic Successfully Updated")


# Deletes topic from db and flashes message confirming deletion
def remove_topic(topic_id):
    topic_info = fetch_single_topic(topic_id)
    if check_owner_or_admin(topic_info['author']):
        mongo.db.topics.remove({"_id": ObjectId(topic_id)})
        flash("Topic has been deleted.")


# Fetch topic from db and all associated posts
def fetch_topic_and_posts(topic):
    topic_info = mongo.db.topics.find_one({'_id': ObjectId(topic)})
    posts = list(mongo.db.posts.find({'topic': topic}))
    return topic_info, posts


# Creates insert post document dict
def create_post_document(topic):
    post = {
        "topic": topic,
        "author": session['user_id'],
        "date": datetime.now(),
        "post": request.form.get("post")
    }
    return post


# Fetch user from db
def fetch_user(user_id):
    user = mongo.db.users.find_one(
        {"_id": ObjectId(user_id)})
    return user


# Modifies post count for user and topic
def modify_post_count(topic, author, amount):
    mongo.db.topics.update_one({"_id": ObjectId(topic)}, {
                            "$inc": {"posts": amount}})
    mongo.db.users.update_one({"_id": ObjectId(author)}, {
                            "$inc": {"posts": amount}})


# Insert post into db
def insert_new_post(topic):
    post = create_post_document(topic)
    # Insert new post into db
    mongo.db.posts.insert_one(post)
    # Increase post counts for the post and the user
    modify_post_count(topic, post['author'], 1)


# Grabs post from db
def fetch_post(post_id):
    post = mongo.db.posts.find_one({'_id': ObjectId(post_id)})
    return post


# Creates update post document dict
def update_post_document(post_info):
    post = {
        "topic": post_info['topic'],
        "author": post_info['author'],
        "date": post_info['date'],
        "post": request.form.get(f"post_edit_{post_info['_id']}")
    }
    return post


# Updates post and flashes message confirming changes
def update_post(post_info):
    if check_owner_or_admin(post_info['author']):
        post = update_post_document(post_info)
        mongo.db.posts.update({"_id": post_info['_id']}, post)
        flash("Post Successfully Updated")


# Modifies post count for topic and user, deletes post and flashes message
# confirming changes
def remove_post(post):
    if check_owner_or_admin(post['author']):
        modify_post_count(post['topic'], post['author'], -1)
        # Delete post from db and flash message confirming deletion
        mongo.db.posts.delete_one({"_id": ObjectId(post['_id'])})
        flash("Post has been deleted.")


# Saves image in upload folder and grabs filename to save in db
def save_profile_image():
    profile_image = request.files['profile_picture']
    filename = session['user_id']
    profile_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


# Creates update user document dict
def update_user_document(user):
    submit = {
        "rank": "user",
        "display_name": request.form.get("display_name"),
        "email": user['email'],
        "password": user['password'],
        "posts": user['posts'],
    }
    return submit


# Saves profile image, updates user in db, updates cookies and shows
# message confirming update
def update_user(user):
    if check_owner_or_admin(user['_id']):
        save_profile_image()
        submit = update_user_document(user)
        mongo.db.users.update({"_id": ObjectId(user['_id'])}, submit)
        session['display_name'] = submit['display_name']
        flash("Profile Successfully Updated")


# Fetch user from db
def check_user_registered():
    existing_user = mongo.db.users.find_one(
        {"email": request.form.get("email").lower()})
    return existing_user


# Creates register user document dict
def register_user_document():
    # Inserts new user into db
    register = {
        "rank": "user",
        "display_name": request.form.get("display_name"),
        "email": request.form.get("email").lower(),
        "password": generate_password_hash(request.form.get("password")),
        "posts": 0,
    }
    return register


# Create a copy of default.png and save it in profile_images
def set_profile_picture(user_id):
    shutil.copyfile(f'{app.config["UPLOAD_FOLDER"]}default.png',
                    f'{app.config["UPLOAD_FOLDER"]}{user_id}')


# Put the new user's name and _id into 'session' cookie, shows
# message confirming registration
def set_cookies(register, user_id):
    session['display_name'] = register['display_name']
    session['rank'] = register['rank']
    session['user_id'] = user_id


# Inserts new user into db, sets default profile picture and sets cookies
def register_user():
    register = register_user_document()
    mongo.db.users.insert_one(register)
    user_id = str(mongo.db.users.find_one(
        {"email": register["email"]})["_id"])
    set_profile_picture(user_id)
    set_cookies(register, user_id)
    flash("Registration Successful!")


# Logs user out, shows message confirming changes and
# deletes cookies
def clear_session():
    flash("You have been logged out.")
    session.pop("display_name")
    session.pop("user_id")
    session.pop("rank")


# Queries the topics collection according to the value entered
# in the search field and loads page with the results
def search_topics():
    query = request.form.get("search")
    topics = list(mongo.db.topics.find({"$text": {"$search": query}}))
    return topics


# Routes
@app.route("/")
@app.route("/index")
def index():

    # Fetch topics collection from db
    topics = fetch_topics()

    return render_template("index.html", topics=topics)


@app.route("/create_topic")
def create_topic():

    # Redirects user to login if no session exists
    if not check_user_is_logged_in():
        return redirect(url_for("login"))

    return render_template("create_topic.html")


@app.route("/insert_topic_in_database", methods=["POST"])
def insert_topic_in_database():

    # Redirects user to login if no session exists
    if not check_user_is_logged_in():
        return redirect(url_for("login"))

    # Create new topic, flash a message confirming the
    # insertion and reload page
    insert_new_topic()

    return redirect(url_for("index"))


@app.route("/edit_topic/<topic>", methods=["POST"])
def edit_topic(topic):

    if not check_user_is_logged_in():
        return redirect(url_for("login"))

    # Fetch topic info from db
    topic_info = fetch_single_topic(topic)

    # Update topic and flash message confirming changes
    update_topic(topic_info)

    return redirect(url_for("discussion", topic=topic_info['_id']))


@app.route("/delete_topic/<topic>")
def delete_topic(topic):

    if not check_user_is_logged_in():
        return redirect(url_for("login"))

    # Remove topic from db and flash message confirming deletion
    remove_topic(topic)

    return redirect(url_for("index"))


@app.route("/discussion/<topic>")
def discussion(topic):

    # Fetch topic info and posts within the topic from db
    topic_info, posts = fetch_topic_and_posts(topic)

    return render_template(
        "discussion.html", topic_info=topic_info, posts=posts)


@app.route("/create_post/<topic>", methods=["POST"])
def create_post(topic):

    # Redirects user to login if no session exists
    if not check_user_is_logged_in():
        return redirect(url_for("login"))

    insert_new_post(topic)

    return redirect(url_for("discussion", topic=topic))


@app.route("/edit_post/<post>", methods=["POST"])
def edit_post(post):

    # Redirects user to login if no session exists
    if not check_user_is_logged_in():
        return redirect(url_for("login"))

    # Fetch post from db
    post_info = fetch_post(post)

    # Update post
    update_post(post_info)

    return redirect(url_for("discussion", topic=post_info['topic']))


@app.route("/delete_post/<post>")
def delete_post(post):

    # Redirects user to login if no session exists
    if not check_user_is_logged_in():
        return redirect(url_for("login"))

    # Fetch post from db
    post_info = fetch_post(post)

    # Decrease post counts for the post and the user
    remove_post(post_info)

    return redirect(url_for("discussion", topic=post_info['topic']))


@app.route("/profile/<user_id>")
def profile(user_id):

    # Fetch user from db
    user = fetch_user(user_id)

    return render_template("profile.html", user=user)


@app.route("/edit_profile/<user_id>", methods=["GET"])
def edit_profile(user_id):

    # Fetch user from db
    user = fetch_user(user_id)

    # Allows user to edit own profile only if logged in, otherwise
    # redirect to main page
    if user_id == session['user_id']:
        return render_template("edit_profile.html", user=user)

    return redirect(url_for("index"))


@app.route("/update_user_details/<user_id>", methods=["POST"])
def update_user_details(user_id):

    # Fetch user from db
    user = fetch_user(user_id)

    # Stores profile image in db, updates user and flashes message
    # confirming changes, then redirects to updated profile page
    update_user(user)

    return redirect(url_for("profile", user_id=user_id))


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/insert_user_in_database", methods=["POST"])
def insert_user_in_database():

    # Check if username already exists in db
    existing_user = check_user_registered()

    # If session exists, redirects user to profile
    if check_user_is_logged_in():
        return redirect(url_for("profile", user_id=session['user_id']))

    # Shows message to user confirming that account already
    # exists and redirects to register
    if existing_user:
        flash("Account already exists")
        return redirect(url_for("register"))

    register_user()

    return redirect(url_for("profile", user_id=session['user_id']))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/validate_user", methods=["POST"])
def validate_user():

    # Check if usernarme exists in db
    existing_user = check_user_registered()

    # If session exists, redirects user to profile
    if check_user_is_logged_in():
        return redirect(url_for("profile", user_id=session['user_id']))

    if existing_user:
        # Ensures hashed password matches user input, sets cookies,
        # shows message welcoming user and redirects to profile
        if check_password_hash(
                existing_user["password"],
                request.form.get("password")):
            set_cookies(existing_user, str(existing_user["_id"]))
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


@app.route("/logout")
def logout():
    clear_session()
    return redirect(url_for("login"))


@app.route("/search", methods=["POST"])
def search():
    topics = search_topics()
    return render_template("index.html", topics=topics)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

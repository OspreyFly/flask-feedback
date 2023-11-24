from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    request,
    jsonify,
    session,
    abort,
)
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Feedback
from forms import RegisterUser, LoginUser, Feedback_form
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///user_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secretKEY"
bcrypt = Bcrypt(app)
connect_db(app)


@app.route("/")
def redir_register():
    session.clear()
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_form():
    form = RegisterUser()

    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful!", "success")
        session["username"] = f"{username}"
        return redirect("/login")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_form():
    form = LoginUser()

    if request.method == "POST" and form.validate_on_submit():
        password = form.password.data
        username = form.username.data

        user = User.verify_user(username, password)

        if user:
            # Login successful
            flash("Login Successful!", "success")
            session["username"] = f"{username}"
            return redirect("/users")
        else:
            # Login Unsuccesssful
            flash("Login Unsuccessful! Check your Username and Password.", "warning")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    try:
        if session["username"]:
            del session["username"]
            return redirect("/login")
    except KeyError:
        flash("Sign in first!", "warning")
        return redirect("/login")


@app.route("/users")
def users():
    try:
        if session["username"]:
            username = session["username"]
            return redirect(f"users/{username}")
    except KeyError:
        flash("Sign in first!", "warning")
        return redirect("/login")


@app.route("/users/<username>")
def user_detail(username):
    try:
        if session["username"]:
            user = User.query.get_or_404(username)
            if user is None:
                abort(404)  # User NOT FOUND

            feedback = user.feedback

            return render_template("user.html", user=user, feedback=feedback)

    except KeyError:
        flash("Sign in first!", "warning")
        return redirect("/login")


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    try:
        if session["username"]:
            user = User.query.get(username)

            db.session.delete(user)
            db.session.commit()

            return redirect("/")
    except KeyError:
        flash("Sign in first!", "warning")
        return redirect("/login")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    try:
        if session["username"]:
            form = Feedback_form()
            user = User.query.get_or_404(username)

            if not user:
                flash("Must be logged in!", "warning")
                return redirect("/login")

            if request.method == "POST":
                if request.is_json:
                    # Handle JSON data
                    data = request.get_json()
                    title = data.get("title")
                    content = data.get("content")

                    feedback = Feedback(title=title, content=content, user=user)
                    import pdb

                    pdb.set_trace()
                    db.session.add(feedback)
                    db.session.commit()

                    return jsonify({"message": "Feedback Saved"})

                elif form.validate_on_submit():
                    # Handle form data
                    title = form.title.data
                    content = form.content.data

                    feedback = Feedback(title=title, content=content, user=user)

                    db.session.add(feedback)
                    db.session.commit()

                    flash("Feedback Saved", "success")
                    return redirect(f"/users/{username}")

            return render_template("feedback.html", form=form, username=username)
    except KeyError:
        flash("Sign in first!", "warning")
        return redirect("/login")


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST", "DELETE"])
def manage_feedback(feedback_id):
    try:
        if session["username"]:
            form = Feedback_form()
            username = session["username"]
            user = User.query.get_or_404(username)

            if not user:
                flash("Must be logged in!", "warning")
                return redirect("/login")

            if request.method == "POST" and form.validate_on_submit():
                flash("Feedback Saved", "success")
                title = form.title.data
                content = form.content.data
                feedback = Feedback(title=title, content=content, user=user)

                db.session.add(feedback)
                db.session.commit()

                return redirect(f"/users/{username}")

            if request.method == "DELETE":
                target = Feedback.query.get_or_404(feedback_id)
                db.session.delete(target)
                db.session.commit()
                redirect(f"/users/{user.username}")

            feedback = Feedback.query.all()

            return render_template(
                "feedback.html", form=form, user=user, feedback=feedback
            )
    except KeyError:
        flash("Sign in first!", "warning")
        return redirect("/login")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)

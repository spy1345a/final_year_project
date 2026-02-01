from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")

load_dotenv(dotenv_path=ENV_PATH)

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")
FASTAPI_URL = os.getenv("FASTAPI_URL")

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        response = requests.post(
            f"{FASTAPI_URL}/login",
            data={
                "username": username,
                "password": password
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code == 200:
            token = response.json()["access_token"]
            session["token"] = token
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid login")

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    token = session.get("token")
    if not token:
        return redirect(url_for("login"))

    response = requests.get(
        f"{FASTAPI_URL}/profile",
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code != 200:
        return redirect(url_for("login"))

    user = response.json()
    return render_template("dashboard.html", user=user)

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        response = requests.post(
            f"{FASTAPI_URL}/signup",
            json={
                "username": username,
                "password": password
            }
        )

        if response.status_code != 200:
            return render_template(
                "signup.html",
                error=response.json().get("detail", "Signup failed")
            )

        return redirect(url_for("login"))

    # GET request — no error yet
    return render_template("signup.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

#------------USERS LIST---------------
@app.route("/users")
def users_page():
    token = session.get("token")
    if not token:
        return redirect(url_for("login"))

    response = requests.get(
        f"{FASTAPI_URL}/users",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if response.status_code == 403:
        return render_template(
            "error.html",
            message="You don’t have permission to view this page."
        )

    if response.status_code != 200:
        return render_template(
            "error.html",
            message="Something went wrong. Please try again."
        )

    users = response.json()
    return render_template("users.html", users=users)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(os.getenv("DEBUG"))

from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os
from dotenv import load_dotenv
from spellchecker import SpellChecker
import re


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")

load_dotenv(dotenv_path=ENV_PATH)

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")
FASTAPI_URL = os.getenv("FASTAPI_URL")


#------------ PROSSING ---------------
spell = SpellChecker()
def normalize_text(text: str) -> str:
    if not text:
        return ""

    # trim spaces
    text = text.strip()

    # lowercase
    text = text.lower()

    # remove weird characters
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # spelling correction
    corrected_words = []
    for word in text.split():
        corrected_words.append(spell.correction(word) or word)

    return " ".join(corrected_words)


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
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    token = session.get("token")
    if not token:
        return redirect(url_for("login"))

    # Get user profile from FastAPI
    response = requests.get(
        f"{FASTAPI_URL}/profile",
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code != 200:
        return redirect(url_for("login"))

    user = response.json()
    prediction = None

    # -------- POST: Prediction --------
    if request.method == "POST":

        raw_text = request.form.get("text", "")

        # normalize input
        cleaned_text = normalize_text(raw_text)

        # avoid empty submissions
        if cleaned_text:

            pred_response = requests.post(
                f"{FASTAPI_URL}/predict",
                json={"text": cleaned_text},
                headers={"Authorization": f"Bearer {token}"}
            )

            if pred_response.status_code == 200:
                prediction = pred_response.json().get("prediction")

    return render_template(
        "dashboard.html",
        user=user,
        prediction=prediction
    )

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
    app.run()

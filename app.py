from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change_this_later"

def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

# -------- CREATE TABLES --------
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            completed INTEGER DEFAULT 0,
            user_id INTEGER
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry TEXT,
            date TEXT,
            user_id INTEGER
        )
    """)

# -------- AUTH PAGES --------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            return "Passwords do not match"

        hashed = generate_password_hash(password)
        try:
            with get_db() as db:
                db.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, hashed)
                )
            return redirect("/login")
        except:
            return "Username already exists"

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect("/")
        return "Invalid username or password"

    return render_template("login.html")

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        username = request.form["username"]
        new_pass = request.form["password"]
        confirm = request.form["confirm"]

        if new_pass != confirm:
            return "Passwords do not match"

        hashed = generate_password_hash(new_pass)
        with get_db() as db:
            db.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (hashed, username)
            )
        return redirect("/login")

    return render_template("forgot.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# -------- PROTECTED PAGES --------
@app.route("/")
def todo_page():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("todo.html")

@app.route("/diary")
def diary_page():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("diary.html")

# -------- TODO API --------
@app.route("/add_task", methods=["POST"])
def add_task():
    with get_db() as db:
        db.execute(
            "INSERT INTO todos (task, user_id) VALUES (?, ?)",
            (request.json["task"], session["user_id"])
        )
    return jsonify(success=True)

@app.route("/get_tasks")
def get_tasks():
    db = get_db()
    tasks = db.execute(
        "SELECT * FROM todos WHERE user_id = ?",
        (session["user_id"],)
    ).fetchall()
    return jsonify([dict(t) for t in tasks])

@app.route("/toggle/<int:id>", methods=["PUT"])
def toggle_task(id):
    with get_db() as db:
        db.execute(
            "UPDATE todos SET completed = 1-completed WHERE id = ?",
            (id,)
        )
    return jsonify(success=True)

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_task(id):
    with get_db() as db:
        db.execute("DELETE FROM todos WHERE id = ?", (id,))
    return jsonify(success=True)

# -------- DIARY API --------
@app.route("/add_diary", methods=["POST"])
def add_diary():
    with get_db() as db:
        db.execute(
            "INSERT INTO diary (entry, date, user_id) VALUES (?, ?, ?)",
            (
                request.json["entry"],
                datetime.now().strftime("%d %B %Y"),
                session["user_id"]
            )
        )
    return jsonify(success=True)

@app.route("/get_diary")
def get_diary():
    db = get_db()
    entries = db.execute(
        "SELECT * FROM diary WHERE user_id = ? ORDER BY id DESC",
        (session["user_id"],)
    ).fetchall()
    return jsonify([dict(e) for e in entries])

if __name__ == "__main__":
    app.run(debug=True)

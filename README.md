# 📝 Secure Personal Diary & To-Do Checklist App

A full‑stack web application that allows users to securely manage personal to‑do lists and private diary entries. The application focuses on **user authentication, data privacy, and encryption**, making it suitable for academic projects and portfolio use.

---

## 🚀 Features

* 🔐 User Signup, Login, Logout
* 🔁 Forgot Password with Confirm Password validation
* ✅ Personal To‑Do Checklist (Add, Tick, Delete)
* 📔 Personal Diary on a Separate Page
* 📔 Private diary entries stored securely in the database

---

## 📁 Project Structure

```
todo_app/
│
├── app.py
├── todo.db
│
├── templates/
│   ├── login.html
│   ├── signup.html
│   ├── forgot.html
│   ├── todo.html
│   └── diary.html
│
└── static/
    ├── style.css
    ├── script.js
    └── bg.jpg
```

---

## ⚙️ Installation & Setup

1. Clone the repository

```bash
git clone <repository-url>
cd todo_app
```
2. Run the application

```bash
python app.py
```

3. Open browser

```
http://127.0.0.1:5000
```

---

## 🔐 Security Implementation

* Passwords are hashed before storage
* Session-based authentication ensures user privacy
* Each user can access only their own checklist and diary entries
* Unauthorized users cannot access protected pages
* Unauthorized users cannot access checklist or diary pages

---

## 📌 Usage Flow

1. Sign up with username and password
2. Login to access checklist
3. Manage daily tasks
4. Navigate to diary page to write personal entries
5. Logout securely

---

🎓 Academic Relevance

This project demonstrates:

* Full‑stack web development
* Secure authentication mechanisms
* Database design and user‑specific access control

Suitable for **college projects, mini projects, and portfolios**.

## 📄 License

This project is for educational use.

---

✨ *Built as a privacy‑focused personal productivity application.*

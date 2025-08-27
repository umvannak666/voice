# app.py
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secretkey123"

# ======= USERS =======
USERS = {
    "student1": "1234",
    "student2": "abcd",
    "student3": "5678"
}

# ======= ROUTES =======
@app.route("/", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in USERS and USERS[username] == password:
            session["logged_in"] = True
            session["user"] = username
            return redirect(url_for("reading_test"))
        else:
            msg = "ឈ្មោះអ្នកប្រើ ឬ ពាក្យសម្ងាត់មិនត្រឹមត្រូវ!"
    return render_template("login.html", msg=msg)

@app.route("/reading")
def reading_test():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("reading.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

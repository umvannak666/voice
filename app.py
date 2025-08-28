from flask import Flask, render_template, request, redirect, session, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secretkey123"

USERS = {
    "student1": "1234",
    "student2": "abcd",
    "student3": "5678"
}

RECORDINGS_FOLDER = "recordings"
if not os.path.exists(RECORDINGS_FOLDER):
    os.makedirs(RECORDINGS_FOLDER)

# ===== ROUTES =====
@app.route("/", methods=["GET","POST"])
def login():
    msg = ""
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in USERS and USERS[username]==password:
            session["logged_in"] = True
            session["user"] = username
            return redirect(url_for("choose_subject"))
        else:
            msg = "ឈ្មោះអ្នកប្រើ ឬ ពាក្យសម្ងាត់មិនត្រឹមត្រូវ!"
    return render_template("login.html", msg=msg)

# ===== Subject selection page =====
@app.route("/choose_subject", methods=["GET","POST"])
def choose_subject():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    subjects = ["តេស្តអំណាន","តេស្តស្តាប់","តេស្តនិយា"]
    if request.method=="POST":
        subject = request.form.get("subject")
        session["subject"] = subject
        return redirect(url_for("reading_test"))
    return render_template("choose_subject.html", subjects=subjects, user=session["user"])

@app.route("/reading")
def reading_test():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("reading.html", user=session["user"], subject=session.get("subject","Reading"))

@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    if not session.get("logged_in"):
        return "Unauthorized", 401
    file = request.files.get("audio_data")
    if file:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{session['user']}_{timestamp}.wav"
        filepath = os.path.join(RECORDINGS_FOLDER, filename)
        file.save(filepath)
        return "Saved!"
    return "No file uploaded", 400

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__=="__main__":
    app.run(debug=True)

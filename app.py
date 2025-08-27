from flask import Flask, render_template, flash, session

app = Flask(__name__)
app.secret_key = "secretkey123"  # ចាំបាច់សម្រាប់ flash

@app.route("/")
def home():
    flash("Welcome to the Home Page!")
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

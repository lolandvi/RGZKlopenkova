from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def start():
    return redirect("/mainpage", code=302)

@app.route("/mainpage")
def mainpage():
    return render_template('index.html')
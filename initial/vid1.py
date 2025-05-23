from flask import Flask, redirect, url_for

app= Flask(__name__)

@app.route("/")
def home():
	return "Hello! this is the home page"

@app.route("/<name>")
def user(name):
	return f"Sairam {name} Sairam"

@app.route("/admin")
def admin():
	return redirect(url_for("home"))

if __name__ == "__main__":
	app.run()
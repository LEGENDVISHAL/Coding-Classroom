from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/home')
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/student')
def student():
    return render_template("student_dash.html")

if __name__ == "__main__":
    app.run(debug = True)

from flask import Flask, render_template, redirect, url_for, sessions

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/cv')
def my_cv():
    return render_template('ninad_cv.html')


@app.route('/paradimshift')
def pradimshift():
    return render_template('index2.html')

if __name__ == "__main__":
    app.run(debug=True)
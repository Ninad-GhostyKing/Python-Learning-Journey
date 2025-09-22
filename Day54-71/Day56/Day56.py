from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def identity():
    return render_template('Identity.html')

if __name__ == "__main__":
    app.run(debug=True)
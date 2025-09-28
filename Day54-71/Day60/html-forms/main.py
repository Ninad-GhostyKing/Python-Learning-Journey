from flask import Flask, render_template, url_for, request


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = None
    password = None
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        
    return render_template('login.html', name=username, password=password)


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, url_for
import random
import time
import requests

app = Flask(__name__)


@app.route('/')
def index():
    random_number = random.randint(0,9)
    current_year = time.strftime("%Y")
    return render_template('index.html', num=random_number, c_year=current_year)

@app.route('/agify/<name>')
def age_prediction(name):
    gender_url = f"https://api.genderize.io?name={name}"
    agify_url = f"https://api.agify.io?name={name}"
    gender_response = requests.get(gender_url)
    gender_data = gender_response.json()
    agify_response = requests.get(agify_url)
    agify_data = agify_response.json()
    gender = gender_data["gender"]
    age = agify_data["age"]
    return render_template('agify.html', name=name, gender=gender, age=age)


@app.route('/bigblogger')
def get_blog():
    blog_url = "https://api.npoint.io/d77885cd0fb1bd3ae804"
    blog_response = requests.get(blog_url)
    all_post = blog_response.json()
    return render_template('blog.html', all_post=all_post)


if __name__ == "__main__":
    app.run(debug=True)
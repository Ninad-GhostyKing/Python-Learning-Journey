from flask import Flask, render_template, url_for
import requests
from post import Post

app = Flask(__name__)

blog_url = "https://api.npoint.io/d77885cd0fb1bd3ae804"
response = requests.get(blog_url)
blog_data = response.json()

all_blogs = []

for blog in blog_data:
    blog_object  = Post(blog['id'], blog['title'], blog['subtitle'], blog['body'],blog['image_url'])
    all_blogs.append(blog_object)

@app.route("/")
def home():
    return render_template("index.html", posts = all_blogs )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:id>")
def post(id):
    requested_post = None
    for post in all_blogs:
        if post.id == id:
            requested_post = post
    return render_template("post.html", post= requested_post )


if __name__ == "__main__":
    app.run(debug=True)

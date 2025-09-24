from flask import Flask, render_template
import requests
from post import Post

app = Flask(__name__)

# Getting all posts from blog.
blog_url = "https://api.npoint.io/d77885cd0fb1bd3ae804"
blog_response = requests.get(blog_url)
blog_data = blog_response.json()

post_objects = []
for blog in blog_data:
    post_obj = Post(blog['id'], blog['title'], blog['subtitle'], blog['body'])
    post_objects.append(post_obj)


@app.route('/')
def home():
    return render_template("index.html", posts=post_objects)

@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for post in post_objects:
        if index==post.id:
            requested_post = post
    if requested_post == None:
        return "Error 404 Object Not Found!!"
    return render_template('post.html', blog=requested_post)


if __name__ == "__main__":
    app.run(debug=True)

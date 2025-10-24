from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import requests, pathlib, random

"""
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
"""

app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap5(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


# Connect to Database
CUR_DIR = pathlib.Path(__file__).parent
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(
    CUR_DIR / "instance/posts.db"
)
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


# FormClass
class BlogForm(FlaskForm):
    # id = StringField("Blog Id")
    title = StringField("Blog Title", validators=[DataRequired()])
    subtitle = StringField("Blog Subtitle", validators=[DataRequired()])
    date = StringField("Published Date", validators=[DataRequired()])
    author = StringField("Author Name", validators=[DataRequired()])
    img_url = StringField("Image Url", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Body", validators=[DataRequired()])
    submit = SubmitField("Publish")

ckeditor = CKEditor(app)


@app.route("/")
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    all_blogs = db.session.execute(db.select(BlogPost)).scalars()
    posts = [
        {
            "id": b.id,
            "title": b.title,
            "subtitle": b.subtitle,
            "date": b.date,
            "body": b.body,
            "author": b.author,
            "img_url": b.img_url,
        }
        for b in all_blogs
    ]
    return render_template("index.html", all_posts=posts)


# TODO: Add a route so that you can click on individual posts.
@app.route("/blog/<int:post_id>")
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route("/new-post", methods=['GET', 'POST'])
def add_new_post():
    form = BlogForm()
    heading = "New Post"
    if form.validate_on_submit():
        print("submitted")
        new_post = BlogPost(
            title = form.title.data,
            subtitle = form.subtitle.data,
            body = form.body.data,
            date = form.date.data,
            author = form.author.data,
            img_url = form.img_url.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=form , heading=heading)

# TODO: edit_post() to change an existing blog post
@app.route('/edit_post/<int:post_id>', methods=['GET','POST'])
def edit_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    form = BlogForm(obj=requested_post)
    heading = "Edit Post"
    if form.validate_on_submit():
        requested_post.title = form.title.data
        requested_post.subtitle = form.subtitle.data
        requested_post.body = form.body.data
        requested_post.author = form.author.data
        # requested_post.date = form.date.data
        requested_post.img_url = form.img_url.data
        db.session.commit()
        return redirect(url_for('show_post', post_id=requested_post.id))
    return render_template('make-post.html', form=form, heading=heading)

# TODO: delete_post() to remove a blog post from the database
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    db.session.delete(instance=requested_post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)

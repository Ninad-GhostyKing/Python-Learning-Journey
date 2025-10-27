from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor

# from flask_gravatar import Gravatar # doesn't support from Flask 3.0.0 instead a function of gravatar_url is used.
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, LoginForm, RegisterForm, CommentForm
import os, dotenv, pathlib, typing, hashlib, datetime, smtplib


"""
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
"""

dotenv.load_dotenv("Python-Learning-Journey/.env")
CUR_DIR = pathlib.Path(__file__).parent
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
ckeditor = CKEditor(app)

Bootstrap5(app)

# TODO: Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(CUR_DIR / "instance/blog.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES


# RELATIONAL DATABASE
# PARENT DB
class User(db.Model, UserMixin):
    __tablename__ = "blog_users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    children_blog: Mapped[typing.List["BlogPost"]] = relationship(
        back_populates="parent_user"
    )
    comment_blog: Mapped[typing.List["BlogComment"]] = relationship(
        back_populates="parent_user_b"
    )


# CHILD DB
class BlogPost(db.Model, UserMixin):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("blog_users.id"))
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    parent_user: Mapped["User"] = relationship(back_populates="children_blog")
    comments: Mapped[typing.List["BlogComment"]] = relationship(
        back_populates="parent_post"
    )


# CHILD DB
class BlogComment(db.Model, UserMixin):
    __table__name = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("blog_users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("blog_posts.id"))
    author: Mapped[int] = mapped_column(String(250), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    parent_user_b: Mapped["User"] = relationship(back_populates="comment_blog")
    parent_post: Mapped["BlogPost"] = relationship(back_populates="comments")


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, ident=user_id)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def gravatar_url(email, size=100, rating="g", default="retro", force_default=False):
    hash_value = hashlib.md5(email.lower().encode("utf-8")).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_value}?s={size}&d={default}&r={rating}&f={force_default}"


# TODO: Use Werkzeug to hash the user's password when creating a new user.
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        if db.session.execute(db.select(User).where(User.email == email)).scalar():
            flash("You've already signed up with this email, log in instead.")
            return redirect(url_for("login"))
        hashed_psw = generate_password_hash(
            form.password.data, method="pbkdf2:sha256", salt_length=8
        )
        new_user = User(username=form.username.data, email=email, password=hashed_psw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


# TODO: Retrieve a user from the database based on their email.
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        existed_user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar()
        if existed_user:
            if check_password_hash(existed_user.password, password):
                login_user(user=existed_user)
                return redirect(url_for("get_all_posts"))
            else:
                flash("Incorrect Password!!")
        else:
            flash(
                "That Email does not exist or incorrect, please try again or register"
            )

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("get_all_posts"))


@app.route("/")
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    if current_user.is_authenticated:
        print(current_user.username)
    return render_template("index.html", all_posts=posts, logged_in=login_checker())


# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    requested_post = db.get_or_404(BlogPost, post_id)
    if form.validate_on_submit():
        new_comment = BlogComment(
            author_id=current_user.id,
            post_id=post_id,
            author=current_user.username,
            text=form.comment.data,
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))
    comments_data = db.session.execute(
        db.select(BlogComment).where(BlogComment.post_id == post_id)
    ).scalars()
    all_comments = [comment for comment in comments_data]
    return render_template(
        "post.html",
        post=requested_post,
        form=form,
        comments=all_comments,
        gravatar_url=gravatar_url,
        logged_in=login_checker(),
    )


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@login_required
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            author_id=current_user.id,
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user.username,
            date=date.today().strftime("%B %d, %Y"),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, logged_in=login_checker())


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(obj=post)
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template(
        "make-post.html", form=edit_form, is_edit=True, logged_in=login_checker()
    )


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


@app.route("/about")
def about():
    return render_template("about.html")


# @app.route("/contact")
# def contact():
#     print(MAIL_ADDRESS)
#     return render_template("contact.html")


MAIL_ADDRESS = os.environ.get("MY_EMAIL")
MAIL_APP_PW = os.environ.get("MY_EMAIL_PASSWORD")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    print(MAIL_ADDRESS,MAIL_APP_PW)
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MAIL_ADDRESS, MAIL_APP_PW)
        connection.sendmail(MAIL_ADDRESS, email, email_message)


def login_checker():
    return current_user.is_authenticated


if __name__ == "__main__":
    app.run(debug=True, port=5001)

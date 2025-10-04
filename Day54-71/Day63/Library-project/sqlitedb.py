# import sqlite3

# db = sqlite3.connect("books-collection.db")

# cursor = db.cursor()

# # cursor.execute("CREATE TABLE books(id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")

# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J.K.Rowling', '9.3')")
# db.commit()

from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import pathlib, os, dotenv

CUR_DIR = pathlib.Path(__file__).parent

# Class 
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.secret_key = "aabb"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + str(CUR_DIR) + "/new-books-collection.db"
)
db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float(10), nullable=False)


with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD
        new_book = Book(
            title=request.form["title"], # type: ignore
            author=request.form["author"], # type: ignore
            rating=request.form["rating"], # type: ignore
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import dotenv, os, pathlib

"""
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
"""

CUR_DIR = pathlib.Path(__file__).parent

dotenv.load_dotenv(
    "Python-Learning-Journey/.env"
)

# Class


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(
    CUR_DIR / "new-books-collection.db"
)
db.init_app(app=app)


# Class


class Book(db.Model):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
    )
    title: Mapped[str] = mapped_column(
        String(250),
        unique=True,
        nullable=False,
    )
    author: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
    )
    book_rating: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    with app.app_context():
        all_books = [] 
        books = db.session.execute(db.select(Book)).scalars()
        for b in books:
            book = {
                'id'    : b.id,
                'title' : b.title,
                'author' : b.author,
                'rating' : b.book_rating
            }
            all_books.append(book)
    return render_template("index.html", books=all_books)


# @app.route("/add", methods=['GET', 'POST'])
# def add():
#     if request.method=='POST':
#         book_name = request.form['book_name']
#         author_name = request.form['author_name']
#         book_rating = request.form['book_rating']
#         book_dict = {
#             "name" : book_name.capitalize(),
#             "author" : author_name.capitalize(),
#             "rating" : book_rating,
#         }
#         all_books.append(book_dict)
#         print(True)
#         return render_template('add.html')
#     return render_template('add.html')


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],  # type: ignore
            author=request.form["author"],  # type: ignore
            book_rating=request.form["rating"],  # type: ignore
        )
        with app.app_context():
            db.session.add(new_book)
            db.session.commit()
        return "Successfull" "<a href='/'>Home</a>\n" "<a href='/add'>Add</a>"
    return render_template("add.html")


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def update_book(id):
    with app.app_context():
        book_to_update = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
        if request.method == 'POST':
            new_rating = request.form['new_rating']
            book_to_update.book_rating = new_rating # type: ignore
            db.session.add(book_to_update)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('update.html', book=book_to_update)


# @app.route("/edit", methods=["GET", "POST"])
# def edit():
#     if request.method == "POST":
#         # UPDATE RECORD
#         book_id = request.form["id"]
#         book_to_update = db.get_or_404(Book, book_id)
#         book_to_update.rating = request.form["rating"]
#         db.session.commit()
#         return redirect(url_for("home"))
#     book_id = request.args.get("id")
#     book_selected = db.get_or_404(Book, book_id)
#     return render_template("edit_rating.html", book=book_selected)


@app.route('/delete/<int:id>')
def delete_book(id):
    with app.app_context():
        book_to_delete = db.get_or_404(Book, id)
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

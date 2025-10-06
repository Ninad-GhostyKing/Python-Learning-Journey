from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests, pathlib

"""
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
"""

# CONSTANTS
API_QUERY = ""
TMBD_API_URL = f"https://api.themoviedb.org/3/search/movie"
TMBD_API_MOVIE_DETAILS_URL = "https://api.themoviedb.org/3/movie"
TMBD_API_IMG_URL = "https://image.tmdb.org/t/p/w500"
TMBD_BEARER_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxMzQxYjUwM2JiZWJmNWY2NTdjYzUwMDM5YTYwMTAwMCIsIm5iZiI6MTc1OTY4NjY5OC4zNCwic3ViIjoiNjhlMmIwMmEyMGM1MmE3NDBjYzI3MjAxIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.a_lL8KUeqtD0M_Kj7cmlg8JrgV40pXGEn5Jd3EJXTHA"

app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

CUR_DIR = pathlib.Path(__file__).parent
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(CUR_DIR / "moviesproj.db")
db.init_app(app=app)


# CREATE TABLE
class Movies(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)


with app.app_context():
    db.create_all()


# Direct Data Entry


# WTF Forms


class EditForms(FlaskForm):
    rating = FloatField("Your Rating E.g. 7.5 out of 10", validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")


class AddMovieForm(FlaskForm):
    title = StringField("Title of the Movie", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Routes
@app.route("/")
def home():
    # all_movies = []
    # with app.app_context():
    # movies = db.session.execute(db.select(Movies)).scalars()
    # for m in movies:
    #     movie = {
    #         'id' : m.id,
    #         'title' : m.title,
    #         'year' : m.year,
    #         'description' : m.description,
    #         'rating' : m.rating,
    #         'ranking' : m.ranking,
    #         'review' : m.review,
    #         'img_url' : m.img_url,
    #     }
    #     all_movies.append(movie)
    result = db.session.execute(db.select(Movies).order_by(Movies.rating.desc()))
    all_movies = result.scalars()
    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = AddMovieForm()
    if form.validate_on_submit():
        TMBD_API_URL = f"https://api.themoviedb.org/3/search/movie"
        headers = {
            "accept" : "application/json",
            "Authorization" : f"Bearer {TMBD_BEARER_TOKEN}"
        }
        parameters = {
            "query" : form.title.data,
        }
        response = requests.get(TMBD_API_URL,headers=headers,params=parameters)
        data = response.json()["results"]
        
        return render_template('select.html', movies_data = data)
    return render_template("add.html", form=form)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    id = request.args.get("id")
    edit_form = EditForms()
    with app.app_context():
        # movie = db.session.execute(db.select(Movies).where(Movies.id == id)).scalar()
        movie = db.get_or_404(Movies, id)

        # if request.method == 'POST':
        if edit_form.validate_on_submit():
            movie.rating = request.form["rating"]  # type: ignore
            movie.review = request.form["review"]
            db.session.add(movie)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("edit.html", form=edit_form, movie=movie)


@app.route("/delete")
def delete_movie():
    id = request.args.get("id")
    movie = db.get_or_404(Movies, id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


@app.route('/search')
def search_movie():
    movie_id = request.args.get("id")
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMBD_BEARER_TOKEN}",
    }
    url = f"{TMBD_API_MOVIE_DETAILS_URL}/{movie_id}"
    response = requests.get(url, headers=headers)
    data = response.json()
    with app.app_context():
        movie = Movies(
            title = data['title'],
            year = data['release_date'].split('-')[0],
            description = data['overview'],
            rating = round(data['vote_average'],1),
            ranking = 0,
            review = "",
            img_url = f"{TMBD_API_IMG_URL}{data['poster_path']}"
        )
        db.session.add(movie)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)


# In your forms.py:
# from wtforms import ValidationError


# def UniqueMovie(form, field):
#     with app.app_context():
#         if db.session.execute(
#             db.select(Movies).where(Movies.title == field.data)
#         ).scalar_one_or_none():
#             raise ValidationError("This title is already in the database.")


# class AddMovieForm(FlaskForm):
#     title = StringField("Title", validators=[DataRequired(), UniqueMovie])
#     # ... other fields

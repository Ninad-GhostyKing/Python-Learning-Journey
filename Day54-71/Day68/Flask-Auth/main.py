from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    send_from_directory,
    make_response,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    current_user,
    logout_user,
)
import pathlib, os, dotenv, functools

dotenv.load_dotenv("Python-Learning-Journey/.env")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


CUR_DIR = pathlib.Path(__file__).parent
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(
    CUR_DIR / "instance/users.db"
)
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE IN DB
class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# No Cache
def no_cache(view):
    """Decorator to add no-cache headers to a response."""

    @functools.wraps(view)
    def decorated_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    return decorated_view


@app.route("/")
def home():
    logged_in = login_checker()
    return render_template("index.html", logged_in=logged_in)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hash_pass = generate_password_hash(
            password=request.form["password"], method="pbkdf2:sha256", salt_length=8
        )
        new_user = User(
            email=request.form["email"],
            name=request.form["name"],
            password=hash_pass,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("secrets"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user:
            if check_password_hash(user.password, request.form["password"]):
                login_user(user)
                return redirect(url_for("secrets"))
            else:
                flash("Incorrect Password !!")
        else:
            flash("Invalid Email !!")
    return render_template("login.html")


@app.route("/secrets")
@login_required
@no_cache
def secrets():
    username = current_user.name
    logged_in = login_checker()
    return render_template("secrets.html", username=username, logged_in=logged_in)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/download/<path:name>")
@login_required
@no_cache
def download(name):
    return send_from_directory(
        directory="static",
        path=f"files/{name}",
    )


def login_checker():
    # return login_user(current_user) # The Working Logic but has security risk due to AnonomysMixin
    # print(current_user.is_authenticated)
    return current_user.is_authenticated


if __name__ == "__main__":
    app.run(debug=True)

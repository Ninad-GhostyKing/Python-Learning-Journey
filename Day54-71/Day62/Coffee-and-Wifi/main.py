from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, URLField, SelectField
from wtforms.validators import DataRequired, URL, ValidationError
import csv, dotenv, os, pathlib

"""
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
"""
dotenv.load_dotenv(
    "/home/ghostyking/Projects/Python100Days/Python-Learning-Journey/.env"
)

app = Flask(__name__)
# app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.secret_key = os.getenv("SECRET_KEY")
bootstrap = Bootstrap5(app)

# Data Paths
CAFE_CSV_PATH = pathlib.Path(__file__).parent / "cafe-data.csv"


# Custom Validator methods

GOOGLE_MAPS_HEADERS = (
    "https://www.google.com/maps/",
    "http://maps.google.com/",
    "http://www.google.com/maps/",
    "https://goo.gl/maps/",  # For shortened links, though less common now
)


def GoogleMapsURL(form, field):
    """Custom validator to check if the URL is a Google Maps link."""
    url = field.data

    # Optional: Basic check to ensure it's a URL first (though URLField does this)
    if not url:
        return

    # Check if the URL starts with any of the valid headers
    if not url.startswith(GOOGLE_MAPS_HEADERS):
        # Raise ValidationError if the link is not a Google Maps URL
        raise ValidationError(
            "The link must be a valid Google Maps URL (e.g., starting with https://www.google.com/maps/)"
        )


# Form Class

class CafeForm(FlaskForm):
    cafe = StringField("Cafe name", validators=[DataRequired()])
    location = URLField(
        "Location of Cafe on Google Maps (URL)", validators=[DataRequired(),URL(message="Must be a valid URL."),GoogleMapsURL]
    )
    open_time = TimeField("Opening Time", validators=[DataRequired()])
    close_time = TimeField("Closing Time", validators=[DataRequired()])
    coffee_rating = SelectField(
        "Coffee Rating",
        validators=[DataRequired()],
        choices=["☕️", "☕️☕️", "☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️☕️☕️"],
    )
    wifi = SelectField(
        "Wifi Strength Rating",
        validators=[DataRequired()],
        choices=[
            "✘",
            "💪",
            "💪💪",
            "💪💪💪",
            "💪💪💪💪",
            "💪💪💪💪💪",
        ],
    )
    power_outlet = SelectField(
        "Power Outlets Avaibility",
        validators=[DataRequired()],
        choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
    )
    submit = SubmitField("Submit")


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        cafe_name = form.cafe.data
        location = form.location.data
        open_time = form.open_time.data
        close_time = form.close_time.data
        coffee_rating = form.coffee_rating.data
        wifi_rating = form.wifi.data
        power_rating = form.power_outlet.data
        with open(CAFE_CSV_PATH, "a", encoding="utf-8" )as csv_file:
            csv_data = f"\n{cafe_name},{location},{open_time},{close_time},{coffee_rating},{wifi_rating},{power_rating}"
            print(csv_data)
            csv_file.write(csv_data)
        

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template("add.html", form=form)


@app.route("/cafes")
def cafes():
    with open(CAFE_CSV_PATH, newline="", encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template("cafes.html", cafes=list_of_rows)


if __name__ == "__main__":
    app.run(debug=True)

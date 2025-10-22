from flask import Flask, jsonify, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import requests, pathlib, random


"""
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
"""

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
CUR_DIR = pathlib.Path(__file__).parent
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(
    CUR_DIR / "instance/cafes.db"
)
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:  # type: ignore
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # return {
        #     column.name: getattr(self, column.name) for column in self.__table__.columns
        # }


with app.app_context():
    db.create_all()

API_SECRET_KEY : str = "123456abcd"

@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - random route
@app.route("/random", methods=["GET"])
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    data = jsonify(
        cafe={
            "id": random_cafe.id,
            "name": random_cafe.name,
            "map_url": random_cafe.img_url,
            "location": random_cafe.location,
            "amenities": {
                "seats": random_cafe.seats,
                "has_toilet": random_cafe.has_toilet,
                "has_wifi": random_cafe.has_wifi,
                "has_sockets": random_cafe.has_sockets,
                "can_take_calls": random_cafe.can_take_calls,
                "coffee_price": random_cafe.coffee_price,
            },
        }
    )
    return jsonify(random_cafe.to_dict())


# HTTP GET - Read Record

@app.route("/all")
def get_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    cafes = [cafe.to_dict() for cafe in all_cafes]

    return jsonify(cafes)


@app.route("/search")
def get_cafeby_location():
    query_location = request.args.get("location")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    cafes = [cafe.to_dict() for cafe in all_cafes]
    if all_cafes:
        return jsonify(cafes)
    else:
        return (
            jsonify(
                error={"Not Found": "Sorry, we don't have a cafe at that location."}
            ),
            404,
        )


# HTTP POST - Create Record


@app.route("/add", methods=["POST"])
def add_cafe():
    if request.method == "POST":
        cafe_name = request.args.get("cafe_name")
        cafe_location_url = request.args.get("loc_url")
        new_cafe = Cafe(
            id=request.args.get("id"),  # type: ignore
            name=request.args.get("name"),  # type: ignore
            map_url=request.args.get("map-url"),  # type: ignore
            img_url=request.args.get("img-url"),  # type: ignore
            location=request.args.get("location"),  # type: ignore
            seats=request.args.get("seats"),  # type: ignore
            has_toilet=bool(request.args.get("toilet")),  # type: ignore
            has_wifi=bool(request.args.get("wifi")),  # type: ignore
            has_sockets=bool(request.args.get("sockets")),  # type: ignore
            can_take_calls=bool(request.args.get("call")),  # type: ignore
            coffee_price=request.args.get("price"),  # type: ignore
        )
        print(new_cafe.id)
        print(cafe_name, cafe_location_url)
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(
            response={
                "success": "Successfully Added New Cafe!!",
                "Post_data": f"{cafe_name} ,{cafe_location_url}",
            }
        )
    return "0"


# HTTP PUT/PATCH - Update Record
@app.route("/update/<int:cafe_id>", methods=["PATCH"])
def update_cafe(cafe_id):
    # cafe_id = request.args.get("cafe_id")
    cafe = db.session.get(entity=Cafe, ident=cafe_id)
    new_price = request.args.get("price")
    if cafe:
        cafe.coffee_price = new_price # type: ignore
        db.session.commit()
        return jsonify(
            response={
                "success": "Successfully Updated The cafe.",
                "updated_data": f"{new_price}",
            }
        ), 200
    else:
        return jsonify(
            error = {
                "Not Found" : "Sorry a cafe with that id is not found in database",
            }
        ), 404


# HTTP DELETE - Delete Record


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key != API_SECRET_KEY:
        return jsonify(
            error = {
                "Forbidden Access" : "Wrong API Key is provided."
            }
        ),403
    cafe = db.session.get(entity=Cafe, ident=cafe_id)
    # cafe = db.get(Cafe, id=cafe_id)
    if cafe == None:
        return jsonify(
                error = {
                    "Not Found" : "The Cafe is not available."
                }
            ),404
    else:
        db.session.delete(cafe)
        db.session.commit()
        return (
            jsonify(
                response={
                    "success": "Sadly the Cafe has been Deleted.",
                    "id": cafe.id,
                    "name": cafe.name,
                }
            ),
            200,
        )


if __name__ == "__main__":
    app.run(debug=True)

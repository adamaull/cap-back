from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ijjmreeoplaxkn:37f73081c5f80ad37c23d7e6d2f653b9366a479977b9d4d9803b095cb583c4ad@ec2-3-219-19-205.compute-1.amazonaws.com:5432/dbi4i54l0t2db1"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS = CORS(app)

class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imgUrl = db.Column(db.String, nullable=False)
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    blogpost = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, imgUrl, make, model, blogpost, price):
        self.imgUrl = imgUrl
        self.make = make
        self.model = model
        self.blogpost = blogpost
        self.price = price

class CarSchema(ma.Schema):
    class Meta:
        fields = ("id", "imgUrl", "make", "model", "blogpost", "price")
    
car_schema = CarSchema()
multiple_car_schema = CarSchema(many=True)

@app.route("/car/add", methods=["POST"])
def post_car():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    post_data = request.get_json()
    imgUrl = post_data.get("imgUrl")
    make = post_data.get("make")
    model = post_data.get("model")
    blogpost = post_data.get("blogpost")
    price = post_data.get("price")


    new_record = Cars(imgUrl, make, model, blogpost, price)
    db.session.add(new_record)
    db.session.commit()

    return jsonify("The whip was added.")

@app.route('/car/get', methods=['GET'])
def get_cars():
    cars = db.session.query(Cars).all()
    return jsonify(multiple_car_schema.dump(cars))

if __name__ == "__main__":
    app.run(debug=True)
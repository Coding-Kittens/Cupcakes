"""Flask app for Cupcakes"""


from flask import Flask, jsonify, request, render_template
from models import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()


@app.route("/")
def home_page():
    """shows the home page"""
    return render_template("home.html")


@app.route("/api/cupcakes", methods=["GET"])
def get_all_cakes():
    """returns jason of all Cupcakes"""
    serialized = [cake.serialize() for cake in Cupcake.query.all()]
    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["GET"])
def get_cake(cupcake_id):
    """returns jason of one Cupcake"""
    cake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cake.serialize())


@app.route("/api/cupcakes", methods=["POST"])
def make_cake():
    """returns jason of new Cupcake"""
    new_cake = Cupcake(
        flavor=request.json["flavor"],
        size=request.json["size"],
        rating=request.json["rating"],
    )
    if request.json["image"]:
        new_cake.image = request.json["image"]
    db.session.add(new_cake)
    db.session.commit()

    return (jsonify(cupcake=new_cake.serialize()), 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cake(cupcake_id):
    cake = Cupcake.query.get_or_404(cupcake_id)
    db.session.query(Cupcake).filter_by(id=cupcake_id).update(request.json)
    db.session.commit()
    return jsonify(cupcake=cake.serialize())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cake(cupcake_id):
    """deletes a cupcake"""
    Cupcake.query.filter_by(id=cupcake_id).delete()
    db.session.commit()
    return jsonify(message="Deleted")

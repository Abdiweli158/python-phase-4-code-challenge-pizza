#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate

from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
@@ -13,6 +14,7 @@
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)
@@ -24,6 +26,184 @@
def index():
    return "<h1>Code challenge</h1>"

class Restaurants(Resource):

    def get(self):
        restaurants = [restaurant.to_dict(rules=("-restaurant_pizzas",)) for restaurant in Restaurant.query.all()]
        return make_response(jsonify(restaurants), 200)

api.add_resource(Restaurants, '/restaurants')

# @app.route('/restaurants')
# def restaurants():
#     restaurants = [restaurant.to_dict(rules=("-restaurant_pizzas",)) for restaurant in Restaurant.query.all()]
#     response = make_response(
#         restaurants,
#         200
#     )
#     return response


class RestaurantByID(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id==id).first()

        if restaurant == None:
            response = make_response(
                {"error": "Restaurant not found"},
                404
            )
            return response

        else:
            return make_response(
                restaurant.to_dict(),
                200,
            )

    def delete(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()

        if restaurant == None:
            return make_response(
                {"error": "Restaurant not found"},
                404
            )

        else:
            db.session.delete(restaurant)
            db.session.commit()
            return make_response(
                "",
                204,
            )

api.add_resource(RestaurantByID, '/restaurants/<int:id>')        


# @app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
# def restaurant(id):
#     restaurant = Restaurant.query.filter(Restaurant.id==id).first()

#     if restaurant == None:
#         response = make_response(
#             {"error": "Restaurant not found"},
#             404
#         )
#         return response

#     else:
#         if request.method == 'GET':
#             return make_response(
#                 restaurant.to_dict(),
#                 200
#             )

#         elif request.method == 'DELETE':
#             db.session.delete(restaurant)
#             db.session.commit()
#             return make_response(
#                 "",
#                 204,
#             )


class Pizzas(Resource):
    def get(self):
        pizzas = [pizza.to_dict(rules=("-restaurant_pizzas",)) for pizza in Pizza.query.all()]
        return make_response(pizzas, 200)

api.add_resource(Pizzas, '/pizzas')

# @app.route('/pizzas')
# def pizzas():
#     pizzas = [pizza.to_dict(rules=("-restaurant_pizzas",)) for pizza in Pizza.query.all()]

#     return make_response(
#         pizzas,
#         200,
#     )


class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()

        price = data.get("price")
        pizza_id = data.get("pizza_id")
        restaurant_id = data.get("restaurant_id")

        if not all([price, pizza_id, restaurant_id]):
            return make_response(
                {"errors": ["validation errors"]},
                400,
            )

        if price < 1 or price > 30:
            return make_response(
                {"errors": ["validation errors"]},
                400,
            )

        pizza = Pizza.query.filter(Pizza.id == pizza_id).first()
        restaurant = Restaurant.query.filter(Restaurant.id == restaurant_id).first()

        if pizza is None or restaurant is None:
            return make_response(
                {"errors": ["validation errors"]},
                400,
            )

        restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
        db.session.add(restaurant_pizza)
        db.session.commit()

        return make_response(
            restaurant_pizza.to_dict(),
            201,
        )
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')


# @app.route('/restaurant_pizzas', methods=['POST'])
# def restaurant_pizzas():
#     data = request.get_json()

#     price = data.get("price")
#     pizza_id = data.get("pizza_id")
#     restaurant_id = data.get("restaurant_id")

#     if not all([price, pizza_id, restaurant_id]):
#         return make_response(
#             {"errors": ["Missing required fields"]},
#             400,
#         )

#     if price < 1 or price > 30:
#         return make_response(
#             {"errors": ["validation errors"]},
#             400,
#         )

#     pizza = Pizza.query.filter(Pizza.id == pizza_id).first()
#     restaurant = Restaurant.query.filter(Restaurant.id == restaurant_id).first()

#     if pizza is None or restaurant is None:
#         return make_response(
#             {"errors": ["validation errors"]},
#             400,
#         )

#     restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
#     db.session.add(restaurant_pizza)
#     db.session.commit()

#     return make_response(
#         restaurant_pizza.to_dict(),
#         201,
#     )


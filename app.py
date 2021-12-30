from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize app:
app = Flask(__name__)

### set up SQL Alchemy Database Uniform Resource Identifier (URI):
# Base Directory
basedir = os.path.abspath(os.path.dirname(__file__))
# Database:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #no more warnings in console :)
# Initialize DB:
db = SQLAlchemy(app)
# Initialize Marshmallow:
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    # Constructor:
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

# Product Schema:
class ProductSchema(ma.Schema):
    class Meta: # fields we are allowed to show
        fields = ('id', 'name', 'description', 'price', 'quantity')

# Initialize Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True) #in the context of working with one product vs. working with many products

### Create endpoints:
# Create a Product:
@app.route('/product', methods=['POST']) # restrict to POST
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    new_product = Product(name, description, price, quantity)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Fetch all Products
@app.route('/product', methods=['GET']) # restrict to GET
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products, many=True)
    return jsonify(result)

# Get Single Products
@app.route('/product/<id>', methods=['GET']) # know specific product to fetch
def get_product(id):
     product = Product.query.get(id)
     return product_schema.jsonify(product)

# Update a Product:
@app.route('/product/<id>', methods=['PUT']) # know specific product to update
def update_product(id):
    #need to first fetch product:
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    # create new product to submit to database:
    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity

    db.session.commit()

    return product_schema.jsonify(product)

### last function/endpoint to make this a full-on CRUD API
# Delete Product
@app.route('/product/<id>', methods=['DELETE']) # know specific product to delete
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)

# Run server:
if __name__ == '__main__': # check if main
    app.run(debug=True)

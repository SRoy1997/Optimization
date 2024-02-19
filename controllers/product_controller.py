from flask import jsonify

from db import db
from models.product import Products, product_schema, products_schema
from models.category import Categories
from util.reflection import populate_object


def add_product(req):
    post_data = req.form if req.form else req.json

    new_product = Products.new_product_obj()
    populate_object(new_product, post_data)

    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'product created', 'result': product_schema.dump(new_product)}), 201


def get_products():
    product_query = db.session.query(Products).all()

    return jsonify({'message': 'products found', 'result': products_schema.dump(product_query)}), 200


def get_all_active_products():
    product_query = db.session.query(Products).filter(Products.active == True).all()

    return jsonify({'message': 'product found', 'result': products_schema.dump(product_query)}), 200


def get_products_by_company_id(company_id):
    product_query = db.session.query(Products).filter(Products.company_id == company_id).all()

    return jsonify({'message': 'product found', 'result': products_schema.dump(product_query)}), 200


def get_product_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    return jsonify({'message': 'product found', 'result': product_schema.dump(product_query)}), 200


def update_product_by_id(req, product_id):
    post_data = req.form if req.form else req.json
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if product_query:
        populate_object(product_query, post_data)

        db.session.commit()

        return jsonify({'message': 'product updated', 'result': product_schema.dump(product_query)}), 200

    return jsonify({'message': 'product could not be updated'}), 400


def product_add_category(req):
    post_data = req.form if req.form else req.json
    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    product_query.categories.append(category_query)
    db.session.commit()

    return jsonify({'message': 'category added.', 'product': product_schema.dump(product_query)}), 200


def delete_product_by_id(product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not query:
        return jsonify({"message": "product  does not exist"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "cannot delete record"}), 400

    return jsonify({"message": "product deleted"}), 200

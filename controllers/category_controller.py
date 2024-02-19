from flask import jsonify

from db import db
from models.category import Categories, category_schema, categories_schema
from util.reflection import populate_object


def add_category(req):
    post_data = req.form if req.form else req.json

    new_category = Categories.new_category_obj()
    populate_object(new_category, post_data)

    db.session.add(new_category)
    db.session.commit()

    return jsonify({'message': 'category created', 'result': category_schema.dump(new_category)}), 201


def get_categories():
    category_query = db.session.query(Categories).all()

    return jsonify({'message': 'categories found', 'result': categories_schema.dump(category_query)}), 200


def get_category_by_id(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    return jsonify({'message': 'category found', 'result': category_schema.dump(category_query)}), 200


def update_category_by_id(req, category_id):
    post_data = req.form if req.form else req.json
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if category_query:
        populate_object(category_query, post_data)

        db.session.commit()
        return jsonify({'message': 'category updated', "result": category_schema.dump(category_query)}), 200

    return jsonify({'message': 'category not updated'}), 400


def delete_category_by_id(category_id):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not query:
        return jsonify({"message": "category does not exist"}), 400

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "cannot delete record"}), 400

    return jsonify({"message": "category deleted"}), 200

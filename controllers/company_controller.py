from flask import jsonify

from db import db
from models.company import Companies, company_schema, companies_schema
from util.reflection import populate_object


def add_company(req):
    post_data = req.form if req.form else req.json

    new_company = Companies.new_company_obj()
    populate_object(new_company, post_data)

    db.session.add(new_company)
    db.session.commit()

    return jsonify({'message': 'company created', 'result': company_schema.dump(new_company)}), 200


def get_companies():
    company_query = db.session.query(Companies).all()

    return jsonify({'message': 'companies found', 'result': companies_schema.dump(company_query)}), 200


def get_company_by_id(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    return jsonify({'message': 'company found', 'result': company_schema.dump(company_query)}), 200


def update_company_by_id(req, company_id):
    post_data = req.form if req.form else req.json
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if company_query:
        populate_object(company_query, post_data)

        db.session.commit()

        return jsonify({'message': 'company updated', "result": company_schema.dump(company_query)}), 200

    return jsonify({'message': 'company not updated'}), 400


def delete_company_by_id(company_id):
    query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not query:
        return jsonify({"message": "company does not exist"}), 400

    try:
        db.session.delete(query)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "can not delete record"}), 400

    return jsonify({"message": "company deleted"}), 200

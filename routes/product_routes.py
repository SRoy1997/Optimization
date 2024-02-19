from flask import Blueprint, request

import controllers

products = Blueprint('products', __name__)


@products.route('/product', methods=['POST'])
def add_product():
    return controllers.add_product(request)


@products.route('/products', methods=['GET'])
def get_products():
    return controllers.get_products()


@products.route('/products/active', methods=['GET'])
def get_all_active_products():
    return controllers.get_all_active_products()


@products.route('/product/company/<company_id>', methods=['GET'])
def get_products_by_company_id(company_id):
    return controllers.get_products_by_company_id(company_id)


@products.route('/product/<product_id>', methods=["GET"])
def get_product_by_id(product_id):
    return controllers.get_product_by_id(product_id)


@products.route('/product/<product_id>', methods=['PUT'])
def update_product_by_id(product_id):
    return controllers.update_product_by_id(request, product_id)


@products.route('/product/category', methods=['POST'])
def product_add_category():
    return controllers.product_add_category(request)


@products.route('/product/delete/<product_id>', methods=['DELETE'])
def delete_product_by_id(product_id):
    return controllers.delete_product_by_id(product_id)

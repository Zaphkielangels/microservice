import json
import pymysql
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'koceng123'
jwt = JWTManager(app)

class Products:
    def __init__(self, sku, product_name, stocks):
        self.Sku = sku
        self.Product_name = product_name
        self.Stocks = stocks

def get_products():
    arr_products = []

    try:
        db = pymysql.connect(host="127.0.0.1", user="root", password="", database="server2")
        cursor = db.cursor()
        
        sql = "SELECT sku, product_name, stocks FROM products ORDER BY sku DESC"
        cursor.execute(sql)
        
        rows = cursor.fetchall()
        
        for row in rows:
            sku, product_name, stocks = row
            products = Products(sku, product_name, stocks)
            arr_products.append(products)

        db.close()
    
    except Exception as e:
        print("Error:", e)

    return arr_products

@app.route('/getProduct', methods=['GET'])
@jwt_required()
def get_product():
    products_list = get_products()
    products_dict_list = [product.__dict__ for product in products_list]
    return jsonify(products_dict_list)

@app.route('/login', methods=['POST'])
def login():
    access_token = create_access_token(identity='user')
    return jsonify(access_token=access_token)

if __name__ == '__main__':
    app.run(port=7654)

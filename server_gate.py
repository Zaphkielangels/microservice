import json
import requests
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'koceng123'
jwt = JWTManager(app)

def get_ongkir_data(access_token):
    url = "http://localhost:6756/getOngkir"
    
    headers = {'Authorization': f'Bearer {access_token}'}  # Menambahkan header Authorization dengan token akses
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for 4XX or 5XX errors
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching data from API: {e}"
        print(error_message)
        return None

def get_products_data(access_token):
    url = "http://localhost:7654/getProduct"
    
    headers = {'Authorization': f'Bearer {access_token}'}  # Menambahkan header Authorization dengan token akses
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for 4XX or 5XX errors
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching data from API: {e}"
        print(error_message)
        return None

@app.route('/getDataServer1', methods=['GET'])
@jwt_required()
def get_data_server1():
    current_user = get_jwt_identity()
    print(f"Authenticated user: {current_user}")
    
    access_token = create_access_token(identity=current_user)  # Menggunakan identitas user untuk membuat token akses
    ongkir_data = get_ongkir_data(access_token)
    
    if ongkir_data:
        return jsonify(ongkir_data), 200
    else:
        return jsonify(message="Failed to fetch Ongkir data"), 500

@app.route('/getDataServer2', methods=['GET'])
@jwt_required()
def get_data_server2():
    current_user = get_jwt_identity()
    print(f"Authenticated user: {current_user}")
    
    access_token = create_access_token(identity=current_user)  # Menggunakan identitas user untuk membuat token akses
    products_data = get_products_data(access_token)
    
    if products_data:
        return jsonify(products_data), 200
    else:
        return jsonify(message="Failed to fetch Product data"), 500

@app.route('/login', methods=['POST'])
def login():
    access_token = create_access_token(identity='user')
    return jsonify(access_token=access_token)

if __name__ == '__main__':
    app.run(port=5674)

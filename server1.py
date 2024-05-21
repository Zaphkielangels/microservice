import requests
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'koceng123'
jwt = JWTManager(app)

RAJAONGKIR_API_KEY = '5675c09373472e9ed9383d3f04e6f86b'

class Ongkir:
    def __init__(self, province_id, province, city_id, city_name):
        self.province_id = province_id
        self.province = province
        self.city_id = city_id
        self.city_name = city_name

def get_ongkir_data():
    url = "https://api.rajaongkir.com/starter/city"

    headers = {
        'key': RAJAONGKIR_API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for 4XX or 5XX errors
        data = response.json()

        if 'rajaongkir' in data and 'results' in data['rajaongkir']:
            results = data['rajaongkir']['results']
            if len(results) > 0:
                # Ambil data kota pertama dari hasil
                city_data = results[0]
                ongkir = Ongkir(city_data['province_id'], city_data['province'], city_data['city_id'], city_data['city_name'])
                return ongkir.__dict__  # Mengembalikan dictionary representasi objek
            else:
                print("No city data found")
                return None
        else:
            error_message = f"Invalid or incomplete response from RajaOngkir API: {data}"
            print(error_message)
            return None

    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching data from RajaOngkir API: {e}"
        print(error_message)
        return None

@app.route('/getOngkir', methods=['GET'])
@jwt_required()
def get_ongkir():
    ongkir_data = get_ongkir_data()

    if ongkir_data:
        return jsonify(ongkir_data)
    else:
        return jsonify(message="Failed to fetch Ongkir data"), 500

@app.route('/login', methods=['POST'])
def login():
    access_token = create_access_token(identity='user')
    return jsonify(access_token=access_token)

if __name__ == '__main__':
    app.run(port=6756)

from flask import Flask, jsonify, request, abort
import controller
from db import create_tables, generate_api_key,get_db
app = Flask(__name__)

# Decorador para verificar company_api_key
def require_company_api_key(f):
    def decorated_function(*args, **kwargs):
        company_api_key = request.args.get('company_api_key') or request.headers.get('company_api_key')
        print("Received company_api_key:", company_api_key)  # Debugging
        if not company_api_key or not controller.verify_company_api_key(company_api_key):
            abort(401, description="Invalid or missing company_api_key")
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Decorador para verificar sensor_api_key
def require_sensor_api_key(f):
    def decorated_function(*args, **kwargs):
        sensor_api_key = request.args.get('sensor_api_key') or request.headers.get('sensor_api_key')
        if not sensor_api_key or not controller.verify_sensor_api_key(sensor_api_key):
            abort(401, description="Invalid or missing sensor_api_key")
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@app.route('/admin', methods=['POST'])
def create_admin():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", (username, password))
    db.commit()
    
    return jsonify({"message": "Admin created successfully"}), 201


#Endpoint de company
@app.route('/company', methods=['POST'])
def create_company():
    data = request.json
    company_name = data.get('company_name')
    company_api_key = generate_api_key()  # Genera una API key para la compañía
    success = controller.create_company(company_name, company_api_key)
    if success:
        return jsonify({
            "company_name": company_name,
            "company_api_key": company_api_key
        }), 201
    return jsonify({'error': 'Failed to create company'}), 400

@app.route('/company', methods=['GET'])
@require_company_api_key
def get_all_companies():
    companies = controller.get_companies()
    return jsonify(companies)

# Obtener una compañía por su ID
@app.route('/company/<id>', methods=['GET'])
@require_company_api_key
def get_company(id):
    company = controller.get_company_by_id(id)
    if company:
        return jsonify(company)
    return jsonify({'error': 'Company not found'}), 404

@app.route('/company/<id>', methods=['DELETE'])
@require_company_api_key
def delete_company(id):
    success = controller.delete_company(id)
    if success:
        return jsonify({'message': 'Company deleted successfully'})
    return jsonify({'error': 'Failed to delete company'}), 400

# Endpoints para el modelo Location

@app.route('/location', methods=['POST'])
@require_company_api_key
def create_location():
    data = request.json
    company_id = data.get('company_id')
    location_name = data.get('location_name')
    location_country = data.get('location_country')
    location_city = data.get('location_city')
    location_meta = data.get('location_meta', '')
    success = controller.insert_location(company_id, location_name, location_country, location_city, location_meta)
    if success:
        return jsonify({
            "location_name": location_name,
            "location_country": location_country,
            "location_city": location_city,
            "location_meta": location_meta
        }), 201
    return jsonify({'error': 'Failed to create location'}), 400

@app.route('/location', methods=['GET'])
@require_company_api_key
def get_all_locations():
    locations = controller.get_locations()
    return jsonify(locations)

@app.route('/location/<id>', methods=['GET'])
@require_company_api_key
def get_location(id):
    location = controller.get_location_by_id(id)
    if location:
        return jsonify(location)
    return jsonify({'error': 'Location not found'}), 404

@app.route('/location/<id>', methods=['PUT'])
@require_company_api_key
def update_location_endpoint(id):
    data = request.json
    success = controller.update_location(id, data['company_id'], data['location_name'], data['location_country'], data['location_city'], data.get('location_meta'))
    if success:
        return jsonify({'message': 'Location updated successfully'})
    return jsonify({'error': 'Failed to update location'}), 400

@app.route('/location/<id>', methods=['DELETE'])
@require_company_api_key
def delete_location_endpoint(id):
    success = controller.delete_location(id)
    if success:
        return jsonify({'message': 'Location deleted successfully'})
    return jsonify({'error': 'Failed to delete location'}), 400

# Endpoints para el modelo Sensor
# DE SENSOR

@app.route('/sensor', methods=['POST'])
@require_company_api_key
def create_sensor():
    data = request.json
    location_id = data.get('location_id')
    sensor_name = data.get('sensor_name')
    sensor_category = data.get('sensor_category')
    sensor_meta = data.get('sensor_meta', '')
    result = controller.create_sensor(location_id, sensor_name, sensor_category, sensor_meta)
    if result:
        return jsonify(result), 201
    return jsonify({'error': 'Failed to create sensor'}), 400

@app.route('/sensor', methods=['GET'])
@require_company_api_key
def get_all_sensors():
    sensors = controller.get_sensors()
    return jsonify(sensors)

@app.route('/sensor/<id>', methods=['GET'])
@require_company_api_key
def get_sensor(id):
    sensor = controller.get_sensor_by_id(id)
    if sensor:
        return jsonify(sensor)
    return jsonify({'error': 'Sensor not found'}), 404

@app.route('/sensor/<id>', methods=['PUT'])
@require_company_api_key
def update_sensor_endpoint(id):
    data = request.json
    success = controller.update_sensor(id, data['location_id'], data['sensor_name'], data['sensor_category'], data.get('sensor_meta'))
    if success:
        return jsonify({'message': 'Sensor updated successfully'})
    return jsonify({'error': 'Failed to update sensor'}), 400

@app.route('/sensor/<id>', methods=['DELETE'])
@require_company_api_key
def delete_sensor_endpoint(id):
    success = controller.delete_sensor(id)
    if success:
        return jsonify({'message': 'Sensor deleted successfully'})
    return jsonify({'error': 'Failed to delete sensor'}), 400

# Endpoints para el modelo SensorData--------------------------
@app.route('/api/v1/sensor_data', methods=['GET'])
@require_company_api_key
def get_all_sensor_data():
    data = controller.get_sensor_data()
    return jsonify(data)

@app.route('/api/v1/sensor_data/<id>', methods=['GET'])
@require_company_api_key
def get_sensor_data_record(id):
    data = controller.get_sensor_data_by_id(id)
    if data:
        return jsonify(data)
    return jsonify({'error': 'Sensor data not found'}), 404

@app.route('api/v1/sensor_data/<id>', methods=['PUT'])
@require_company_api_key
def update_sensor_data_endpoint(id):
    data = request.json
    success = controller.update_sensor_data(id, data['sensor_id'], data['data'])
    if success:
        return jsonify({'message': 'Sensor data updated successfully'})
    return jsonify({'error': 'Failed to update sensor data'}), 400

@app.route('/api/v1/sensor_data/<id>', methods=['DELETE'])
@require_company_api_key
def delete_sensor_data_endpoint(id):
    success = controller.delete_sensor_data(id)
    if success:
        return jsonify({'message': 'Sensor data deleted successfully'})
    return jsonify({'error': 'Failed to delete sensor data'}), 400

# Endpoint para insertar sensor_data (usa sensor_api_key)
@app.route('/api/v1/sensor_data', methods=['POST'])
@require_sensor_api_key
def insert_sensor_data():
    data = request.json
    sensor_api_key = request.args.get('sensor_api_key')  # Obtener de la URL
    json_data = data.get('data')
    timestamp = data.get('timestamp')

    print("Received request to insert sensor data")
    print("URL sensor_api_key:", sensor_api_key)
    print("Body data:", json_data)
    print("Body timestamp:", timestamp)

    if not sensor_api_key or not controller.verify_sensor_api_key(sensor_api_key):
        abort(401, description="Invalid or missing sensor_api_key")

    result = controller.create_sensor_data(sensor_api_key, json_data, timestamp)
    if result:
        return jsonify({'message': 'Sensor data inserted successfully', 'id': result}), 201
    return jsonify({'error': 'Failed to insert sensor data'}), 400

#@app.route('/api/v1/sensor_data', methods=['GET'])
#@require_company_api_key
#def get_sensor_data():
    sensor_ids = request.args.getlist('sensor_id')
    from_timestamp = int(request.args.get('from'))
    to_timestamp = int(request.args.get('to'))
    if not sensor_ids or not from_timestamp or not to_timestamp:
        abort(400, description="Missing required parameters")
    data = controller.get_sensor_data(sensor_ids, from_timestamp, to_timestamp)
    return jsonify(data)

if __name__ == "__main__":
    create_tables()
    """
    Here you can change debug and port
    Remember that, in order to make this API functional, you must set debug in False
    """
    app.run(host='0.0.0.0', port=8000, debug=False)
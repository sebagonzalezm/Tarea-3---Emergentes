from db import get_db, generate_api_key

# Company API Key verification
def verify_company_api_key(company_api_key):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id FROM company WHERE company_api_key = ?"
    cursor.execute(statement, [company_api_key])
    return cursor.fetchone() is not None

# Sensor API Key verification
def verify_sensor_api_key(sensor_api_key):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT sensor_id FROM sensor WHERE sensor_api_key = ?"
    cursor.execute(statement, [sensor_api_key])
    return cursor.fetchone() is not None

#DE COMPANY--------------------------------------
def create_company(company_name, company_api_key):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO company (company_name, company_api_key) VALUES (?, ?)"
    cursor.execute(statement, [company_name, company_api_key])
    db.commit()
    return cursor.lastrowid
# Obtener todas las compañías
def get_companies():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, company_name, company_api_key FROM company"
    cursor.execute(query)
    return cursor.fetchall()

# Obtener una compañía por su ID
def get_company_by_id(id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, company_name, company_api_key FROM company WHERE id = ?"
    cursor.execute(statement, [id])
    return cursor.fetchone()

# Eliminar una compañía por su ID
def delete_company(id):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM company WHERE id = ?"
    cursor.execute(statement, [id])
    db.commit()
    return cursor.rowcount > 0


# DE LOCATION---------------------------

def insert_location(company_id, location_name, location_country, location_city, location_meta):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO location (company_id, location_name, location_country, location_city, location_meta) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(statement, [company_id, location_name, location_country, location_city, location_meta])
    db.commit()
    return cursor.lastrowid

def update_location(id, company_id, location_name, location_country, location_city, location_meta):
    db = get_db()
    cursor = db.cursor()
    statement = "UPDATE location SET company_id = ?, location_name = ?, location_country = ?, location_city = ?, location_meta = ? WHERE id = ?"
    cursor.execute(statement, [company_id, location_name, location_country, location_city, location_meta, id])
    db.commit()
    return True

def delete_location(id):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM location WHERE id = ?"
    cursor.execute(statement, [id])
    db.commit()
    return True

def get_location_by_id(id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, company_id, location_name, location_country, location_city, location_meta FROM location WHERE id = ?"
    cursor.execute(statement, [id])
    return cursor.fetchone()

def get_locations():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, company_id, location_name, location_country, location_city, location_meta FROM location"
    cursor.execute(query)
    return cursor.fetchall()

#DE SENSOR--------------------------------------------

def create_sensor(location_id, sensor_name, sensor_category, sensor_meta):
    db = get_db()
    cursor = db.cursor()
    sensor_api_key = generate_api_key()
    statement = "INSERT INTO sensor (location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(statement, [location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key])
    db.commit()
    return {
        "sensor_id": cursor.lastrowid,
        "sensor_api_key": sensor_api_key
    }

def update_sensor(sensor_id, location_id, sensor_name, sensor_category, sensor_meta):
    db = get_db()
    cursor = db.cursor()
    
    # Obtener el sensor_api_key actual si no se proporciona en la solicitud
    statement = "SELECT sensor_api_key FROM sensor WHERE sensor_id = ?"
    cursor.execute(statement, [sensor_id])
    result = cursor.fetchone()
    if not result:
        return False  # Sensor no encontrado

    sensor_api_key = result[0]
    
    statement = """
        UPDATE sensor
        SET location_id = ?, sensor_name = ?, sensor_category = ?, sensor_meta = ?, sensor_api_key = ?
        WHERE sensor_id = ?
    """
    cursor.execute(statement, [location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key, sensor_id])
    db.commit()
    return True

def delete_sensor(sensor_id):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM sensor WHERE sensor_id = ?"
    cursor.execute(statement, [sensor_id])
    db.commit()
    return True

def get_sensor_by_id(sensor_id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT sensor_id, location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key FROM sensor WHERE sensor_id = ?"
    cursor.execute(statement, [sensor_id])
    return cursor.fetchone()

def get_sensors():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT sensor_id, location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key FROM sensor"
    cursor.execute(query)
    return cursor.fetchall()

#DE SENSOR DATA

def create_sensor_data(sensor_api_key, data, timestamp):
    db = get_db()
    cursor = db.cursor()
    print("Received sensor_api_key:", sensor_api_key)
    print("Received data:", data)
    print("Received timestamp:", timestamp)

    statement = "SELECT sensor_id FROM sensor WHERE sensor_api_key = ?"
    cursor.execute(statement, [sensor_api_key])
    sensor = cursor.fetchone()

    if sensor is None:
        print("No sensor found with the provided sensor_api_key")
        return None

    sensor_id = sensor[0]
    print("Found sensor_id:", sensor_id)

    statement = "INSERT INTO sensor_data (sensor_id, data, timestamp) VALUES (?, ?, ?)"
    cursor.execute(statement, [sensor_id, data, timestamp])
    db.commit()

    print("Inserted sensor data with id:", cursor.lastrowid)
    return cursor.lastrowid

def update_sensor_data(id, sensor_id, data):
    db = get_db()
    cursor = db.cursor()
    statement = "UPDATE sensor_data SET sensor_id = ?, data = ? WHERE id = ?"
    cursor.execute(statement, [sensor_id, data, id])
    db.commit()
    return True

def delete_sensor_data(id):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM sensor_data WHERE id = ?"
    cursor.execute(statement, [id])
    db.commit()
    return True

def get_sensor_data_by_id(id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, sensor_id, data FROM sensor_data WHERE id = ?"
    cursor.execute(statement, [id])
    return cursor.fetchone()

def get_sensor_data(sensor_ids, from_timestamp, to_timestamp):
    db = get_db()
    cursor = db.cursor()
    placeholder = ', '.join('?' for _ in sensor_ids)
    query = f"SELECT id, sensor_id, data, timestamp FROM sensor_data WHERE sensor_id IN ({placeholder}) AND timestamp BETWEEN ? AND ?"
    cursor.execute(query, sensor_ids + [from_timestamp, to_timestamp])
    return cursor.fetchall()
import json
import os
from psycopg2 import sql
import uuid
from datetime import datetime

def clean_and_validate(data):
    # Validate and clean the 'version' field
    if 'version' not in data or data['version'] is None:
        data['version'] = 'unknown'

    # Validate and clean the 'area' field
    if 'area' not in data or data['area'] is None:
        data['area'] = 0
    else:
        data['area'] = float(data['area'])

    # Validate and clean the 'roof_type' field
    if 'roof_type' not in data or data['roof_type'] is None:
        data['roof_type'] = 'unknown'
    
    # Validate and clean the 'mounting_plane_angles' field
    if 'mounting_plane_angles' not in data or data['mounting_plane_angles'] is None:
        data['mounting_plane_angles'] = []
    else:
        data['mounting_plane_angles'] = [float(angle) for angle in data['mounting_plane_angles']]

    # Add any additional validation and cleaning steps as needed

    return data

# Add a function to get the latest version of the roof
def get_latest_version(cur, roof_uid):
    cur.execute('''
        SELECT version FROM Roof WHERE roof_uid = %s ORDER BY version DESC LIMIT 1
    ''', (roof_uid,))
    result = cur.fetchone()
    return result[0] if result else 0

def process_data(conn, data_path):
    cur = conn.cursor()

    for file_name in os.listdir(data_path):
        with open(f"{data_path}/{file_name}") as f:
            data = json.load(f)
            data = clean_and_validate(data)
            roof_uid = uuid.UUID(data['roof_uid'])
            version = get_latest_version(cur, roof_uid) + 1
            area = data['area']
            roof_type = data['roof_type']
            timestamp = datetime.utcnow()

            cur.execute(sql.SQL('''
                INSERT INTO RoofTypes (type) VALUES (%s)
                ON CONFLICT (type) DO UPDATE SET type = %s
                RETURNING id
            '''), (roof_type, roof_type))
            roof_type_id = cur.fetchone()[0]

            cur.execute('''
                INSERT INTO Roof (roof_uid, version, area, roof_type_id, timestamp)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            ''', (roof_uid, version, area, roof_type_id, timestamp))
            roof_id = cur.fetchone()[0]

            for angle in data['mounting_plane_angles']:
                cur.execute('''
                    INSERT INTO MountingPlanes (roof_id, angle) VALUES (%s, %s)
                ''', (roof_id, angle))

            conn.commit()


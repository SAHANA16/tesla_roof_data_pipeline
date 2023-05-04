import psycopg2
from psycopg2 import sql


def create_tables(conn):
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Roof (
            id SERIAL PRIMARY KEY,
            roof_uid UUID DEFAULT uuid_generate_v4(),
            version INTEGER NOT NULL,
            area FLOAT NOT NULL,
            roof_type_id INTEGER REFERENCES RoofTypes(id),
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            UNIQUE (roof_uid, version)
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS MountingPlanes (
            id SERIAL PRIMARY KEY,
            roof_id INTEGER,
            angle FLOAT,
            FOREIGN KEY (roof_id) REFERENCES Roof(id)
        );
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS RoofTypes (
            id SERIAL PRIMARY KEY,
            type VARCHAR(255)
        );
    ''')

    conn.commit()

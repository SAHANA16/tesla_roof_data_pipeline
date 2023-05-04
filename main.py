import os
import configparser
import psycopg2
from scripts.create_tables import create_tables
from scripts.process_data import process_data
from scripts.export_data import export_data


def main():
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    conn = psycopg2.connect(
        dbname=config['database']['dbname'],
        user=config['database']['user'],
        password=config['database']['password'],
        host=config['database']['host'],
        port=config['database']['port']
    )

    create_tables(conn)
    process_data(conn, 'data')
    export_data(conn, 'output')

    conn.close()


if __name__ == '__main__':
    main()

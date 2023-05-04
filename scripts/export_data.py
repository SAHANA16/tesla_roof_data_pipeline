import pandas as pd
from psycopg2 import sql


def export_data(conn, output_path):
    tables = ['Roof', 'MountingPlanes', 'RoofTypes']
    for table in tables:
        query = sql.SQL('SELECT * FROM {}').format(sql.Identifier(table))
        df = pd.read_sql_query(query, conn)
        df.to_csv(f"{output_path}/{table}.csv", index=False)

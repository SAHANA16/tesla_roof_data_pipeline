import pytest
from datetime import datetime
from psycopg2 import sql
from process_data import clean_and_validate, process_data

# Example data for testing
sample_data = {
    'version': 'v1',
    'area': '1000',
    'roof_type': 'Tile',
    'mounting_plane_angles': ['30', '45', '60'],
    'roof_uid': 'c27e23f6-4027-4d2a-8c24-30e3c994120a'
}

# Unit tests for clean_and_validate function
def test_clean_and_validate():
    cleaned_data = clean_and_validate(sample_data)

    # Test 'version' field
    assert cleaned_data['version'] == 'v1'

    # Test 'area' field
    assert isinstance(cleaned_data['area'], float)
    assert cleaned_data['area'] == 1000.0

    # Test 'roof_type' field
    assert cleaned_data['roof_type'] == 'Tile'

    # Test 'mounting_plane_angles' field
    assert isinstance(cleaned_data['mounting_plane_angles'], list)
    assert len(cleaned_data['mounting_plane_angles']) == 3
    assert all(isinstance(angle, float) for angle in cleaned_data['mounting_plane_angles'])

    # Test additional validations and cleanings if applicable

# Mock connection and cursor objects for testing
class MockCursor:
    def __init__(self):
        self.fetchall_result = []
    
    def execute(self, query, values=None):
        pass
    
    def fetchone(self):
        return self.fetchall_result.pop(0)

class MockConnection:
    def __init__(self):
        self.cursor = MockCursor()

# Unit test for process_data function
def test_process_data():
    # Mock data path
    data_path = '/path/to/data'
    
    # Mock database connection
    conn = MockConnection()

    # Mock execute and fetchone methods
    conn.cursor.fetchall_result = [1, 1]

    # Execute the process_data function
    process_data(conn, data_path)

    # Test the executed SQL statements
    expected_queries = [
        sql.SQL("INSERT INTO RoofTypes (type) VALUES (%s) ON CONFLICT (type) DO UPDATE SET type = %s RETURNING id"),
        sql.SQL("INSERT INTO Roof (roof_uid, version, area, roof_type_id, timestamp) VALUES (%s, %s, %s, %s, %s) RETURNING id"),
        sql.SQL("INSERT INTO MountingPlanes (roof_id, angle) VALUES (%s, %s)")
    ]

    executed_queries = [query[0] for query in conn.cursor.execute.call_args_list]
    assert executed_queries == expected_queries

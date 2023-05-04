CREATE TABLE Roof (
    id SERIAL PRIMARY KEY,
    version INTEGER NOT NULL,
    area FLOAT NOT NULL,
    roof_type_id INTEGER REFERENCES RoofTypes(id),
    UNIQUE (id, version)
);


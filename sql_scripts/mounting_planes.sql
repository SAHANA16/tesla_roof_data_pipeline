CREATE TABLE MountingPlanes (
    id SERIAL PRIMARY KEY,
    roof_id INTEGER REFERENCES Roof(id),
    angle FLOAT NOT NULL
);


#!/bin/bash

docker build -t tesla_roof_data_pipeline .
docker run --rm --name tesla_roof_data_pipeline \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/config:/app/config \
  tesla_roof_data_pipeline

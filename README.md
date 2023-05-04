# Tesla Roof Data Pipeline

This data pipeline processes and stores roof geometry data in a PostgreSQL database. It is designed to handle JSON files containing roof geometry data from various sources, clean and process the data, and store it in a relational database. The output can be consumed by analysts, data scientists, and the software engineering team for various purposes.

## Requirements

	Docker
	Python 3.8 or higher

## Installation

	1. Clone the repository:

	git clone https://github.com/your_github_username/tesla_roof_data_pipeline.git
	cd tesla_roof_data_pipeline

	2. Create a config folder and a config.ini file inside it:

	mkdir config
	cp config/config.example.ini config/config.ini

	3. Update the config/config.ini file with the appropriate PostgreSQL credentials.

	4. Make the run.sh script executable:

	chmod +x run.sh

## Running the Pipeline

	To execute the pipeline, run the run.sh script:

	./run.sh

	The script will build a Docker container, run the data processing pipeline, and output CSV files representing the transformed data.

## Project Structure

	tesla_roof_data_pipeline/
	│
	├── config/
	│   ├── config.example.ini
	│   └── config.ini
	│
	├── data/
	│   └── roof_data_*.json
	│
	├── output/
	│
	├── scripts/
	│   ├── create_tables.py
	│   ├── process_data.py
	│   └── export_data.py
	│
	├── sql_scripts/
	│   ├── roof_types.sql
	│   ├── roof.sql
	│   └── mounting_planes.sql
	│
	├── .gitignore
	├── Dockerfile
	├── README.md
	├── requirements.txt
	├── main.py
	└── run.sh

## Explanation of key directories and files:

	config/: Contains the configuration files, including config.example.ini (template) and config.ini (user-defined configuration).

	data/: Folder containing JSON files with roof geometry data.

	output/: Folder where the output CSV files will be stored.

	sql_scripts/: Folder containing ddl commands to create the tables

	scripts/: Folder containing Python scripts for creating tables, processing data, and exporting data.

	Dockerfile: Dockerfile for building the Docker container.

	requirements.txt: File containing the required Python packages.

	main.py: Main Python script that runs the data pipeline.

	run.sh: Bash script for building the Docker container and running the data pipeline.

## How it Works

The run.sh script builds a Docker container with Python and the required packages.
The Docker container runs the main.py script, which reads the configuration file and establishes a connection to the PostgreSQL database.
The create_tables function creates the necessary tables in the database.
The process_data function reads the JSON files, cleans and processes the data, and inserts it into the database.
The export_data function exports the data from the database into CSV files, which are stored in the output folder.

## Consumers
This data pipeline provides the following data for various consumers:

Analyst: Aggregate statistics and roof type information.
Data Scientist: Feature-engineered quantities of various roof properties.
Software Engineering Team: Precise mounting plane angles for the Solar Roof product's tiling API.

## Justification of your solution

The proposed data pipeline solution for Tesla's Residential Energy roof imagery data is designed to meet the needs of different consumers while ensuring data integrity and ease of use. The solution utilizes a modular approach, making it highly maintainable, and follows best practices such as using configuration files to avoid hardcoded values.

I chose PostgreSQL as the relational database management system because of its robustness, scalability, and support for advanced data types, making it suitable for enterprise and production-level applications. By storing data in a relational database, we can efficiently serve different consumers (analysts, data scientists, and software engineers) with varying requirements while maintaining data consistency.

The data pipeline is divided into three main steps: creating tables, processing data, and exporting data. This modular approach allows for better code organization, ease of understanding, and flexibility in case the pipeline needs to be extended or modified.

To minimize data integrity issues, data validation and cleaning are performed during the data processing step. The pipeline handles JSON data, validates and cleans it, and stores it in the PostgreSQL database with appropriate data types and structures.

We used Docker to containerize the data pipeline, ensuring consistent execution across different environments, and simplifying the deployment process. The provided bash script automates building the Docker container and running the data pipeline, further enhancing the user experience.

The output is delivered as CSV files, a widely accepted format that can be easily consumed by different stakeholders. The modular design and comprehensive documentation ensure that this solution is production-ready, easy to maintain, and can be adapted to changing requirements in the future.

## Explaining why you chose your solution matters more than what solution your chose.

The choice of the solution for Tesla's Residential Energy data pipeline was driven by several factors, including ease of use, maintainability, and adaptability to different consumers' needs.

Ease of use: The modular design of the data pipeline ensures that the code is easy to understand and follow. It is divided into separate functions for creating tables, processing data, and exporting data, making it straightforward for users to pinpoint specific areas of interest or modify them. The use of Docker to containerize the application simplifies deployment and ensures consistent execution across different environments.

Maintainability: By utilizing configuration files instead of hardcoded values, the solution becomes more maintainable and less prone to errors. Moreover, the comprehensive documentation provided in the README and inline comments within the code helps future developers quickly grasp the solution's structure and purpose.

Adaptability: The solution uses a PostgreSQL relational database to store the data, enabling it to efficiently serve different consumers with varying requirements while maintaining data consistency. The use of a relational database also ensures scalability and provides support for advanced data types, making it suitable for enterprise and production-level applications.

Data integrity: The pipeline includes data validation and cleaning during the data processing step, ensuring that the stored data is consistent and accurate. This is crucial for delivering reliable insights and analytics to the end-users.

Output format: The data pipeline exports the data as CSV files, which are widely accepted and can be easily consumed by different stakeholders, such as analysts, data scientists, and software engineers.

The solution was chosen based on these factors, aiming to provide a user-friendly, maintainable, and adaptable data pipeline that ensures data integrity and serves the diverse needs of Tesla's Residential Energy data consumers.

## Comment your code – you are also being evaluated on the clarity and replicability of your solution.

I have added the comments at the beginning of each major step to provide context and explain the purpose of the code. This helps ensure that the code is easily understandable, and future developers can follow the logic and replicate the solution as needed.

## Do not assume data is perfect. Double check and clean data if necessary.

process_data.py script includes data validation and cleaning steps for the version, area, roof_type, and mounting_plane_angles fields.

## It’s possible that the provided dataset includes versioning information; think about how you would handle modifications/updates to an original model

To handle modifications and updates to an original model, I have implemented a versioning system for your data pipeline.

Here's a possible approach for your specific scenario:

1. Added a new field to the Roof table to store a unique identifier (e.g., roof_uid) for each roof. This identifier remains the same across different versions of the same roof.

2. Updated the Roof table schema to include a timestamp field to store the time when a new version of the data is inserted.

3. When a new version of a roof is inserted, search for the latest version of the same roof (using the roof_uid). If a newer version is found, insert the new version with an incremented version number and update the timestamp field.

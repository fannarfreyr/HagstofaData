# HagstofaData

## Overview
The primary objective of this project is to create a simple ETL pipeline that will periodically fetch new consumer price index (CPI) data from the Statistics Iceland API and store the result in a database.

## Data
The data comes from the Statistics Iceland API via a POST request.

## Architecture
![hagstofadataETL](https://github.com/user-attachments/assets/ddcb2cef-593e-42a0-a60b-058d155b030e)

## How to Run the Codebase

1. Set up your environment
    - Ensure you have python installed (3.8 or higher)
    - Set up and activate virtual environment
    ```
    python -m venv venv
    ./venv/scripts/activate
    ```
    - Install necessary dependencies
    ```
    pip install -r requirements.txt
    ````
2. Set up environment variables
    - Create a .env file in the root directory of your project and add the following variables
    ```
    WORKING_DIR=/path/to/your/working/directory //where WORKING_DIR is path to the sqlite database
    DB_NAME=name_of_db // for example here it is cpi.db
    ```
3. Run the pipeline.py script
    - Execute the pipeline.py script to establish connections and perform data transformation.

## Future Work
There are a few things that could be added. I will explain some of them, and if I do decide to act on them they will be stricken over.

1. Add a Diagram showing the database schema.
2. Write tests, for functions and data.
3. Create a dashboard to visualize the consumer price index data.
4. Explore whether to use another DBMS like Postgres or Snowflake.
5. Consider whether and how to deploy to the cloud, using Databricks and Delta Live Tables (for dashboard) for example.
6. Statistics Iceland publishes a new index each month, so fetching that each month is neede. Probably use Apache Airflow for these orchestrations.
7. Containerize the code, with docker.

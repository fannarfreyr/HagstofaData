import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np 
from sqlalchemy import create_engine
import requests
import datetime as dt

# Load environment variables from a .env file.
load_dotenv()

# Set working directory
working_dir = os.getenv("WORKING_DIR")

def change_dir(file_path):
    """
        Change the current working directory to specified file path
    """
    try:
        if os.getcwd() == file_path:
            return os.getcwd()
        os.chdir(file_path)
        return os.getcwd()
    except Exception as e:
        print("Error changing the working directory!")
        return None
    

# Change the directory
curr_dir = change_dir(working_dir)

# Statistics Iceland API consumer price index API URL
api_url = "https://px.hagstofa.is:443/pxen/api/v1/en/Efnahagur/visitolur/1_vnv/1_vnv/VIS01000.px"

# Query to POST to API
query = {
  "query": [
    {
      "code": "Index",
      "selection": {
        "filter": "item",
        "values": [
          "CPI"
        ]
      }
    }
  ],
  "response": {
    "format": "json"
  }
}

# POST request
response = requests.post(api_url, json=query)

# Read the request JSON
data = response.json()

# Attributes of interest are: ['month', 'index', 'change_M', 'change_A', 'A_rate_M', 'A_rate_3M', 'A_rate_6M']
# The month attribute is of a weird format (e.g., 2022M06) so we want to change to standard YYYY-MM-DD

def transform_month(month:str) -> str:
  """
      Takes month of year in the form: YYYY"M"MM
      Returns: month of year in the form of YYYY-MM-DD with DD set as 01 by default
  """
  month_transformed = month.replace("M", "-")
  return month_transformed + "-01"

# Now to collect the data from the response object into a dataframe

# The response object has a weird format
"""
    [{'key': ['1988M05', 'CPI', 'index'], 'values': ['100.0']},
    {'key': ['1988M05', 'CPI', 'change_M'], 'values': ['.']},
    {'key': ['1988M05', 'CPI', 'change_A'], 'values': ['.']},
    {'key': ['1988M05', 'CPI', 'A_rate_M'], 'values': ['.']},
    {'key': ['1988M05', 'CPI', 'A_rate_3M'], 'values': ['.']},
    {'key': ['1988M05', 'CPI', 'A_rate_6M'], 'values': ['.']},
    {'key': ['1988M06', 'CPI', 'index'], 'values': ['103.4']},
    ...]

    Notice how the first 5 lines of the response object are all for the same month.
    Each line holds an attribute and value. Need to change that into a more manageable format.
    
    For example one where each line is one month:
        [{"month":month, "index":value, "change_M":value. ...}]
"""

def one_month_one_row(object):
    """
    Takes in a object where each month has five entries for each attribute
    Returns: pandas dataframe where each month takes a single row
    """
    cpi_data = []
    item = data['data']
    for i in range(0, len(data['data']), 6):
        row = {'month': transform_month(item[i]['key'][0]),
            "index": item[i]['values'][0],
            "change_M": item[i+1]['values'][0],
            "change_A": item[i+2]['values'][0],
            "A_rate_M": item[i+3]['values'][0],
            "A_rate_3M": item[i+4]['values'][0],
            "A_rate_6M": item[i+5]['values'][0]}
        cpi_data.append(row)
    
    return pd.DataFrame(cpi_data)

cpi_df = one_month_one_row(data)

# The month attribute should be of type datetime
cpi_df['month'] = pd.to_datetime(cpi_df['month'])

# Missing values are represented with ".", we clean that and change it to pd.NAN
cpi_df = cpi_df.replace(".", np.nan)

def attributes_to_float(df, dtype):
    """
    Takes in a dataframe and a dictionary where the key is a attribute name and the values specifies the type of the column
    Returns: a dataframe with updated column/attribute types
    """
    for k,v in dtype.items():
        df[k] = df[k].astype(v)
    return df

# The rest of the attributes should be of type float
dtype={"index": float,
       "change_M": float,
       "change_A": float,
       "A_rate_M": float,
       "A_rate_3M": float,
       "A_rate_6M": float}

cpi_df_correct_types = attributes_to_float(cpi_df, dtype=dtype)

# Now we are ready to load the dataframe to a database

def create_db_connection(db_name):
    """
    Creates a database connection object.
    """
    return create_engine("sqlite:///{}".format(db_name))

# First we load the sqlite database name from environment
db_name = os.getenv("DB_NAME")

# Create the database engine
engine = create_db_connection(db_name)

# Use pandas to write to the database

def write_to_sql(dataframe, table_name, connection):
    """
    Takes in a dataframe, name of database table and the database engine/connection object. 
    Writes the dataframe to the specified table in the connected database.
    """
    dataframe.to_sql(name=table_name,con=connection, if_exists='replace')

write_to_sql(cpi_df_correct_types, table_name="cpi", connection=engine)

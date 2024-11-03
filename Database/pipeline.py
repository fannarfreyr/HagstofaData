import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np 
from sqlalchemy import create_engine
import logging
import requests

# Load environment variables from a .env file.
load_dotenv()

# Set working directory
working_dir = os.getenv("WORKING_DIR")

def change_dir(file_path):
    """
        Change the current working directory to specified file path
    """
    try:
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
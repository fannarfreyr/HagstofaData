from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

table_name = os.getenv("DB_NAME")

engine = create_engine("sqlite:///{}".format(table_name))

df = pd.read_sql("SELECT * FROM cpi;", engine)
print(df.head(30))
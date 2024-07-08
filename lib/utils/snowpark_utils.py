__author__ = "John Bellamy"
__copyright__ = "Copyright 2024 John Bellamy"

from snowflake.snowpark import Session, DataFrame
import os
from dotenv import load_dotenv
import os

file_path = os.path.realpath(__file__)
env_path = os.path.dirname(file_path)

load_dotenv(f"{env_path}/.env")

CONN_CONFIG = {
    "user": os.getenv("USER_NAME"),
    "password": os.getenv("PASSWORD"),
    "account": os.getenv("ACCOUNT"),
    "warehouse": "COMPUTE_WH",
    "schema": "PUBLIC",
    "database": 'WINE',
    "role": "ACCOUNTADMIN"
}

def make_session():
    """
    Create a Snowflake session object
    :return:
    """
    conn = Session.builder.configs(CONN_CONFIG).create()
    return conn


def get_snowpark_df() -> DataFrame:
    """
    :return:
    """
    conn = make_session()
    df_tbl_read = conn.table("WINE_QUALITY")
    return df_tbl_read

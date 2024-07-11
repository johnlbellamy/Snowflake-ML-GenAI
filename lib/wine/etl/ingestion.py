__author__ = "John Bellamy"
__copyright__ = "Copyright 2024 John Bellamy"

from snowflake.connector import connect
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv("../utils/.env")


def get_conn() -> connect:
    """
    Gets connection handle for Snowflake
    :return: conn-- connect handle for Snowflake
    """
    conn = connect(
        user=os.getenv("USER_NAME"),
        password=os.getenv("PASSWORD"),
        account=os.getenv("ACCOUNT"),
        warehouse="COMPUTE_WH",
        schema="PUBLIC",
        database='WINE')

    return conn


def combine_csv() -> None:
    """
    Combines red and white samples and sets type for each
    """
    rdf = pd.read_csv("../../data/winequality-red.csv",
                      sep=";")
    wdf = pd.read_csv("../../data/winequality-white.csv",
                      sep=";")
    rdf["type"] = ["r"] * len(rdf)
    wdf["type"] = ["w"] * len(wdf)

    cdf = pd.concat([rdf, wdf])

    try:
        assert (len(wdf) + len(rdf)) == (len(cdf))
    except AssertionError:
        print("Combined dataset size is wrong.\nMerge failed.")
    cat_mapper = {3: 0, 4: 1, 5: 2, 6: 3, 7: 4, 8: 5, 9: 6}
    cdf["quality"] = cdf["quality"].map(lambda x: cat_mapper[x])
    cdf = cdf.sample(frac=1)
    cdf.to_csv("../../data/winequality.csv", index=False)


def create_and_load_table(conn: connect) -> None:
    """
    Ingests combined red and white wine datasets
    :return: None
    """
    with open("create_table.sql", "r") as file:
        table_query = file.readlines()

    table_query = "\n".join(table_query)
    conn.cursor().execute(table_query)

    with open("upload_data.sql", "r") as file:
        upload_data_query = file.readlines()

    upload_data_query = "\n".join(upload_data_query)

    conn.cursor().execute("PUT file://../..//data/winequality.csv @~/staged;")
    conn.cursor().execute(upload_data_query)


if __name__ == "__main__":
    print("Combining datasets...")
    combine_csv()
    print("getting connection object")
    conn = get_conn()

    print("Ingesting")
    print(create_and_load_table(conn))

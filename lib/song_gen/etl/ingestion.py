__author__ = "John Bellamy"
__copyright__ = "Copyright 2024 John Bellamy"

import os
from dotenv import load_dotenv
from snowflake.connector import connect
import json

BASE_DIR = "../data"
load_dotenv("../../wine/utils/.env")


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
        database='SONG')

    return conn


def parse_to_json():
    """

    :return:
    """
    folders = os.listdir(BASE_DIR)
    folders = [f for f in folders if f != "data"]
    conn = get_conn()

    with open("create_table.sql", "r") as file:
        table_query = file.readlines()

    table_query = "\n".join(table_query)
    conn.cursor().execute(table_query)
    for folder in folders:
        for file in os.listdir(f"{BASE_DIR}/{folder}"):
            with open(f"{BASE_DIR}/{folder}/{file}", "r") as f:
                lyric_text = f.readlines()
                lyric_text = "\n".join(lyric_text)
            artist = folder.upper()
            title = file.replace("_", " ").replace(".txt", "").upper()

            json_ibj = json.dumps({"ARTIST": artist, "SONG_TITLE": title, "LYRICS": lyric_text})
            with open(f"../data/json_parsed/{title}.json", "w") as f:
                f.write(json_ibj)
            print(f"Inserting artist: {artist}\nSong: {title}")


if __name__ == "__main__":
    parse_to_json()
import os
from snowflake.snowpark import Session
from agents.agents import (get_first_name_agent,
                         write_song_agent)
from document import Document
import warnings
warnings.filterwarnings("ignore")

CONN_CONFIG = {
    "user": os.getenv("USER_NAME"),
    "password": os.getenv("PASSWORD"),
    "account": os.getenv("ACCOUNT"),
    "warehouse": "COMPUTE_WH",
    "schema": "PUBLIC",
    "database": 'SONG',
    "role": "ACCOUNTADMIN",
    "openai_key": os.getenv("`OPENAI_API_KEY`"),
}

conn = Session.builder.configs(CONN_CONFIG).create()
LYRICS_TABLE = conn.table("LYRICS").to_pandas()

if __name__ == "__main__":
    name = get_first_name_agent("Compose a song in the style of Lana del Rey")
    lyrics = LYRICS_TABLE[LYRICS_TABLE["ARTIST"] == name.upper()]
    lyric_strings = []
    for lyric in lyrics["LYRICS"].to_list():
        lyric_strings.append(lyric.replace("\n", " "))

    song = write_song_agent(lyric_strings)
    print(song)





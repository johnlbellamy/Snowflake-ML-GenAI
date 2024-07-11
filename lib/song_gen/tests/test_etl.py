import os

from snowflake.snowpark import Session

from lib.song_gen.agents.agents import get_first_name_agent

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


def test_lyrics_table():
    """

    :return:
    """
    name = get_first_name_agent("Compose a song in the style of Lana del Rey")
    lyrics = LYRICS_TABLE[LYRICS_TABLE["ARTIST"] == name.upper()]

    assert len(lyrics["LYRICS"].to_list()) == 5

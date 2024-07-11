import sys
sys.path.append("agents")
from agents import (get_first_name_agent,
                    write_song_agent)


def test_get_first_name_agent():
    """
    :return:
    """
    first_name = get_first_name_agent("Write a song in the style of Taylor Swift")
    assert first_name.upper() == "TAYLOR"

def test_write_sing_gen_agent():
    """
    :return:
    """
    first_name = get_first_name_agent("Write a song in the style of Taylor Swift")
    first_name.upper()


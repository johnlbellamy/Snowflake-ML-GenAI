import pathlib
import sys
import streamlit as st
from snowflake.snowpark import Session
from streamlit_chat import message

from agents.agents import (get_first_name_agent,
                           write_song_agent)

from main import CONN_CONFIG

conn = Session.builder.configs(CONN_CONFIG).create()
LYRICS_TABLE = conn.table("LYRICS").to_pandas()


class WikiStreamlitApp:
    def __init__(self):
        self.build_app()
        self.initialize_session()
        self.clear_button = st.sidebar.button("Clear Conversation", key="clear")

    @staticmethod
    def initialize_session():
        """"""
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []
        if 'past' not in st.session_state:
            st.session_state['past'] = []
        if 'messages' not in st.session_state:
            st.session_state['messages'] = [
                {"role": "system", "content": "You are a helpful assistant."}
            ]
        if 'model_name' not in st.session_state:
            st.session_state['model_name'] = []
        if 'cost' not in st.session_state:
            st.session_state['cost'] = []
        if 'total_tokens' not in st.session_state:
            st.session_state['total_tokens'] = []
        if 'total_cost' not in st.session_state:
            st.session_state['total_cost'] = 0.0

    @staticmethod
    def build_app():
        st.set_page_config(page_title="Song Writing App", page_icon=":robot_face:")
        st.markdown("<h1 style='text-align: center;'>Song Writing App</h1>", unsafe_allow_html=True)

    @staticmethod
    def get_lyric_list(artist_name: str) -> list:
        lyrics = LYRICS_TABLE[LYRICS_TABLE["ARTIST"] == artist_name.upper()]
        lyric_strings = []
        for lyric in lyrics["LYRICS"].to_list():
            lyric_strings.append(lyric.replace("\n", " "))
        return lyric_strings

    @staticmethod
    def generate_response(prompt):
        st.session_state['messages'].append({"role": "user", "content": prompt})

        artist_name = get_first_name_agent(prompt)
        lyric_strings = WikiStreamlitApp.get_lyric_list(artist_name)

        if len(lyric_strings) == 0:  # if artist not in database, return default
            lyric_strings = WikiStreamlitApp.get_lyric_list("TAYLOR")
            song = write_song_agent(lyric_strings)
            generated_text = {"result": f"Artist name not provided or not supported\nHere's a song in the style of "
                                        f"Taylor Swift:\n{song}"}
        else:
            song = write_song_agent(lyric_strings)
            generated_text = {
                "result": song}

        st.session_state['messages'].append({"role": "assistant", "content": generated_text['result']})
        return generated_text["result"]


if __name__ == '__main__':

    ms = WikiStreamlitApp()

    # container for chat history
    response_container = st.container()
    # container for text box
    container = st.container()
    if ms.clear_button:
        st.session_state['generated'] = []
        st.session_state['past'] = []
        st.session_state['messages'] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area("You:", key='input', height=100)
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = WikiStreamlitApp.generate_response(user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))

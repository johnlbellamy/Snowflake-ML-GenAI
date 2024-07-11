from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
from langchain_openai import OpenAIEmbeddings
from langchain.agents import tool
from document import Document

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
MODEL = ChatOpenAI(model="gpt-4", temperature=0, api_key=CONN_CONFIG.get('openapi_key'))
MODEL2 = ChatOpenAI(model="gpt-4", temperature=2, api_key=CONN_CONFIG.get('openapi_key'))


@tool
def get_first_name_agent(query: str) -> str:
    """
    :param query:
    :return: first_name
    """
    prompt_template = """You are an NER bot. Given the sentence below you will return the first name of a person in 
    that sentence. Question: Write a song in the style of Billy Ray Cyrus. first_name: Billy Question: Write me a 
    song in the style of Elvis. first_name: Elvis Question: Create a song in the style of Madonna. first_name: 
    Madonna Question: Write me a song in the style of Carrie Underwood. first_name: Carrie {sentence}"""
    prompt = PromptTemplate.from_template(
        prompt_template
    )
    output_parser = StrOutputParser()

    chain = prompt | MODEL | output_parser

    first_name = chain.invoke({"sentence": query})
    return first_name.replace("first_name:", "").strip()


def write_song_agent(lyric_strings: list) -> str:
    """
    :param: lyric_strings
    :return: song
    """
    embeddings = OpenAIEmbeddings()
    documents = []
    for lyric_string in lyric_strings:
        documents.append(Document(lyric_string, {"none": None}))
    db = FAISS.from_documents(documents, embeddings)
    retriever = db.as_retriever()

    template = """You are a world-class songwriter known for writing songs in the same style as other songs. Write a 
        song in the same style as {context}"""

    prompt = PromptTemplate.from_template(template)
    model = ChatOpenAI(model="gpt-4",
                       temperature=1.2,
                       api_key=CONN_CONFIG.get('openapi_key'))

    chain = (
            retriever
            | prompt
            | model
            | StrOutputParser()
    )
    lyric_string = ""
    for string in lyric_strings:
        lyric_string = f"{lyric_string} {string}"
    song = chain.invoke(lyric_string)
    return song

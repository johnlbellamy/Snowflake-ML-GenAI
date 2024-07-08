from snowflake.ml.registry import Registry
from snowflake.snowpark import session, Session
import os

CONN_CONFIG = {
    "user": os.getenv("USER_NAME"),
    "password": os.getenv("PASSWORD"),
    "account": os.getenv("ACCOUNT"),
    "warehouse": "COMPUTE_WH",
    "schema": "PUBLIC",
    "database": 'WINE',
    "role": "ACCOUNTADMIN"
}


def load_model_from_snowflake(model_name: str):
    """

    :param model_name:
    :return:
    """
    session = Session.builder.configs(CONN_CONFIG).create()
    reg = Registry(session=session, database_name="WINE", schema_name="PUBLIC")
    model = reg.get_model(model_name)
    mv = model.version("v1")
    return mv.load(force=True)

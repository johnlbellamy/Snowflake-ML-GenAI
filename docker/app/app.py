import pandas as pd
from fastapi import FastAPI
from snowflake.snowpark import Session

from model_input import ModelInput
import pandas as pd
import os
from model import load_model_from_snowflake

app = FastAPI()
CONN_CONFIG = {
    "user": os.getenv("USER_NAME"),
    "password": os.getenv("PASSWORD"),
    "account": os.getenv("ACCOUNT"),
    "warehouse": "COMPUTE_WH",
    "schema": "PUBLIC",
    "database": 'WINE',
    "role": "ACCOUNTADMIN"
}

@app.post("/predict")
async def predict(model_input: ModelInput):
    df_dict = {"fixed_acidity": model_input.fixed_acidity,
                             "volatile_acidity": model_input.volatile_acidity,
                             "citric_acid": model_input.citric_acid,
                             "residual_sugar": model_input.residual_sugar,
                             "chlorides": model_input.chlorides,
                             "free_sulfur_dioxide": model_input.free_sulfur_dioxide,
                             "total_sulfur_dioxide": model_input.total_sulfur_dioxide,
                             "density": model_input.density,
                             "ph": model_input.ph,
                             "sulphates": model_input.sulphates,
                             "alcohol": model_input.alcohol}
    values = [[x] for x in df_dict.values()]
    pandas_df = pd.DataFrame(data=values).T
    pandas_df.columns = [f"{x.upper()}_FEAT" for x in list(df_dict.keys())]

    session = Session.builder.configs(CONN_CONFIG).create()

    df = session.create_dataframe(pandas_df)
    model = load_model_from_snowflake("xgboost-wine")
    preds = model.predict(df)

    return {"result": preds.to_pandas().iloc[0]["PREDICTIONS"]}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

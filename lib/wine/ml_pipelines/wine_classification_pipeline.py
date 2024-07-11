__author__ = "John Bellamy"
__copyright__ = "Copyright 2024 John Bellamy"

from snowflake.ml.modeling.metrics.classification import accuracy_score
from snowflake.ml.modeling.preprocessing import MinMaxScaler
from snowflake.ml.modeling.pipeline import Pipeline
from snowflake.ml.registry import Registry
from snowflake.snowpark import session
from snowflake.ml.modeling.xgboost import XGBClassifier
from snowflake.snowpark.dataframe import DataFrame
import sys

sys.path.append("../utils")
from snowpark_utils import (get_snowpark_df,
                            make_session)
import warnings

warnings.filterwarnings("ignore")

NUMERICAL_COLS = ['FIXED_ACIDITY',
                  'VOLATILE_ACIDITY',
                  'CITRIC_ACID',
                  'RESIDUAL_SUGAR',
                  'CHLORIDES',
                  'FREE_SULFUR_DIOXIDE',
                  'TOTAL_SULFUR_DIOXIDE',
                  'DENSITY',
                  'PH',
                  'SULPHATES',
                  'ALCOHOL']

FEATURE_OUTPUT_COLS = ['FIXED_ACIDITY_FEAT',
                       'VOLATILE_ACIDITY_FEAT',
                       'CITRIC_ACID_FEAT',
                       'RESIDUAL_SUGAR_FEAT',
                       'CHLORIDES_FEAT',
                       'FREE_SULFUR_DIOXIDE_FEAT',
                       'TOTAL_SULFUR_DIOXIDE_FEAT',
                       'DENSITY_FEAT',
                       'PH_FEAT',
                       'SULPHATES_FEAT',
                       'ALCOHOL_FEAT']
TARGET = "QUALITY"
OUTPUT_COLS = ["PREDICTIONS"]

session = make_session()


def get_pipeline() -> DataFrame:
    """
    Builds a transformation pipeline to perform min-max scaling and feature engineering.
    :return: Dataframe of transformed data
    """
    pipeline = Pipeline(
        steps=[
            (
                "MMS",
                MinMaxScaler(
                    input_cols=NUMERICAL_COLS,
                    output_cols=FEATURE_OUTPUT_COLS,
                )
            )
        ]
    )
    features_df = get_snowpark_df()
    pipeline.fit(features_df)
    df_out = pipeline.transform(features_df)
    return df_out


def train(train_df: DataFrame, test_df: DataFrame) -> None:
    """
    Trains an Xgboost model on a train dataframe
    :param train_df: The training dataframe
    :param test_df: The testing dataframe
    :return:
    """
    xgboost_model = XGBClassifier(
        input_cols=FEATURE_OUTPUT_COLS,
        label_cols=TARGET,
        output_cols=OUTPUT_COLS
    )
    xgboost_model.fit(train_df)

    # Use the model to make predictions.
    predictions = xgboost_model.predict(test_df)
    predictions[OUTPUT_COLS].show()
    predict_on_training_data = xgboost_model.predict(train_data)
    score = accuracy_score(df=predict_on_training_data, y_true_col_names=["QUALITY"], y_pred_col_names=["PREDICTIONS"])
    print(f"Accuracy score: {score}")
    return xgboost_model, score


def log_model_to_snowflake(model: XGBClassifier,
                           score: str,
                           name: str,
                           version: str,
                           feature_sample: DataFrame) -> None:
    """
    Loads model to SF model registry
    :param model: the model to push to registry
    :param score: the score from model evaluation
    :param name: the name of the model
    :param version: the model version
    :param feature_sample: a sample of the features
    :return:
    """
    reg = Registry(session=session, database_name="WINE", schema_name="PUBLIC")
    mv = reg.log_model(model,
                       model_name=name,
                       version_name=version,
                       conda_dependencies=["scikit-learn"],
                       comment="My awesome ML model",
                       metrics={"score": score},
                       sample_input_data=feature_sample)


if __name__ == "__main__":
    # Use the pipeline to transform a dataset.
    features_df_out = get_pipeline()
    train_data, test_data = features_df_out.random_split(weights=[0.9, 0.1], seed=0)
    model, score = train(train_data, test_data)
    #log_model_to_snowflake(model, score, "xgboost-wine", "v1", test_data)

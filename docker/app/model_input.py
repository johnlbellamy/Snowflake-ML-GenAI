__author__ = "John Bellamy"
__copyright__ = "Copyright 2024 John Bellamy"

from pydantic import BaseModel, Field


class ModelInput(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    ph: float
    sulphates: float
    alcohol: float

from pydantic import BaseModel


class ModelResponse(BaseModel):
    prediction: float
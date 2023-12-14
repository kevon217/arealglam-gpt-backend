# app/models/query_model.py
from pydantic import BaseModel


class Query(BaseModel):
    user_input: str

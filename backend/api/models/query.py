from pydantic import BaseModel
from typing import List, Dict

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    sql: str
    result: Dict[str, List]   # columns + rows
    answer: str
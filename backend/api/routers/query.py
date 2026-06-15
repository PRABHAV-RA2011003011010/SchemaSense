# from fastapi import APIRouter
# from backend.api.models.query import QueryRequest, QueryResponse
# from backend.api.services.graph.workflow import run_workflow

# router = APIRouter()

# @router.post("/", response_model=QueryResponse)
# def query_endpoint(request: QueryRequest):
#     print("Raw body received:", request.dict())
#     return run_workflow(request.query)

# from fastapi import APIRouter, Request

# router = APIRouter()

# @router.post("/")
# async def debug_query(request: Request):
#     body = await request.json()   # raw JSON payload
#     print("Raw body received:", body)
#     return {"received": body} 

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

@router.post("/", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    print("Raw body received:", request.dict())
    # For now, just echo back the query as the answer
    return {"answer": f"You said: {request.query}"}
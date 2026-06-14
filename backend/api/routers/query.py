from fastapi import APIRouter
from backend.api.models.query import QueryRequest, QueryResponse
from backend.api.services.graph.workflow import run_workflow

router = APIRouter()

@router.post("/", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    return run_workflow(request.query)
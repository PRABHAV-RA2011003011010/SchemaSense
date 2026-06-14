from fastapi import FastAPI
from pydantic import BaseModel
from backend.api.services.graph.workflow import app, WorkflowState

# Define request schema
class QueryRequest(BaseModel):
    query: str

# Define response schema
class QueryResponse(BaseModel):
    sql: str
    result: dict
    answer: str

fastapi_app = FastAPI(title="SchemaSense API")

@fastapi_app.post("/query", response_model=QueryResponse)
def run_query(request: QueryRequest):
    initial_state: WorkflowState = {
        "user_query": request.query,
        "schema": "",
        "sql_script": "",
        "result": {},
        "final_answer": ""
    }
    final_state = app.invoke(initial_state)
    return QueryResponse(
        sql=final_state["sql_script"],
        result=final_state["result"],
        answer=final_state["final_answer"]
    )

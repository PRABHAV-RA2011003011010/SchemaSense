from langgraph.graph import START, StateGraph, END
from backend.api.services.db.schema_fetcher import get_schema_snapshot
from backend.api.services.agents.generator import generate_sql
from backend.api.services.agents.evaluator import evaluate_sql
from backend.api.services.agents.executor import execute_sql
from backend.api.services.agents.summarizer import summarize_answer 
from typing import TypedDict, Dict, List, Optional
import logging
import sys

# Configure logging
for h in logging.root.handlers[:]:
    logging.root.removeHandler(h)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class WorkflowState(TypedDict):
    schema: Optional[str]
    user_query: str
    sql_script: Optional[str]
    result: Optional[Dict[str, List]]
    final_answer: Optional[str]
    error_message: Optional[str]

graph = StateGraph(WorkflowState)

def schema_node(state: WorkflowState) -> WorkflowState:
    try:
        state["schema"] = str(get_schema_snapshot())
        logger.info("Schema snapshot fetched successfully")
    except Exception as e:
        logger.error(f"Schema fetch failed: {e}")
        state["error_message"] = f"Schema fetch failed: {str(e)}"
    return state

def generator_node(state: WorkflowState) -> WorkflowState:
    if state.get("error_message"):
        return state
    try:
        sql = generate_sql(state["user_query"], state["schema"])
        state["sql_script"] = sql
        logger.info(f"SQL generated successfully: {sql}")
    except Exception as e:
        logger.error(f"SQL generation failed: {e}")
        state["error_message"] = f"SQL generation failed: {str(e)}"
    return state

def evaluator_node(state: WorkflowState) -> WorkflowState:
    if state.get("error_message"):
        return state
    try:
        sql = state.get("sql_script", "")
        if not evaluate_sql(sql):
            state["error_message"] = "Unsafe SQL detected. Only safe SELECT queries are allowed."
    except Exception as e:
        logger.error(f"SQL evaluation failed: {e}")
        state["error_message"] = f"SQL evaluation failed: {str(e)}"
    return state

def executor_node(state: WorkflowState) -> WorkflowState:
    if state.get("error_message"):
        return state
    try:
        result = execute_sql(state["sql_script"])
        state["result"] = result
        logger.info(f"SQL executed successfully, rows returned: {len(result.get('rows', []))}")
    except Exception as e:
        logger.error(f"SQL execution failed: {e}")
        state["error_message"] = f"SQL execution failed: {str(e)}"
    return state

def summarizer_node(state: WorkflowState) -> WorkflowState:
    if state.get("error_message"):
        return state
    try:
        summary = summarize_answer(state["user_query"], state["result"])
        state["final_answer"] = summary
        logger.info(f"Summarization completed: {summary}")
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        state["error_message"] = f"Summarization failed: {str(e)}"
    return state

# Define nodes
graph.add_node("schema", schema_node)
graph.add_node("generator", generator_node)
graph.add_node("evaluator", evaluator_node)
graph.add_node("executor", executor_node)
graph.add_node("summarizer", summarizer_node)

# Define edges
graph.add_edge(START, "schema")
graph.add_edge("schema", "generator")
graph.add_edge("generator", "evaluator")
graph.add_edge("evaluator", "executor")
graph.add_edge("executor", "summarizer")
graph.add_edge("summarizer", END)

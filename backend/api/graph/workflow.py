from langgraph.graph import START, StateGraph, END
from backend.api.db.schema_fetcher import get_schema_snapshot
from backend.api.agents.generator import generate_sql
from backend.api.agents.executor import execute_sql
from backend.api.agents.summarizer import summarize_answer 
from typing import TypedDict, Dict, List

class WorkflowState(TypedDict):
    schema: str
    user_query: str
    sql_script: str
    result: Dict[str, List]
    final_answer: str

# Initialize graph with state schema
graph = StateGraph(WorkflowState)

def schema_node(state: WorkflowState) -> WorkflowState:
    # Fetch schema and store as string for generator
    state["schema"] = str(get_schema_snapshot())
    return state

def generator_node(state: WorkflowState) -> WorkflowState:
    sql = generate_sql(state["user_query"], state["schema"])
    state["sql_script"] = sql
    return state

def executor_node(state: WorkflowState) -> WorkflowState:
    result = execute_sql(state["sql_script"])
    state["result"] = result
    return state

def summarizer_node(state: WorkflowState) -> WorkflowState:
    summary = summarize_answer(state["user_query"], state["result"])
    state["final_answer"] = summary
    return state

# Define nodes
graph.add_node("schema", schema_node)
graph.add_node("generator", generator_node)
graph.add_node("executor", executor_node)
graph.add_node("summarizer", summarizer_node)

# Define edges
graph.add_edge(START, "schema")
graph.add_edge("schema", "generator")
graph.add_edge("generator", "executor")
graph.add_edge("executor", "summarizer")
graph.add_edge("summarizer", END)

if __name__ == "__main__":
    initial_state: WorkflowState = {
        "user_query": "Show me all employees in IT earning more than 70k",
        "schema": "",
        "sql_script": "",
        "result": {},
        "final_answer": ""
    }

    app = graph.compile()
    final_state = app.invoke(initial_state)

    print("Generated SQL:\n", final_state["sql_script"])
    print("\nExecution Result:")
    print("Columns:", final_state["result"]["columns"])
    for row in final_state["result"]["rows"]:
        print(row)
    print("\nFinal Answer:")
    print(final_state["final_answer"])
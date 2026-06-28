from langfuse import Langfuse
from backend.core import config
from backend.api.services.graph.workflow_definition import graph, WorkflowState

# Initialize Langfuse client
langfuse = Langfuse(
    public_key=config.LANGFUSE_PUBLIC_KEY,
    secret_key=config.LANGFUSE_SECRET_KEY,
    host=config.LANGFUSE_BASE_URL,
)

def run_workflow(user_query: str):
    # Create a workflow trace
    with langfuse.start_as_current_observation(as_type="trace", name="workflow") as trace:
        trace.update(input={"query": user_query})

        initial_state: WorkflowState = {
            "user_query": user_query,
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

        # Attach output to trace
        trace.update(output=final_state.get("final_answer", ""))

    # Flush events for short-lived apps
    langfuse.flush()

    return {
        "sql": final_state["sql_script"],
        "result": final_state["result"],
        "answer": final_state["final_answer"]
    }

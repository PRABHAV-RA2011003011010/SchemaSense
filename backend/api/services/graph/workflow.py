from backend.api.services.graph.workflow_definition import graph, WorkflowState

def run_workflow(user_query: str):
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
    
    return {
        "sql": final_state["sql_script"],
        "result": final_state["result"],
        "answer": final_state["final_answer"]
    }

from langgraph import Graph
from backend.api.agents.generator import generate_sql
from backend.api.db.schema_fetcher import get_schema_snapshot
# ... other agents

graph = Graph()

# Define nodes
graph.add_node("schema", get_schema_snapshot)
graph.add_node("generator", generate_sql)
# add executor, summarizer...

# Define edges
graph.add_edge("schema", "generator")
graph.add_edge("generator", "executor")
graph.add_edge("executor", "summarizer")

if __name__ == "__main__":
    result = graph.run("Show me all IT employees earning >70k")
    print(result)
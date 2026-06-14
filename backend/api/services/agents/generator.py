from huggingface_hub import InferenceClient
import backend.core.config as config

# Initialize Hugging Face client using token from config.py
client = InferenceClient(
    provider="featherless-ai",
    api_key=config.HF_TOKEN,
)

def generate_sql(user_query: str, schema: str = ""):
    """
    Generate a SQL SELECT statement from a natural language query.
    Optionally include schema metadata for better accuracy.
    """
    prompt = f"""
    Convert the following user request into a SQL SELECT query.
    Only use SELECT statements.
    Schema: {schema}
    User request: {user_query}
    """

    result = client.text_generation(
        prompt,
        model="defog/sqlcoder-7b-2",
        max_new_tokens=200,
        temperature=0.2,  # keep outputs deterministic
    )
    return result

if __name__ == "__main__":
    schema_info = "employees(id, name, department, salary)"
    user_query = "Show me all employees in IT earning more than 70k"
    sql_script = generate_sql(user_query, schema_info)
    print("Generated SQL:\n", sql_script)

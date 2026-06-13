from huggingface_hub import InferenceClient
import config

client = InferenceClient(
    provider="featherless-ai",
    api_key=config.HF_TOKEN,
)

def summarize_answer(user_query: str, result: dict) -> str:
    """
    Answer the user query based on SQL results.
    result = {"columns": [...], "rows": [...]}
    """
    columns = result["columns"]
    rows = result["rows"]

    # Format rows into a readable string
    table_text = "\n".join([", ".join(map(str, row)) for row in rows])

    prompt = f"""
    You are a helpful assistant. The user asked:
    "{user_query}"

    Here are the SQL results:
    Columns: {columns}
    Rows:
    {table_text}

    Based on this data, provide a direct natural language answer
    to the user's query. Be concise and factual.
    """

    summary = client.text_generation(
        prompt,
        model="meta-llama/Meta-Llama-3-8B-Instruct",  # or GPT-4 if available
        max_new_tokens=200,
        temperature=0.2
    )
    return summary

if __name__ == "__main__":
    sample_result = {
        "columns": ["name", "department", "salary"],
        "rows": [("Alice", "IT", 80000), ("Bob", "IT", 90000)]
    }
    user_query = "Show me all employees in IT earning more than 70k"
    print(summarize_answer(user_query, sample_result))

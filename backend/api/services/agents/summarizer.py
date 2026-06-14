import os
from openai import OpenAI
import backend.core.config as config

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=config.HF_TOKEN,
)

def summarize_answer(user_query: str, result: dict) -> str:
    """
    Answer the user query based on SQL results.
    result = {"columns": [...], "rows": [...]}
    """
    columns = result["columns"]
    rows = result["rows"]

    table_text = "\n".join([", ".join(map(str, row)) for row in rows])

    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct:featherless-ai",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers user queries based on SQL results."
            },
            {
                "role": "user",
                "content": f"""
                User query: {user_query}
                SQL Results:
                Columns: {columns}
                Rows:
                {table_text}

                Provide a direct natural language answer to the query.
                """
            }
        ],
        max_tokens=200,
        temperature=0.2
    )

    return completion.choices[0].message.content

if __name__ == "__main__":
    sample_result = {
        "columns": ["name", "department", "salary"],
        "rows": [("Alice", "IT", 80000), ("Bob", "IT", 90000)]
    }
    user_query = "Show me all employees in IT earning more than 70k"
    print(summarize_answer(user_query, sample_result))
